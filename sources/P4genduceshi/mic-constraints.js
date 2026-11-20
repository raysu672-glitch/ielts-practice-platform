// 跟读只录麦克风。原文是另一个播放器在放，外放时喇叭声仍会进麦克风。
// 人声隔离能压掉旁边的原声；浏览器不支持时保持原来的回声消除。
var SPEAKER_PLAYBACK_VOLUME = 0.35;

function buildMicConstraints(supported) {
    var audio = {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
    };
    if (supported && supported.voiceIsolation) {
        audio.voiceIsolation = { ideal: true };
    }
    return { audio: audio };
}

function playbackForRoute(route) {
    if (route === 'speakers') {
        return {
            volume: SPEAKER_PLAYBACK_VOLUME,
            note: '未戴耳机，原文已放轻。喇叭声仍可能被录进去，分数可能忽高忽低。'
        };
    }
    return { volume: 1, note: '' };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SPEAKER_PLAYBACK_VOLUME: SPEAKER_PLAYBACK_VOLUME,
        buildMicConstraints: buildMicConstraints,
        playbackForRoute: playbackForRoute
    };
}
