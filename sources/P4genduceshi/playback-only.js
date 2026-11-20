// 判断麦克风里是不是只有正在播放的原文。
// 音响开得很大、学生不读时，录音是原文延迟几十到几百毫秒后的同一条波形。
// 学生自己读时音色不同，波形对不上。

var PLAYBACK_RATE = 8000;

function downsampleMono(samples, fromRate, toRate) {
    if (!samples || !samples.length) return new Float32Array(0);
    if (fromRate === toRate) return Float32Array.from(samples);
    var ratio = fromRate / toRate;
    var outLen = Math.max(0, Math.floor(samples.length / ratio));
    var out = new Float32Array(outLen);
    for (var i = 0; i < outLen; i++) {
        var pos = i * ratio;
        var i0 = Math.floor(pos);
        var frac = pos - i0;
        var a = samples[i0] || 0;
        var b = samples[Math.min(i0 + 1, samples.length - 1)] || 0;
        out[i] = a + (b - a) * frac;
    }
    return out;
}

function signalRms(samples) {
    if (!samples.length) return 0;
    var sum = 0;
    var step = Math.max(1, Math.floor(samples.length / 20000));
    var count = 0;
    for (var i = 0; i < samples.length; i += step) {
        sum += samples[i] * samples[i];
        count++;
    }
    return Math.sqrt(sum / count);
}

function nextPow2(n) {
    var p = 1;
    while (p < n) p <<= 1;
    return p;
}

function fft(re, im) {
    var n = re.length;
    for (var i = 1, j = 0; i < n; i++) {
        var bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) {
            var tr = re[i];
            re[i] = re[j];
            re[j] = tr;
            var ti = im[i];
            im[i] = im[j];
            im[j] = ti;
        }
    }
    for (var len = 2; len <= n; len <<= 1) {
        var ang = -2 * Math.PI / len;
        var wlenRe = Math.cos(ang);
        var wlenIm = Math.sin(ang);
        for (var start = 0; start < n; start += len) {
            var wRe = 1;
            var wIm = 0;
            for (var k = 0; k < len / 2; k++) {
                var even = start + k;
                var odd = even + len / 2;
                var vRe = re[odd] * wRe - im[odd] * wIm;
                var vIm = re[odd] * wIm + im[odd] * wRe;
                re[odd] = re[even] - vRe;
                im[odd] = im[even] - vIm;
                re[even] += vRe;
                im[even] += vIm;
                var nextRe = wRe * wlenRe - wIm * wlenIm;
                wIm = wRe * wlenIm + wIm * wlenRe;
                wRe = nextRe;
            }
        }
    }
}

function dotEnergy(samples) {
    var sum = 0;
    for (var i = 0; i < samples.length; i++) sum += samples[i] * samples[i];
    return sum;
}

function centered(samples) {
    var mean = 0;
    for (var i = 0; i < samples.length; i++) mean += samples[i];
    mean /= samples.length || 1;
    var out = new Float32Array(samples.length);
    for (var j = 0; j < samples.length; j++) out[j] = samples[j] - mean;
    return out;
}

// corr[lag] ≈ sum ref[i] * mic[i + lag]，lag 为正表示麦克风比原文晚。
function correlationCurve(reference, microphone) {
    var ref = centered(reference);
    var mic = centered(microphone);
    var size = nextPow2(ref.length + mic.length);
    var reA = new Float32Array(size);
    var imA = new Float32Array(size);
    var reB = new Float32Array(size);
    var imB = new Float32Array(size);
    reA.set(ref);
    reB.set(mic);
    fft(reA, imA);
    fft(reB, imB);
    for (var k = 0; k < size; k++) {
        var ar = reA[k];
        var ai = imA[k];
        var br = reB[k];
        var bi = -imB[k];
        reA[k] = ar * br - ai * bi;
        imA[k] = ar * bi + ai * br;
        imA[k] = -imA[k];
    }
    fft(reA, imA);
    var scale = Math.sqrt(dotEnergy(ref) * dotEnergy(mic));
    if (scale < 1e-8) scale = 1;
    for (var i = 0; i < size; i++) reA[i] = (reA[i] / size) / scale;
    return reA;
}

function correlationAt(curve, lag) {
    // ifft(fft(ref) * conj(fft(mic))) 的峰值在负延迟上，正 lag 表示麦克风更晚。
    var n = curve.length;
    var index = (n - lag) % n;
    if (index < 0) index += n;
    return curve[index];
}

