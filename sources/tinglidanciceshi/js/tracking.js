// 学习/测试追踪工具与保存
(function(root, factory) {
    var api = factory();
    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }
    root.TrackingUtils = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
    var IDLE_LIMIT_MS = 5 * 60 * 1000;

    function isStudySession(session) {
        var kind = session && session.session_kind;
        return !kind || kind === 'study';
    }

    function isTimedSession(session) {
        var kind = session && session.session_kind;
        return !kind || kind === 'study' || kind === 'test';
    }

    function filterStudySessions(sessions) {
        return (sessions || []).filter(isStudySession);
    }

    function filterTimedSessions(sessions) {
        return (sessions || []).filter(isTimedSession);
    }

    function sumDuration(sessions) {
        return (sessions || []).reduce(function(sum, session) {
            return sum + Math.max(0, Number(session && session.duration_seconds) || 0);
        }, 0);
    }

    function resolveModuleType(moduleType) {
        if (typeof normalizeModuleType === 'function') return normalizeModuleType(moduleType);
        return moduleType || '';
    }

    function sumPracticeSeconds(sessions, testRecords, options) {
        options = options || {};
        var moduleId = options.moduleId ? resolveModuleType(options.moduleId) : '';
        var createdAtOk = typeof options.createdAt === 'function' ? options.createdAt : null;
        var seconds = 0;

        filterTimedSessions(sessions).forEach(function(session) {
            if (moduleId && resolveModuleType(session.module_type) !== moduleId) return;
            if (createdAtOk && !createdAtOk(session.created_at)) return;
            seconds += Math.max(0, Number(session.duration_seconds) || 0);
        });

        (testRecords || []).forEach(function(record) {
            var recordModule = resolveModuleType(record && record.module_type);
            // 口语练习时长已记在 study_sessions（录音时长），测试记录里的墙钟时长不重复累计
            if (recordModule === 'speaking') return;
            if (moduleId && recordModule !== moduleId) return;
            if (createdAtOk && !createdAtOk(record.created_at)) return;
            seconds += Math.max(0, Number(record && record.duration_seconds) || 0);
        });
        return seconds;
    }

    function defaultDateKey(value) {
        var d = value ? new Date(value) : new Date();
        if (isNaN(d.getTime())) return '';
        return d.toISOString().slice(0, 10);
    }

    function buildDailyPracticeRows(sessions, testRecords, options) {
        options = options || {};
        var moduleId = options.moduleId ? resolveModuleType(options.moduleId) : '';
        var dateKeyFn = typeof options.dateKey === 'function' ? options.dateKey : defaultDateKey;
        var rows = {};

        function add(iso, seconds, moduleType) {
            var key = dateKeyFn(iso);
            if (!key) return;
            if (!rows[key]) {
                rows[key] = {
                    date: key,
                    moduleSeconds: 0,
                    totalSeconds: 0,
                    moduleCount: 0,
                    totalCount: 0,
                    latest: iso || ''
                };
            }
            var amount = Math.max(0, Number(seconds) || 0);
            rows[key].totalSeconds += amount;
            rows[key].totalCount += 1;
            if (!moduleId || resolveModuleType(moduleType) === moduleId) {
                rows[key].moduleSeconds += amount;
                rows[key].moduleCount += 1;
            }
            if (iso && (!rows[key].latest || new Date(iso) > new Date(rows[key].latest))) {
                rows[key].latest = iso;
            }
        }

        filterTimedSessions(sessions).forEach(function(session) {
            add(session.created_at || session.ended_at, session.duration_seconds, session.module_type);
        });
        (testRecords || []).forEach(function(record) {
            if (resolveModuleType(record && record.module_type) === 'speaking') return;
            add(record.created_at || record.ended_at, record.duration_seconds, record.module_type);
        });

        return Object.keys(rows).map(function(key) { return rows[key]; }).sort(function(a, b) {
            return new Date(b.latest) - new Date(a.latest);
        });
    }

    function pad2(n) {
        return n < 10 ? '0' + n : String(n);
    }

    function getChinaYmd(value) {
        var d = value ? new Date(value) : new Date();
        if (isNaN(d.getTime())) return '';
        var shifted = new Date(d.getTime() + 8 * 60 * 60 * 1000);
        return shifted.getUTCFullYear() + '-' + pad2(shifted.getUTCMonth() + 1) + '-' + pad2(shifted.getUTCDate());
    }

    function shiftYmd(ymd, days) {
        var parts = String(ymd || '').split('-');
        if (parts.length !== 3) return '';
        var date = new Date(Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2])));
        if (isNaN(date.getTime())) return '';
        date.setUTCDate(date.getUTCDate() + Number(days || 0));
        return date.getUTCFullYear() + '-' + pad2(date.getUTCMonth() + 1) + '-' + pad2(date.getUTCDate());
    }

    function chinaWeekBounds(ymd) {
        var key = ymd || getChinaYmd();
        var parts = String(key).split('-');
        if (parts.length !== 3) return { startYmd: '', endYmd: '' };
        var date = new Date(Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2])));
        if (isNaN(date.getTime())) return { startYmd: '', endYmd: '' };
        var day = date.getUTCDay();
        var mondayOffset = day === 0 ? -6 : 1 - day;
        var monday = new Date(date);
        monday.setUTCDate(date.getUTCDate() + mondayOffset);
        var sunday = new Date(monday);
        sunday.setUTCDate(monday.getUTCDate() + 6);
        return {
            startYmd: monday.getUTCFullYear() + '-' + pad2(monday.getUTCMonth() + 1) + '-' + pad2(monday.getUTCDate()),
            endYmd: sunday.getUTCFullYear() + '-' + pad2(sunday.getUTCMonth() + 1) + '-' + pad2(sunday.getUTCDate())
        };
    }

    function chinaMonthBounds(ymd) {
        var key = ymd || getChinaYmd();
        var parts = String(key).split('-');
        if (parts.length !== 3) return { startYmd: '', endYmd: '' };
        var y = Number(parts[0]);
        var m = Number(parts[1]);
        if (!y || !m) return { startYmd: '', endYmd: '' };
        var last = new Date(Date.UTC(y, m, 0));
        return {
            startYmd: y + '-' + pad2(m) + '-01',
            endYmd: last.getUTCFullYear() + '-' + pad2(last.getUTCMonth() + 1) + '-' + pad2(last.getUTCDate())
        };
    }

    function orderedYmdRange(startYmd, endYmd) {
        var start = startYmd || endYmd || '';
        var end = endYmd || startYmd || '';
        if (start && end && start > end) return { startYmd: end, endYmd: start };
        return { startYmd: start, endYmd: end };
    }

    function resolveActiveRange(preset, dayYmd, nowYmd, startYmd, endYmd) {
        var today = nowYmd || getChinaYmd();
        if (preset === 'yesterday') {
            var yesterday = shiftYmd(today, -1);
            return { startYmd: yesterday, endYmd: yesterday };
        }
        if (preset === 'week') return chinaWeekBounds(today);
        if (preset === 'month') return chinaMonthBounds(today);
        if (preset === 'range') return orderedYmdRange(startYmd, endYmd || today);
        if (preset === 'day') {
            var chosen = dayYmd || startYmd || today;
            return { startYmd: chosen, endYmd: chosen };
        }
        return { startYmd: today, endYmd: today };
    }

    function buildActiveStudentRows(students, sessions, testRecords, options) {
        options = options || {};
        var startYmd = options.startYmd || '';
        var endYmd = options.endYmd || startYmd;
        var dateKeyFn = typeof options.dateKey === 'function' ? options.dateKey : getChinaYmd;
        var sortDir = options.sortDir === 'asc' ? 1 : -1;

        function inRange(iso) {
            if (!iso) return false;
            var key = dateKeyFn(iso);
            if (!key) return false;
            if (startYmd && key < startYmd) return false;
            if (endYmd && key > endYmd) return false;
            return true;
        }

        var rows = [];
        (students || []).forEach(function(student) {
            var sid = student && student.student_id;
            if (!sid) return;
            var studentSessions = (sessions || []).filter(function(item) {
                return item && item.student_id === sid;
            });
            var studentRecords = (testRecords || []).filter(function(item) {
                return item && item.student_id === sid;
            });
            var seconds = sumPracticeSeconds(studentSessions, studentRecords, { createdAt: inRange });

            var count = 0;
            var latest = '';
            function consider(iso) {
                if (!inRange(iso)) return;
                count += 1;
                if (!latest || new Date(iso) > new Date(latest)) latest = iso;
            }
            filterTimedSessions(studentSessions).forEach(function(session) {
                consider(session.created_at || session.ended_at);
            });
            studentRecords.forEach(function(record) {
                if (resolveModuleType(record && record.module_type) === 'speaking') return;
                consider(record.created_at || record.ended_at);
            });

            rows.push({
                student_id: sid,
                student_name: student.name || sid,
                seconds: seconds,
                count: count,
                latest: latest
            });
        });

        rows.sort(function(a, b) {
            if (a.seconds !== b.seconds) return (a.seconds - b.seconds) * sortDir;
            return String(a.student_id).localeCompare(String(b.student_id));
        });
        return rows;
    }

    function createIdleClock(idleLimitMs, timeFn) {
        var limit = idleLimitMs == null ? IDLE_LIMIT_MS : idleLimitMs;
        var now = typeof timeFn === 'function' ? timeFn : function() { return Date.now(); };
        var accrued = 0;
        var runStart = null;
        var lastAct = null;
        var running = false;

        function closedRunEnd(t) {
            if (lastAct == null) return t;
            if (t - lastAct >= limit) return lastAct + limit;
            return t;
        }

        function touch() {
            var t = now();
            if (running && lastAct != null && t - lastAct >= limit) {
                accrued += Math.max(0, (lastAct + limit) - runStart);
                runStart = t;
            } else if (!running) {
                runStart = t;
                running = true;
            }
            lastAct = t;
        }

        function elapsedMs() {
            var t = now();
            var extra = 0;
            if (running && runStart != null) extra = Math.max(0, closedRunEnd(t) - runStart);
            return accrued + extra;
        }

        function elapsedSeconds() {
            return Math.max(0, Math.round(elapsedMs() / 1000));
        }

        function stop() {
            if (!running) return elapsedMs();
            accrued = elapsedMs();
            running = false;
            runStart = null;
            return accrued;
        }

        function reset() {
            accrued = 0;
            runStart = null;
            lastAct = null;
            running = false;
        }

        return {
            touch: touch,
            elapsedMs: elapsedMs,
            elapsedSeconds: elapsedSeconds,
            stop: stop,
            reset: reset
        };
    }

    function bindIdleClock(doc, clock) {
        if (!doc || !clock || typeof doc.addEventListener !== 'function') {
            return function() {};
        }
        var handler = function() { clock.touch(); };
        var events = ['pointerdown', 'keydown', 'click', 'touchstart', 'input', 'change', 'scroll', 'wheel'];
        events.forEach(function(ev) {
            doc.addEventListener(ev, handler, true);
        });
        var onVisible = function() {
            if (doc.visibilityState === 'visible') clock.touch();
        };
        doc.addEventListener('visibilitychange', onVisible);
        return function() {
            events.forEach(function(ev) {
                doc.removeEventListener(ev, handler, true);
            });
            doc.removeEventListener('visibilitychange', onVisible);
        };
    }

    function parseDetails(details) {
        if (Array.isArray(details)) return details;
        if (!details || typeof details !== 'string') return [];
        try {
            var parsed = JSON.parse(details);
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            return [];
        }
    }

    function getTestTypeLabel(testType) {
        if (testType === 'random') return '随机测试';
        if (testType === 'wrong_words') return '错题测试';
        if (testType === 'module_test') return '模块测试';
        return '测试记录';
    }

    function getWrongWordDetails(details) {
        return parseDetails(details).filter(function(item) {
            return item && item.isCorrect === false && typeof item.word === 'string' && item.word.trim();
        });
    }

    return {
        IDLE_LIMIT_MS: IDLE_LIMIT_MS,
        bindIdleClock: bindIdleClock,
        buildActiveStudentRows: buildActiveStudentRows,
        buildDailyPracticeRows: buildDailyPracticeRows,
        chinaMonthBounds: chinaMonthBounds,
        chinaWeekBounds: chinaWeekBounds,
        createIdleClock: createIdleClock,
        getChinaYmd: getChinaYmd,
        resolveActiveRange: resolveActiveRange,
        shiftYmd: shiftYmd,
        filterStudySessions: filterStudySessions,
        filterTimedSessions: filterTimedSessions,
        getTestTypeLabel: getTestTypeLabel,
        getWrongWordDetails: getWrongWordDetails,
        isStudySession: isStudySession,
        isTimedSession: isTimedSession,
        parseDetails: parseDetails,
        sumDuration: sumDuration,
        sumPracticeSeconds: sumPracticeSeconds
    };
});

