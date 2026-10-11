/**
 * 口语复合句今日任务：三步都通过才上报，凑满 10 句才打勾。
 * 自由练（没有 plan_item_id）不产生任何消息。
 */
const assert = require('assert');
const task = require('../sources/kouyulianxi/complex-task.js');

const query = '?part=p1&p1=complex&kind=pattern&id=p3&plan_item_id=42&unit_id=speaking_complex_pattern_p3&content_version=1';
const parsed = task.parseComplexTaskQuery(query);
assert.strictEqual(parsed.active, true);
assert.strictEqual(parsed.kind, 'pattern');
assert.strictEqual(parsed.id, 'p3');
assert.strictEqual(parsed.planItemId, 42);
assert.strictEqual(parsed.unitId, 'speaking_complex_pattern_p3');

assert.strictEqual(task.parseComplexTaskQuery('?kind=pattern&id=p1').active, false, '自由练不上报');
assert.strictEqual(task.parseComplexTaskQuery('?plan_item_id=1&kind=nope&id=p1').active, false);
assert.strictEqual(task.parseComplexTaskQuery('').active, false);

assert.strictEqual(task.isSentenceFullyDone({ a: true, sh: true, sp: true }), true);
assert.strictEqual(task.isSentenceFullyDone({ a: true, sh: false, sp: true }), false, '跳过跟读不算');
assert.strictEqual(task.isSentenceFullyDone({ a: true, sh: true, sp: false }), false);
assert.strictEqual(task.isSentenceFullyDone(null), false);

let keys = [];
let report = task.scopeReportForSentence(keys, 0, false, 10);
assert.strictEqual(report.added, false);
assert.strictEqual(task.buildTaskMessages(parsed, report).length, 0);

report = task.scopeReportForSentence(keys, 3, true, 10);
assert.deepStrictEqual(report.keys, ['3']);
assert.strictEqual(report.complete, false);
const one = task.buildTaskMessages(parsed, report);
assert.strictEqual(one.length, 1);
assert.strictEqual(one[0].type, 'taskScopeProgress');
assert.strictEqual(one[0].scope_key, '3');
assert.strictEqual(one[0].plan_item_id, 42);

keys = report.keys;
report = task.scopeReportForSentence(keys, 3, true, 10);
assert.strictEqual(report.added, false, '同一句不重复上报');

for (let i = 0; i < 9; i++) {
    report = task.scopeReportForSentence(keys, i, true, 10);
    keys = report.keys;
}
assert.strictEqual(report.complete, false);
assert.strictEqual(task.buildTaskMessages(parsed, report).some(function (m) {
    return m.type === 'taskUnitComplete';
}), false);

report = task.scopeReportForSentence(keys, 9, true, 10);
assert.strictEqual(report.scopeDone, 10);
assert.strictEqual(report.complete, true);
const doneMsgs = task.buildTaskMessages(parsed, report);
assert.strictEqual(doneMsgs[0].type, 'taskScopeProgress');
assert.strictEqual(doneMsgs[1].type, 'taskUnitComplete');
assert.strictEqual(doneMsgs[1].scope_done, 10);
assert.strictEqual(doneMsgs[1].unit_id, 'speaking_complex_pattern_p3');

const bulk = task.messagesForDoneIndexes(parsed, [0, 1, 1, '2'], 10);
assert.strictEqual(bulk.length, 3);
assert.strictEqual(bulk.some(function (m) { return m.type === 'taskUnitComplete'; }), false);

const all = [];
for (let i = 0; i < 10; i++) all.push(i);
const full = task.messagesForDoneIndexes(parsed, all, 10);
assert.strictEqual(full.length, 11);
assert.strictEqual(full[10].type, 'taskUnitComplete');
assert.strictEqual(full[10].scope_done, 10);
assert.strictEqual(task.messagesForDoneIndexes({ active: false }, all, 10).length, 0);

console.log('test_complex_task.js ok');