function bestPlaybackLag(reference, microphone) {
    var curve = correlationCurve(reference, microphone);
    var minLag = -Math.round(PLAYBACK_RATE * 0.04);
    var maxLag = Math.round(PLAYBACK_RATE * 0.32);
    var bestCorr = -1;
    var bestLag = 0;
    for (var lag = minLag; lag <= maxLag; lag++) {
        var corr = correlationAt(curve, lag);
        if (corr > bestCorr) {
            bestCorr = corr;
            bestLag = lag;
        }
    }
    var farLag = Math.round(PLAYBACK_RATE * 0.75);
    return {
        corr: bestCorr,
        far: correlationAt(curve, farLag),
        lagMs: Math.round(bestLag / PLAYBACK_RATE * 1000)
    };
}

function sliceAt(samples, start, length) {
    var out = new Float32Array(length);
    var n = Math.min(length, Math.max(0, samples.length - start));
    for (var i = 0; i < n; i++) out[i] = samples[start + i];
    return out;
}

function loudWindows(reference, length) {
    var hop = PLAYBACK_RATE;
    var windows = [];
    for (var start = 0; start + length <= reference.length; start += hop) {
        windows.push({ start: start, rms: signalRms(reference.subarray(start, start + length)) });
    }
    windows.sort(function (a, b) { return b.rms - a.rms; });
    var picked = [];
    for (var i = 0; i < windows.length && picked.length < 6; i++) {
        var candidate = windows[i];
        var overlaps = picked.some(function (item) {
            return Math.abs(item.start - candidate.start) < length;
        });
        if (!overlaps && candidate.rms > 0.01) picked.push(candidate);
    }
    picked.sort(function (a, b) { return a.start - b.start; });
    return picked;
}

function playbackMessage() {
    return '录音和原文几乎重合，像是只把播放的声音录了进去，没有听到你自己的跟读。请戴上耳机，自己把原文读出来再试。';
}

function silenceMessage() {
    return '录音里几乎没有声音。请检查麦克风，靠近一点，自己把原文读出来再试。';
}

function round3(value) {
    return Math.round(value * 1000) / 1000;
}

function judgeMicAgainstReference(reference, referenceRate, microphone, microphoneRate) {
    var empty = {
        block: false,
        kind: 'skip',
        message: '',
        correlation: 0,
        farCorrelation: 0,
        lagMs: 0,
        segments: 0,
        playbackSegments: 0,
        micRms: 0
    };
    if (!reference || !microphone || !referenceRate || !microphoneRate) return empty;
    var ref = downsampleMono(reference, referenceRate, PLAYBACK_RATE);
    var mic = downsampleMono(microphone, microphoneRate, PLAYBACK_RATE);
    var n = Math.min(ref.length, mic.length);
    if (n < PLAYBACK_RATE * 2) return empty;
    ref = ref.subarray(0, n);
    mic = mic.subarray(0, n);
    var micRms = signalRms(mic);
    var refRms = signalRms(ref);
    if (refRms < 0.005) return empty;
    if (micRms < 0.004) {
        return {
            block: true,
            kind: 'silence',
            message: silenceMessage(),
            correlation: 0,
            farCorrelation: 0,
            lagMs: 0,
            segments: 0,
            playbackSegments: 0,
            micRms: round3(micRms)
        };
    }

    var win = Math.floor(PLAYBACK_RATE * 2.5);
    var windows = loudWindows(ref, win);
    if (windows.length < 3) return empty;
    var corrSum = 0;
    var farSum = 0;
    var lags = [];
    var playbackSegments = 0;
    for (var i = 0; i < windows.length; i++) {
        var start = windows[i].start;
        var scored = bestPlaybackLag(sliceAt(ref, start, win), sliceAt(mic, start, win));
        corrSum += scored.corr;
        farSum += scored.far;
        lags.push(scored.lagMs);
        if (scored.corr >= 0.68 && scored.corr - scored.far >= 0.25) playbackSegments++;
    }
    lags.sort(function (a, b) { return a - b; });
    var lagSpread = lags[lags.length - 1] - lags[0];
    var segments = windows.length;
    var playback = playbackSegments >= Math.ceil(segments * 0.67) && lagSpread <= 40;
    return {
        block: playback,
        kind: playback ? 'playback' : 'ok',
        message: playback ? playbackMessage() : '',
        correlation: round3(corrSum / segments),
        farCorrelation: round3(farSum / segments),
        lagMs: lags[Math.floor(lags.length / 2)],
        segments: segments,
        playbackSegments: playbackSegments,
        micRms: round3(micRms)
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        judgeMicAgainstReference: judgeMicAgainstReference,
        playbackMessage: playbackMessage,
        silenceMessage: silenceMessage
    };
}
