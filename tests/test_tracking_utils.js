const assert = require('node:assert/strict');
const utils = require('../sources/tinglidanciceshi/tracking_utils.js');

const sessions = [
    { session_kind: 'study', duration_seconds: 120 },
    { session_kind: 'test', duration_seconds: 300 },
    { duration_seconds: 30 },
];

assert.deepEqual(utils.filterStudySessions(sessions), [sessions[0], sessions[2]]);
assert.equal(utils.sumDuration(utils.filterStudySessions(sessions)), 150);
assert.equal(utils.getTestTypeLabel('module_test'), '模块测试');
assert.equal(utils.getTestTypeLabel('wrong_words'), '错题测试');
assert.deepEqual(utils.parseDetails('[{"word":"apple","isCorrect":false}]'), [
    { word: 'apple', isCorrect: false },
]);
assert.deepEqual(utils.getWrongWordDetails([
    { word: 'apple', isCorrect: false },
    { original: 'sentence', isCorrect: false },
    { word: 'pear', isCorrect: true },
]), [{ word: 'apple', isCorrect: false }]);

console.log('tracking utils tests passed');
