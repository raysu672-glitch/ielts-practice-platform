/*
 * 交互演示用的示例数据（不是任何学生的真实进度）。
 *
 * 结构与 /api/v2/progress/me 完全相同，交给同一个 progress_model.js 推导；
 * 演示里假设「新版已有单元级测试」（每个单元一次测试），另保留一段旧式多单元阶段测，
 * 用来展示「折算政策待定」的样子。
 */
(function (root, factory) {
    if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.V2ProgressDemo = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    var DAY = 24 * 60 * 60 * 1000;

    var SUBJECTS = [
        { mt: 'dictation', name: '听力1000词', units: ['第1组', '第2组', '第3组', '第4组', '第5组', '第6组', '第7组', '第8组', '第9组', '第10组'] },
        { mt: 'reading_synonym', name: '阅读同义替换', units: ['单元1 · 入门基础篇', '单元2 · 学术核心篇', '单元3 · 阅读高频篇', '单元4 · 动词进阶篇', '单元5 · 形容词扩展篇', '单元6 · 名词辨析篇', '单元7 · 副词强化篇', '单元8 · 因果逻辑篇', '单元9 · 转折对比篇'] },
        { mt: 'listening_synonym', name: '听力同义替换', units: ['第1单元 · 题1-5', '第2单元 · 题6-10', '第3单元 · 题11-15', '第4单元 · 题16-20', '第5单元 · 题21-25', '第6单元 · 题26-30'] },
        { mt: 'sentence', name: '长难句分析', units: ['第1单元 · 句1-5', '第2单元 · 句6-10', '第3单元 · 句11-15', '第4单元 · 句16-20', '第5单元 · 句21-25', '第6单元 · 句26-30', '第7单元 · 句31-35', '第8单元 · 句36-40'] },
        { mt: 'writing_phrase', name: '写作词伙', units: ['基础必背 · 1-10', '基础必背 · 11-20', '小作文词伙一 · 1-10', '小作文词伙一 · 11-20', '教育类 · 1-10', '教育类 · 11-20'] },
        { mt: 'speaking_p1', name: '口语P1', units: ['P1 第1单元 · 10题', 'P1 第2单元 · 10题', 'P1 第3单元 · 10题', 'P1 第4单元 · 10题', 'P1 第5单元 · 10题', 'P1 第6单元 · 10题'] }
    ];

    // 每科每段 3 个单元；阅读同义替换第 1 段保留旧式「一次测 3 单元」阶段测。
    var LEGACY_STAGE = { mt: 'reading_synonym', stage: 0 };

    function iso(ms) { return new Date(ms).toISOString(); }

    function create(nowMs) {
        var now = typeof nowMs === 'number' ? nowMs : Date.now();
        var items = [];
        var attempts = [];
        var names = {};
        var id = 1;
        var attemptId = 1;
        var sort = 0;

        // 每科已过关单元数与距今天数（越早过关越可能在褪色）
        var history = {
            dictation: [16, 12, 9, 6, 4, 2],
            reading_synonym: [3, 2],
            listening_synonym: [20, 8, 5],
            sentence: [],
            writing_phrase: [1],
            speaking_p1: []
        };

        SUBJECTS.forEach(function (s) {
            names[s.mt] = s.name;
            var unitIds = s.units.map(function (_, i) { return s.mt + '_u' + String(i + 1).padStart(2, '0'); });
            for (var start = 0; start < unitIds.length; start += 3) {
                var chunk = unitIds.slice(start, start + 3);
                var stageIdx = start / 3;
                chunk.forEach(function (uid, k) {
                    var unitIndex = start + k;
                    items.push({
                        id: id++, sort_order: sort++, item_type: 'study', unit_id: uid,
                        unit_title: s.units[unitIndex], unit_no: unitIndex + 1, module_type: s.mt,
                        test_unit_ids: [], test_title: '', status: 'pending',
                        study_completed: unitIndex < (history[s.mt].length + 1), test_passed: false
                    });
                });
                var legacy = s.mt === LEGACY_STAGE.mt && stageIdx === LEGACY_STAGE.stage;
                if (chunk.length > 1) {
                    items.push({
                        id: id++, sort_order: sort++, item_type: 'test', unit_id: null, unit_title: null,
                        unit_no: null, module_type: s.mt, test_unit_ids: chunk,
                        test_title: s.name + ' U' + (start + 1) + '–U' + (start + chunk.length) + ' 阶段测',
                        status: 'pending', study_completed: false, test_passed: false
                    });
                }
                if (!legacy) {
                    chunk.forEach(function (uid, k) {
                        var unitIndex = start + k;
                        items.push({
                            id: id++, sort_order: sort++, item_type: 'test', unit_id: null, unit_title: null,
                            unit_no: null, module_type: s.mt, test_unit_ids: [uid],
                            test_title: s.name + ' U' + (unitIndex + 1) + ' 单元测试',
                            status: 'pending', study_completed: false, test_passed: false
                        });
                    });
                }
            }
            history[s.mt].forEach(function (daysAgo, i) {
                var legacyUnit = s.mt === LEGACY_STAGE.mt && i < 3;
                var title = legacyUnit
                    ? s.name + ' U1–U3 阶段测'
                    : s.name + ' U' + (i + 1) + ' 单元测试';
                if (legacyUnit && i > 0) return;
                attempts.push({
                    id: attemptId++, module_type: s.mt, test_title: title,
                    score: 84 + (i % 3) * 4, threshold: 80, passed: true, at: iso(now - daysAgo * DAY)
                });
            });
        });

        // 一次早期失败再通过的真实感记录
        attempts.push({
            id: attemptId++, module_type: 'listening_synonym', test_title: '听力同义替换 U3 单元测试',
            score: 70, threshold: 80, passed: false, at: iso(now - 6 * DAY)
        });

        return {
            source: 'demo',
            server_time: iso(now),
            student: { id: 'demo', name: '示例学生', target_score: 6.5 },
            module_names: names,
            plan_items: items,
            test_attempts: attempts,
            plan_meta: { applied_at: iso(now - 40 * DAY), draft_pending: false }
        };
    }

    function nextAttemptId(raw) {
        return raw.test_attempts.reduce(function (m, a) { return Math.max(m, a.id || 0); }, 0) + 1;
    }

    // 有单元测试就考单元测试；没有（旧式段）就考覆盖它的阶段测
    function testFor(raw, unitId) {
        var single = raw.plan_items.filter(function (it) {
            return it.item_type === 'test' && it.test_unit_ids.length === 1 && it.test_unit_ids[0] === unitId;
        })[0];
        if (single) return single;
        return raw.plan_items.filter(function (it) {
            return it.item_type === 'test' && it.test_unit_ids.indexOf(unitId) >= 0;
        })[0] || null;
    }

    function addAttempt(raw, unitId, passed, nowMs) {
        var t = testFor(raw, unitId);
        if (!t) return null;
        var a = {
            id: nextAttemptId(raw), module_type: t.module_type, test_title: t.test_title,
            score: passed ? 88 : 64, threshold: 80, passed: passed, at: new Date(nowMs).toISOString()
        };
        raw.test_attempts.push(a);
        raw.server_time = a.at;
        return a;
    }

    function addUnits(raw, moduleType, count, nowMs) {
        var maxSort = raw.plan_items.reduce(function (m, it) { return Math.max(m, it.sort_order); }, 0);
        var maxId = raw.plan_items.reduce(function (m, it) { return Math.max(m, it.id); }, 0);
        var existing = raw.plan_items.filter(function (it) {
            return it.item_type === 'study' && it.module_type === moduleType;
        }).length;
        var name = raw.module_names[moduleType] || moduleType;
        var added = [];
        for (var i = 0; i < count; i++) {
            var no = existing + i + 1;
            var uid = moduleType + '_u' + String(no).padStart(2, '0');
            raw.plan_items.push({
                id: ++maxId, sort_order: ++maxSort, item_type: 'study', unit_id: uid,
                unit_title: '第' + no + '单元（助教新增）', unit_no: no, module_type: moduleType,
                test_unit_ids: [], test_title: '', status: 'pending', study_completed: false, test_passed: false
            });
            raw.plan_items.push({
                id: ++maxId, sort_order: ++maxSort, item_type: 'test', unit_id: null, unit_title: null,
                unit_no: null, module_type: moduleType, test_unit_ids: [uid],
                test_title: name + ' U' + no + ' 单元测试', status: 'pending', study_completed: false, test_passed: false
            });
            added.push(uid);
        }
        raw.plan_meta = { applied_at: new Date(nowMs).toISOString(), draft_pending: false };
        raw.server_time = new Date(nowMs).toISOString();
        return added;
    }

    return { create: create, addAttempt: addAttempt, addUnits: addUnits, DAY: DAY };
}));