var testSaveCache = {};

function getStudySaveKey(record) {
    return [
        record.student_id,
        record.module_type,
        record.session_kind,
        record.plan_item_id || '',
        Math.round((Number(record.duration_seconds) || 0) / 5) * 5,
        record.words_tested || 0,
        record.initial_correct || 0,
        record.score_percent || ''
    ].join('|');
}

function getTestSaveKey(record) {
    // 不把 duration 计入去重键：连点提交时秒数常差 1～几秒，分桶会导致重复写入
    return [
        record.student_id,
        record.module_type,
        record.test_type,
        record.score,
        record.correct_count,
        record.total_count
    ].join('|');
}

async function saveStudySession(payload) {
    const studentId = payload.student_id || (currentStudent && currentStudent.student_id);
    if (!studentId) return { skipped: true, reason: 'student_missing' };
    const moduleType = normalizeModuleType(payload.moduleType || payload.module_type || (window._currentModule && window._currentModule.id));
    const module = getModuleById(moduleType);
    const duration = Math.max(0, Math.round(Number(payload.durationSeconds || payload.duration_seconds || 0)));
    const sessionKind = payload.sessionKind || payload.session_kind || 'study';
    const practicedItems = Number(payload.wordsTested || payload.words_tested || payload.totalCount || payload.totalWords || payload.total_count || 0);
    if (duration <= 0 && practicedItems <= 0 && sessionKind !== 'test') return { skipped: true, reason: 'empty_duration' };
    // 与退出兜底一致：无有效练习且不足 3 秒不记，避免“打开即学习”
    if (sessionKind !== 'test' && moduleType !== 'speaking' && duration < 3 && practicedItems <= 0) {
        return { skipped: true, reason: 'too_short' };
    }

    const nowIso = new Date().toISOString();
    const taskCtx = window._currentTaskContext || {};
    const taskMod = window._currentModule || {};
    const planItemId = payload.plan_item_id != null ? payload.plan_item_id
        : (payload.planItemId != null ? payload.planItemId
            : (taskMod.plan_item_id != null ? taskMod.plan_item_id : taskCtx.plan_item_id));
    const unitId = payload.unit_id || payload.unitId || taskMod.unit_id || taskCtx.unit_id;
    const record = {
        student_id: studentId,
        module_type: moduleType,
        module_name: payload.moduleName || payload.module_name || (module ? module.name : moduleType),
        session_kind: sessionKind,
        words_tested: Number(payload.wordsTested || payload.words_tested || payload.totalCount || payload.totalWords || payload.total_count || 0),
        initial_correct: Number(payload.initialCorrect || payload.initial_correct || payload.rightCount || payload.totalCorrect || payload.correctCount || payload.correct_count || 0),
        initial_wrong: Number(payload.initialWrong || payload.initial_wrong || payload.wrongCount || payload.wrong_count || 0),
        groups_completed: Number(payload.completedGroups || payload.groups_completed || 0),
        score_percent: payload.scorePercent != null ? Number(payload.scorePercent) : (payload.score != null ? Number(payload.score) : null),
        duration_seconds: duration,
        details: payload.details || [],
        started_at: payload.startedAt || payload.started_at || null,
        ended_at: payload.endedAt || payload.ended_at || nowIso,
        created_at: nowIso
    };
    if (planItemId != null && planItemId !== '') record.plan_item_id = Number(planItemId);
    if (unitId) record.unit_id = String(unitId);

    const cacheKey = getStudySaveKey(record);
    const cacheTime = studySaveCache[cacheKey];
    if (cacheTime && Date.now() - cacheTime < 3000) {
        return { skipped: true, reason: 'duplicate' };
    }
    studySaveCache[cacheKey] = Date.now();

    const result = await apiFetch('/api/student/study-sessions', {
        method: 'POST',
        body: JSON.stringify(record)
    });
    if (!result.error && window._currentModule && normalizeModuleType(window._currentModule.id) === moduleType) {
        window._currentModule.reported = true;
    }
    return result;
}

