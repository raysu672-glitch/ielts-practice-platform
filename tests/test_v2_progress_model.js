const assert = require('node:assert/strict');
const Model = require('../sources/v2-progress/progress_model.js');
const Demo = require('../sources/v2-progress/demo_data.js');

const DAY = Model.DAY_MS;
const T0 = Date.parse('2026-11-01T02:00:00.000Z');

function item(id, type, extra) {
    return Object.assign({
        id, sort_order: id, item_type: type, unit_id: null, unit_title: null, module_type: 'dictation',
        test_unit_ids: [], test_title: '', status: 'pending', study_completed: false, test_passed: false,
    }, extra);
}

function rawFacts(attempts) {
    return {
        source: 'platform_db',
        server_time: new Date(T0).toISOString(),
        student: { id: 's1', name: '测试' },
        module_names: { dictation: '听力1000词', sentence: '长难句分析' },
        plan_items: [
            item(1, 'study', { unit_id: 'd1', unit_title: '第1组', study_completed: true }),
            item(2, 'test', { test_unit_ids: ['d1'], test_title: 'U1 单元测试' }),
            item(3, 'study', { unit_id: 'd2', unit_title: '第2组' }),
            item(4, 'study', { unit_id: 'd3', unit_title: '第3组' }),
            item(5, 'test', { test_unit_ids: ['d2', 'd3'], test_title: 'U2–U3 阶段测' }),
            item(6, 'study', { unit_id: 's1', unit_title: '句1-5', module_type: 'sentence', study_completed: true }),
        ],
        test_attempts: attempts,
    };
}

function attempt(id, title, passed, at, score) {
    return { id, module_type: 'dictation', test_title: title, score: score || (passed ? 90 : 60), threshold: 80, passed, at: new Date(at).toISOString() };
}

// 学完打勾不算过关；没有任何测试记录时路程为 0
let v = Model.build(rawFacts([]), T0);
assert.equal(v.route.total, 4);
assert.equal(v.route.passed, 0);
assert.equal(v.route.studiedOnly, 2);
assert.equal(v.unitById.d1.route, 'open');
assert.equal(v.subjects.length, 2);
assert.equal(v.subjects[0].stages.length, 2);
assert.equal(v.subjects[1].stages[0].noStageTest, true);
assert.equal(v.unitById.d1.hasUnitTest, true);
assert.equal(v.unitById.d2.hasUnitTest, false);

// 阶段 = 旧清单的多单元阶段测；同时有单元测试的单元仍留在该段里
const mixed = rawFacts([]);
mixed.plan_items.push(item(8, 'test', { test_unit_ids: ['d2'], test_title: 'U2 单元测试' }));
const mv = Model.build(mixed, T0);
assert.equal(mv.subjects[0].stages.length, 2);
assert.deepEqual(mv.subjects[0].stages[1].unitIds, ['d2', 'd3']);
assert.equal(mv.subjects[0].stages[1].withUnitTest, 1);

// 单单元测试达标 → 过关；多单元阶段测达标 → 待定，不计入路程
const passes = [
    attempt(1, 'U1 单元测试', true, T0),
    attempt(2, 'U2–U3 阶段测', true, T0),
];
v = Model.build(rawFacts(passes), T0);
assert.equal(v.unitById.d1.route, 'passed');
assert.equal(v.unitById.d2.route, 'pending');
assert.equal(v.unitById.d3.route, 'pending');
assert.equal(v.route.passed, 1);
assert.equal(v.route.pending, 2);
assert.equal(v.subjects[0].stages[0].complete, true);
assert.equal(v.unitById.d1.mastery.state, 'strong');
assert.equal(v.unitById.d2.mastery.value, null);

// 遗忘：时间过去 → 掌握度下降进入复习，但路程不变
const later = Model.build(rawFacts(passes), T0 + 20 * DAY);
assert.equal(later.route.passed, 1);
assert.equal(later.unitById.d1.mastery.state, 'review');
assert.ok(later.unitById.d1.mastery.value < Model.MASTERY.reviewBelow);
assert.equal(later.reviewQueue[0].unitId, 'd1');
let changes = Model.diff(v, later);
assert.deepEqual(changes.dropped, ['d1']);
assert.deepEqual(changes.passed, []);

// 复测通过 → 掌握度恢复且稳定期变长
const retest = passes.concat([attempt(3, 'U1 单元测试', true, T0 + 20 * DAY)]);
const restored = Model.build(rawFacts(retest), T0 + 20 * DAY);
assert.equal(restored.unitById.d1.mastery.state, 'strong');
assert.ok(restored.unitById.d1.mastery.stabilityDays > Model.MASTERY.initialStabilityDays);
assert.deepEqual(Model.diff(later, restored).restored, ['d1']);

// 复测未过 → 掌握度压低，但路程仍保留
const failed = passes.concat([attempt(3, 'U1 单元测试', false, T0 + DAY)]);
const afterFail = Model.build(rawFacts(failed), T0 + DAY);
assert.equal(afterFail.unitById.d1.route, 'passed');
assert.equal(afterFail.unitById.d1.mastery.retestFailed, true);
assert.equal(afterFail.unitById.d1.mastery.state, 'review');
assert.equal(afterFail.route.passed, 1);

// 计划里 test_passed 被重置（重新应用清单）时，以测试记录为准，路程不倒退
const resetRaw = rawFacts(passes);
resetRaw.plan_items.forEach((it) => { it.test_passed = false; });
assert.equal(Model.build(resetRaw, T0).route.passed, 1);

// 新过关在 diff 中被识别；下一里程碑指向待过关单元
const before = Model.build(rawFacts([]), T0);
const after = Model.build(rawFacts([attempt(1, 'U1 单元测试', true, T0)]), T0);
assert.deepEqual(Model.diff(before, after).passed, ['d1']);
assert.equal(after.nextMilestone.nextUnitId, 'd2');
assert.equal(after.nextMilestone.multiUnitTest, true);

// 清单变更：新增单元 → 重算并报告变化
const grown = rawFacts(passes);
grown.plan_items.push(item(7, 'study', { unit_id: 'd4', unit_title: '第4组' }));
changes = Model.diff(v, Model.build(grown, T0));
assert.deepEqual(changes.plan.added, ['d4']);
assert.equal(changes.plan.totalBefore, 4);
assert.equal(changes.plan.totalAfter, 5);

// 演示数据走同一套模型：过关后三层同步增加
const demoNow = T0;
const demoRaw = Demo.create(demoNow);
const d0 = Model.build(demoRaw, demoNow);
const target = d0.nextMilestone.nextUnitId;
const subj0 = d0.subjects.find((s) => s.moduleType === d0.unitById[target].moduleType);
Demo.addAttempt(demoRaw, target, true, demoNow + 60000);
const d1 = Model.build(demoRaw, demoNow + 60000);
const subj1 = d1.subjects.find((s) => s.moduleType === subj0.moduleType);
assert.equal(d1.unitById[target].route, 'passed');
assert.equal(subj1.passed, subj0.passed + 1);
assert.equal(d1.route.passed, d0.route.passed + 1);
assert.deepEqual(Model.diff(d0, d1).passed, [target]);

console.log('test_v2_progress_model.js ok');
