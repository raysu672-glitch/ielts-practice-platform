// 学习/测试追踪工具与保存
(function(root, factory) {
    var api = factory();
    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }
    root.TrackingUtils = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
    function isStudySession(session) {
        var kind = session && session.session_kind;
        return !kind || kind === 'study';
    }

    function filterStudySessions(sessions) {
        return (sessions || []).filter(isStudySession);
    }

    function sumDuration(sessions) {
        return (sessions || []).reduce(function(sum, session) {
            return sum + Math.max(0, Number(session && session.duration_seconds) || 0);
        }, 0);
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
        filterStudySessions: filterStudySessions,
        getTestTypeLabel: getTestTypeLabel,
        getWrongWordDetails: getWrongWordDetails,
        isStudySession: isStudySession,
        parseDetails: parseDetails,
        sumDuration: sumDuration
    };
});

var testSaveCache = {};

function getStudySaveKey(record) {
    return [
        record.student_id,
        record.module_type,
        record.session_kind,
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
    if (!db) return { skipped: true, reason: 'db_missing' };
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

    const cacheKey = getStudySaveKey(record);
    const cacheTime = studySaveCache[cacheKey];
    if (cacheTime && Date.now() - cacheTime < 3000) {
        return { skipped: true, reason: 'duplicate' };
    }
    studySaveCache[cacheKey] = Date.now();

    const result = await db.from('study_sessions').insert(record);
    if (!result.error && window._currentModule && normalizeModuleType(window._currentModule.id) === moduleType) {
        window._currentModule.reported = true;
    }
    return result;
}

async function saveModuleTestRecord(payload) {
    if (!db) return { skipped: true, reason: 'db_missing' };
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
    const result = await db.from('test_records').insert(record);
    if (result.error) delete testSaveCache[cacheKey];
    if (!result.error) {
        if (window._currentModule && normalizeModuleType(window._currentModule.id) === moduleType) {
            window._currentModule.reported = true;
        }
    }
    return result;
}
