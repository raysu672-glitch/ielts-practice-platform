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
