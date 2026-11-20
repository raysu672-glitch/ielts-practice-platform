const assert = require('node:assert/strict');
const {
    SPEAKER_PLAYBACK_VOLUME,
    buildMicConstraints,
    playbackForRoute
} = require('../sources/P4genduceshi/mic-constraints.js');

const plain = buildMicConstraints({});
assert.equal(plain.audio.echoCancellation, true);
assert.equal(plain.audio.noiseSuppression, true);
assert.equal(plain.audio.autoGainControl, true);
assert.equal(Object.prototype.hasOwnProperty.call(plain.audio, 'voiceIsolation'), false);
assert.equal(plain.audio.sampleRate, undefined);

const isolated = buildMicConstraints({ voiceIsolation: true });
assert.deepEqual(isolated.audio.voiceIsolation, { ideal: true });
assert.equal(isolated.audio.echoCancellation, true);

const headphones = playbackForRoute('headphones');
assert.equal(headphones.volume, 1);
assert.equal(headphones.note, '');

const speakers = playbackForRoute('speakers');
assert.equal(speakers.volume, SPEAKER_PLAYBACK_VOLUME);
assert.ok(speakers.volume < 0.5);
assert.match(speakers.note, /放轻/);

assert.equal(playbackForRoute(undefined).volume, 1);