async function saveModuleTestRecord(payload) {
    const studentId = payload.student_id || (currentStudent && currentStudent.student_id);
    if (!studentId) return { skipped: true, reason: 'student_missing' };
    const moduleType = normalizeModuleType(payload.moduleType || payload.module_type || (window._currentModule && window._currentModule.id) || 'dictation');
    const module = getModuleById(moduleType);
    const totalCount = Number(payload.totalCount || payload.total_count || 0);
    const correctCount = Number(payload.correctCount || payload.correct_count || payload.rightCount || payload.right_count || 0);
    const score = payload.scorePercent != null
        ? Number(payload.scorePercent)
        : (payload.score_percent != null ? Number(payload.score_percent) : (payload.score != null ? Number(payload.score) : (totalCount > 0 ? Math.round(correctCount / totalCount * 100) : 0)));
    const threshold = payload.passThreshold != null ? Number(payload.passThreshold) : (payload.pass_threshold != null ? Number(payload.pass_threshold) : await getPassThreshold(moduleType, currentStudent));
    const duration = Math.max(0, Math.round(Number(payload.durationSeconds || payload.duration_seconds || 0)));
    const isPassed = payload.isPassed != null ? !!payload.isPassed : (payload.is_passed != null ? !!payload.is_passed : score >= threshold);
    const nowIso = new Date().toISOString();
    const record = {
        student_id: studentId,
        module_type: moduleType,
        module_name: payload.moduleName || payload.module_name || (module ? module.name : moduleType),
        test_type: payload.testType || payload.test_type || 'module_test',
        score: score,
        correct_count: correctCount,
        total_count: totalCount,
        is_passed: isPassed,
        pass_threshold: threshold,
        duration_seconds: duration,
        started_at: payload.startedAt || payload.started_at || null,
        ended_at: payload.endedAt || payload.ended_at || nowIso,
        details: payload.details || []
    };
    const cacheKey = getTestSaveKey(record);
    const cacheTime = testSaveCache[cacheKey];
    if (cacheTime && Date.now() - cacheTime < 15000) {
        return { skipped: true, reason: 'duplicate' };
    }
    testSaveCache[cacheKey] = Date.now();
    const result = await apiFetch('/api/student/test-records', {
        method: 'POST',
        body: JSON.stringify(record)
    });
    if (result.error) delete testSaveCache[cacheKey];
    if (!result.error) {
        if (window._currentModule && normalizeModuleType(window._currentModule.id) === moduleType) {
            window._currentModule.reported = true;
        }
    }
    return result;
}
