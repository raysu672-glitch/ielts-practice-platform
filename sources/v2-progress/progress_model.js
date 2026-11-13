/*
 * 新版学习路线 · 进度推导（纯函数，浏览器与 node 共用）。
 *
 * 输入：/api/v2/progress/me 返回的原始事实（计划清单 + 阶段测尝试），或演示数据（同结构）。
 * 输出：单元 → 科目阶段 → 总路线 三层，以及掌握度、复习队列、下一里程碑。
 *
 * 口径（docs/v2-pass-system-rules.md）：
 * - 路程进度只认测试达标，且只增不减；学完打勾只作「已学」标记。
 * - 只覆盖 1 个单元的测试达标 = 该单元过关（计入路程）。
 * - 覆盖多个单元的旧阶段测达标：是否整段折算尚未拍板 → 标「待定」，不计入路程。
 * - 掌握度会随时间衰减、复测未过会下降；它不影响路程。
 */
(function (root, factory) {
    if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.V2ProgressModel = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    var DAY_MS = 24 * 60 * 60 * 1000;

    // 暂定参数（未经教研校准）：遗忘曲线沿用 FSRS 的幂函数形式 R = (1 + t / (9S))^-1。
    var MASTERY = {
        initialStabilityDays: 7,
        stabilityGrowth: 2.5,
        maxStabilityDays: 180,
        minRetestGapDays: 1,
        strongAt: 0.9,
        reviewBelow: 0.8,
        failedRetestCap: 0.6
    };

    function parseTime(value) {
        if (value === null || value === undefined || value === '') return null;
        if (typeof value === 'number') return value;
        var t = Date.parse(value);
        return isNaN(t) ? null : t;
    }

    function retrievability(daysSince, stabilityDays) {
        var t = Math.max(0, daysSince);
        return 1 / (1 + t / (9 * stabilityDays));
    }

    function masteryState(value) {
        if (value === null) return 'none';
        if (value >= MASTERY.strongAt) return 'strong';
        if (value >= MASTERY.reviewBelow) return 'fading';
        return 'review';
    }

    function computeMastery(attempts, nowMs, fallbackPassed) {
        var stability = null;
        var lastPassAt = null;
        var lastPassScore = null;
        var retestFailed = false;
        var retests = 0;
        for (var i = 0; i < attempts.length; i++) {
            var a = attempts[i];
            var at = parseTime(a.at);
            if (a.passed) {
                if (lastPassAt === null) {
                    stability = MASTERY.initialStabilityDays;
                } else if (at !== null && (at - lastPassAt) / DAY_MS >= MASTERY.minRetestGapDays) {
                    stability = Math.min(stability * MASTERY.stabilityGrowth, MASTERY.maxStabilityDays);
                    retests += 1;
                }
                lastPassAt = at === null ? lastPassAt : at;
                lastPassScore = a.score;
                retestFailed = false;
            } else if (lastPassAt !== null) {
                retestFailed = true;
            }
        }
        if (lastPassAt === null) {
            return {
                value: null,
                state: 'none',
                lastPassAt: null,
                note: fallbackPassed ? '计划里标记为已过，但没有找到对应的测试记录，无法计算掌握度' : ''
            };
        }
        var days = (nowMs - lastPassAt) / DAY_MS;
        var value = retrievability(days, stability);
        if (retestFailed) value = Math.min(value, MASTERY.failedRetestCap);
        var state = masteryState(value);
        var reviewAt = lastPassAt + 9 * stability * (1 / MASTERY.reviewBelow - 1) * DAY_MS;
        return {
            value: value,
            state: state,
            lastPassAt: lastPassAt,
            lastPassScore: lastPassScore,
            daysSincePass: days,
            stabilityDays: stability,
            retests: retests,
            retestFailed: retestFailed,
            reviewAt: retestFailed ? nowMs : reviewAt
        };
    }

    // submit_stage_test 把空标题记成「阶段测」，这里按同样口径对齐
    function attemptKey(moduleType, title) {
        return String(moduleType || '') + '\u0001' + String(title || '阶段测');
    }

    function build(raw, nowMs) {
        raw = raw || {};
        var now = typeof nowMs === 'number' ? nowMs : (parseTime(raw.server_time) || Date.now());
        var names = raw.module_names || {};
        var items = (raw.plan_items || []).slice().sort(function (a, b) {
            return (a.sort_order - b.sort_order) || (a.id - b.id);
        });

        var attemptsByKey = {};
        (raw.test_attempts || []).slice().sort(function (a, b) {
            return (parseTime(a.at) || 0) - (parseTime(b.at) || 0) || (a.id || 0) - (b.id || 0);
        }).forEach(function (a) {
            var k = attemptKey(a.module_type, a.test_title);
            (attemptsByKey[k] = attemptsByKey[k] || []).push(a);
        });

        var units = [];
        var unitById = {};
        var subjects = [];
        var subjectByType = {};

        function subjectFor(mt) {
            if (!subjectByType[mt]) {
                subjectByType[mt] = {
                    moduleType: mt,
                    name: names[mt] || mt || '未命名科目',
                    units: [],
                    stages: []
                };
                subjects.push(subjectByType[mt]);
            }
            return subjectByType[mt];
        }

        items.forEach(function (it) {
            if (it.item_type !== 'study' || !it.unit_id || unitById[it.unit_id]) return;
            var subj = subjectFor(it.module_type);
            var u = {
                unitId: it.unit_id,
                title: it.unit_title || it.unit_id,
                unitNo: it.unit_no || null,
                moduleType: it.module_type,
                subjectName: subj.name,
                routeIndex: units.length,
                indexInSubject: subj.units.length,
                studied: !!it.study_completed,
                route: 'open',
                evidence: null,
                mastery: { value: null, state: 'none', lastPassAt: null },
                stageKey: null
            };
            units.push(u);
            unitById[u.unitId] = u;
            subj.units.push(u);
        });

        // 单单元测试 = 单元过关证据；多单元阶段测 = 旧清单的「阶段」，达标只算待定证据。
        var stageTests = [];
        items.forEach(function (t) {
            if (t.item_type !== 'test') return;
            var covered = (t.test_unit_ids || []).filter(function (id) { return unitById[id]; });
            if (!covered.length) return;
            var attempts = attemptsByKey[attemptKey(t.module_type, t.test_title)] || [];
            var info = {
                id: t.id,
                title: t.test_title || '阶段测',
                covered: covered,
                attempts: attempts,
                everPassed: attempts.some(function (a) { return a.passed; }) || !!t.test_passed,
                planPassed: !!t.test_passed
            };
            if (covered.length === 1) {
                var u = unitById[covered[0]];
                (u.unitTests = u.unitTests || []).push(info);
            } else {
                stageTests.push(info);
                covered.forEach(function (id) {
                    var cu = unitById[id];
                    (cu.stageTests = cu.stageTests || []).push(info);
                    if (!cu.stageKey) cu.stageKey = 'test:' + t.id;
                });
            }
        });

        units.forEach(function (u) {
            var own = u.unitTests || [];
            u.hasUnitTest = own.length > 0;
            var ownPassed = own.filter(function (t) { return t.everPassed; });
            if (ownPassed.length) {
                var merged = [];
                own.forEach(function (t) { merged = merged.concat(t.attempts); });
                merged.sort(function (a, b) { return (parseTime(a.at) || 0) - (parseTime(b.at) || 0); });
                u.route = 'passed';
                u.evidence = { kind: 'unit_test', testTitle: ownPassed[0].title, attempts: merged };
                u.mastery = computeMastery(merged, now, ownPassed.some(function (t) { return t.planPassed; }));
                return;
            }
            var stagePassed = (u.stageTests || []).filter(function (t) { return t.everPassed; })[0];
            if (stagePassed) {
                var passedAt = null;
                stagePassed.attempts.forEach(function (a) { if (a.passed) passedAt = parseTime(a.at); });
                u.route = 'pending';
                u.evidence = {
                    kind: 'stage_multi',
                    testTitle: stagePassed.title,
                    coveredCount: stagePassed.covered.length,
                    passedAt: passedAt
                };
            }
        });

        var testById = {};
        stageTests.forEach(function (t) { testById['test:' + t.id] = t; });

        subjects.forEach(function (subj) {
            var openRun = 0;
            subj.units.forEach(function (u) {
                var key = u.stageKey;
                if (!key) {
                    var prevU = subj.units[u.indexInSubject - 1];
                    if (!prevU || prevU.stageKey.indexOf('open:') !== 0) openRun += 1;
                    key = u.stageKey = 'open:' + subj.moduleType + ':' + openRun;
                }
                var st = subj.stages[subj.stages.length - 1];
                if (!st || st.key !== key) {
                    var t = testById[key];
                    st = {
                        key: key,
                        testTitle: t ? t.title : '',
                        noStageTest: !t,
                        stageTestPassed: t ? t.everPassed : false,
                        stageTestAttempts: t ? t.attempts.length : 0,
                        unitIds: []
                    };
                    subj.stages.push(st);
                }
                st.unitIds.push(u.unitId);
            });
            subj.stages.forEach(function (st, idx) {
                st.index = idx;
                st.label = '第 ' + (idx + 1) + ' 段';
                var su = st.unitIds.map(function (id) { return unitById[id]; });
                st.total = su.length;
                st.passed = su.filter(function (u) { return u.route === 'passed'; }).length;
                st.pending = su.filter(function (u) { return u.route === 'pending'; }).length;
                st.withUnitTest = su.filter(function (u) { return u.hasUnitTest; }).length;
                st.complete = st.passed === st.total;
            });
            var counted = subj.units.filter(function (u) { return u.route === 'passed'; });
            subj.total = subj.units.length;
            subj.passed = counted.length;
            subj.pending = subj.units.filter(function (u) { return u.route === 'pending'; }).length;
            subj.studiedOnly = subj.units.filter(function (u) { return u.route === 'open' && u.studied; }).length;
            var withMastery = counted.filter(function (u) { return u.mastery.value !== null; });
            subj.masteryAvg = withMastery.length
                ? withMastery.reduce(function (s, u) { return s + u.mastery.value; }, 0) / withMastery.length
                : null;
            subj.review = counted.filter(function (u) { return u.mastery.state === 'review'; }).length;
            subj.fading = counted.filter(function (u) { return u.mastery.state === 'fading'; }).length;
            subj.currentStage = subj.stages.filter(function (s) { return !s.complete; })[0] || null;
        });

        var route = {
            total: units.length,
            passed: units.filter(function (u) { return u.route === 'passed'; }).length,
            pending: units.filter(function (u) { return u.route === 'pending'; }).length,
            studiedOnly: units.filter(function (u) { return u.route === 'open' && u.studied; }).length
        };
        route.remaining = route.total - route.passed;

        var reviewQueue = units.filter(function (u) {
            return u.route === 'passed' && (u.mastery.state === 'review' || u.mastery.state === 'fading');
        }).sort(function (a, b) { return a.mastery.value - b.mastery.value; });

        var zones = buildZones(subjects);
        var badges = { total: 0, earned: 0 };
        zones.forEach(function (z) { badges.total += z.badgesTotal; badges.earned += z.badges; });

        return {
            now: now,
            source: raw.source || 'unknown',
            zones: zones,
            badges: badges,
            activity: activity(units, raw.test_attempts || [], now, 7),
            student: raw.student || {},
            planMeta: raw.plan_meta || {},
            route: route,
            subjects: subjects,
            units: units,
            reviewQueue: reviewQueue,
            nextMilestone: nextMilestone(subjects, units, unitById),
            planSignature: units.map(function (u) { return u.unitId; }).slice().sort().join('|'),
            unitById: unitById
        };
    }

    // 原系统没有「技能区」字段，这里按科目所属技能分区，仅用于版面分组。
    var ZONES = [
        { key: 'listening', name: '听力区', modules: ['dictation', 'listening_basic', 'listening_synonym', 'listening_p4_speed'] },
        { key: 'reading', name: '阅读区', modules: ['reading_synonym', 'sentence'] },
        { key: 'writing', name: '写作区', modules: ['writing_phrase', 'writing_translate', 'writing_correction'] },
        { key: 'speaking', name: '口语区', modules: ['speaking', 'speaking_p1', 'speaking_complex', 'speaking_p2_material', 'speaking_p2_apply'] }
    ];

    function zoneKeyOf(mt) {
        for (var i = 0; i < ZONES.length; i++) {
            if (ZONES[i].modules.indexOf(mt) >= 0) return ZONES[i].key;
        }
        return 'other';
    }

    function buildZones(subjects) {
        var defs = ZONES.concat([{ key: 'other', name: '其他', modules: [] }]);
        return defs.map(function (d) {
            var subs = subjects.filter(function (s) { return zoneKeyOf(s.moduleType) === d.key; });
            var z = { key: d.key, name: d.name, subjects: subs, total: 0, passed: 0, pending: 0, badges: 0, badgesTotal: 0 };
            subs.forEach(function (s) {
                s.zoneKey = d.key;
                z.total += s.total; z.passed += s.passed; z.pending += s.pending;
                z.badgesTotal += s.stages.length;
                z.badges += s.stages.filter(function (st) { return st.complete; }).length;
            });
            return z;
        }).filter(function (z) { return z.subjects.length; });
    }

    // 近 N 天：测了几次、新过几关、复测描深几次（都来自测试记录）
    function activity(units, attempts, now, days) {
        var since = now - days * DAY_MS;
        var out = { days: days, attempts: 0, newPasses: 0, retestPasses: 0 };
        attempts.forEach(function (a) {
            var t = parseTime(a.at);
            if (t !== null && t >= since && t <= now) out.attempts += 1;
        });
        units.forEach(function (u) {
            if (u.route !== 'passed') return;
            var passes = u.evidence.attempts.filter(function (a) { return a.passed; })
                .map(function (a) { return parseTime(a.at); })
                .filter(function (t) { return t !== null && t <= now; });
            passes.forEach(function (t, i) {
                if (t < since) return;
                if (i === 0) out.newPasses += 1;
                else out.retestPasses += 1;
            });
        });
        return out;
    }

    function stageByUnit(subjects, u) {
        var subj = null;
        var st = null;
        subjects.forEach(function (s) {
            if (s.moduleType !== u.moduleType) return;
            subj = s;
            s.stages.forEach(function (x) { if (x.key === u.stageKey) st = x; });
        });
        return { subject: subj, stage: st };
    }

    function openIn(stage, unitById) {
        return stage.unitIds.map(function (id) { return unitById[id]; })
            .filter(function (u) { return u.route === 'open'; });
    }

    // 目标只指向学生还能动手的格子（open）。待定格已经测过，等的是折算政策，不拿来当目标。
    // 优先：所在段已经有进度、并且这一格能单独测过（再过几关就点亮徽章）。
    function nextMilestone(subjects, units, unitById) {
        var best = null;
        function consider(u, rank) {
            var ctx = stageByUnit(subjects, u);
            if (!ctx.stage) return;
            var remaining = openIn(ctx.stage, unitById).length;
            // 只在「再过几关就点亮徽章」这一档里挑离徽章最近的；其余档按路线顺序
            var closerBadge = best && rank === 0 && best.rank === 0 &&
                (remaining < best.remaining || (remaining === best.remaining && u.routeIndex < best.unit.routeIndex));
            var earlier = best && rank === best.rank && rank !== 0 && u.routeIndex < best.unit.routeIndex;
            if (!best || rank < best.rank || closerBadge || earlier) {
                best = { subject: ctx.subject, stage: ctx.stage, unit: u, remaining: remaining, rank: rank };
            }
        }
        units.forEach(function (u) {
            if (u.route !== 'open') return;
            var ctx = stageByUnit(subjects, u);
            var started = ctx.stage && ctx.stage.passed > 0;
            if (u.hasUnitTest && started) consider(u, 0);
            else if (u.hasUnitTest) consider(u, 1);
            else if (started) consider(u, 2);
            else consider(u, 3);
        });
        if (!best) return null;
        var nextUnit = best.unit;
        return {
            moduleType: best.subject.moduleType,
            subjectName: best.subject.name,
            stageKey: best.stage.key,
            stageLabel: best.stage.label,
            remaining: best.remaining,
            stageTotal: best.stage.total,
            stagePassed: best.stage.passed,
            testTitle: best.stage.testTitle,
            nextHasUnitTest: !!(nextUnit && nextUnit.hasUnitTest),
            multiUnitTest: !!(nextUnit && !nextUnit.hasUnitTest && !best.stage.noStageTest),
            noTest: !!(nextUnit && !nextUnit.hasUnitTest && best.stage.noStageTest),
            nextUnitId: nextUnit ? nextUnit.unitId : null,
            nextUnitTitle: nextUnit ? nextUnit.title : ''
        };
    }

    function diff(prev, next) {
        var out = { passed: [], pending: [], dropped: [], restored: [], plan: null };
        if (!prev || !next) return out;
        next.units.forEach(function (u) {
            var p = prev.unitById[u.unitId];
            if (!p) return;
            if (u.route === 'passed' && p.route !== 'passed') out.passed.push(u.unitId);
            else if (u.route === 'pending' && p.route === 'open') out.pending.push(u.unitId);
            if (u.route === 'passed' && p.route === 'passed') {
                var was = p.mastery.state;
                var is = u.mastery.state;
                if (is === 'review' && was !== 'review') out.dropped.push(u.unitId);
                else if ((was === 'review' || was === 'fading') && is === 'strong') out.restored.push(u.unitId);
            }
        });
        if (prev.planSignature !== next.planSignature) {
            out.plan = planChange(prev.units.map(function (u) { return u.unitId; }), next);
        }
        return out;
    }

    function planChange(prevUnitIds, next) {
        var before = {};
        prevUnitIds.forEach(function (id) { before[id] = true; });
        var added = next.units.filter(function (u) { return !before[u.unitId]; }).map(function (u) { return u.unitId; });
        var removed = prevUnitIds.filter(function (id) { return !next.unitById[id]; });
        return {
            totalBefore: prevUnitIds.length,
            totalAfter: next.units.length,
            added: added,
            removed: removed
        };
    }

    return {
        MASTERY: MASTERY,
        DAY_MS: DAY_MS,
        ZONES: ZONES,
        build: build,
        diff: diff,
        planChange: planChange,
        retrievability: retrievability,
        computeMastery: computeMastery
    };
}));
