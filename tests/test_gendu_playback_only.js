const assert = require('node:assert/strict');
const { judgeMicAgainstReference } = require('../sources/P4genduceshi/playback-only.js');

const SR = 8000;

function voice(seconds, freq) {
    const n = SR * seconds;
    const out = new Float32Array(n);
    for (let i = 0; i < n; i++) {
        const t = i / SR;
        const syllable = Math.floor(t * 3.5);
        const f = freq * (1 + 0.18 * ((syllable % 5) - 2));
        const phase = (t * 3.5) % 1;
        const env = Math.sin(Math.PI * phase);
        out[i] = env * (
            Math.sin(2 * Math.PI * f * t)
            + 0.4 * Math.sin(2 * Math.PI * f * (2 + (syllable % 2)) * t)
            + 0.15 * Math.sin(2 * Math.PI * f * (3.4 + (syllable % 3) * 0.3) * t)
        );
    }
    return out;
}

function delay(samples, ms) {
    const shift = Math.round(SR * ms / 1000);
    const out = new Float32Array(samples.length);
    for (let i = shift; i < samples.length; i++) out[i] = samples[i - shift];
    return out;
}

function reverb(samples) {
    const taps = [0, 70, 140, 230];
    const gains = [1, 0.45, 0.28, 0.16];
    const out = new Float32Array(samples.length);
    for (let t = 0; t < taps.length; t++) {
        for (let i = taps[t]; i < samples.length; i++) out[i] += gains[t] * samples[i - taps[t]];
    }
    return out;
}

function mix(a, b, gainB) {
    const out = new Float32Array(a.length);
    for (let i = 0; i < a.length; i++) out[i] = a[i] + gainB * (b[i] || 0);
    return out;
}

function noise(n, gain) {
    const out = new Float32Array(n);
    let seed = 17;
    for (let i = 0; i < n; i++) {
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        out[i] = ((seed / 0x7fffffff) * 2 - 1) * gain;
    }
    return out;
}

const lesson = voice(12, 150);
const played = mix(reverb(delay(lesson, 60)), noise(lesson.length, 0.08), 1);
const student = delay(voice(12, 230), 420);
const both = mix(student, played, 0.85);
const quiet = noise(lesson.length, 0.001);

const playback = judgeMicAgainstReference(lesson, SR, played, SR);
const spoken = judgeMicAgainstReference(lesson, SR, student, SR);
const mixed = judgeMicAgainstReference(lesson, SR, both, SR);
const silent = judgeMicAgainstReference(lesson, SR, quiet, SR);
const late = judgeMicAgainstReference(lesson, SR, delay(lesson, 200), SR);

assert.equal(playback.block, true);
assert.equal(playback.kind, 'playback');
assert.ok(playback.lagMs >= 45 && playback.lagMs <= 80);
assert.match(playback.message, /播放的声音/);

assert.equal(late.block, true);
assert.equal(late.kind, 'playback');
assert.ok(late.lagMs >= 180 && late.lagMs <= 230);

assert.equal(spoken.block, false);
assert.equal(spoken.kind, 'ok');

assert.equal(mixed.block, false);
assert.equal(mixed.kind, 'ok');

assert.equal(silent.block, true);
assert.equal(silent.kind, 'silence');
assert.match(silent.message, /几乎没有声音/);
