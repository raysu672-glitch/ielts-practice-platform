/**
 * 口语复合句今日任务：把「一句三步都通过」收成服务端 scope。
 *
 * 页面只在带 plan_item_id 的任务深链里上报。自由练没有该参数，不打勾。
 * 跟读 / 脱口而出被跳过、或逐词比对未通过，都不算这一句完成。
 * 本文件不读 localStorage，方便单测；页面负责判断某一句是否三步通过。
 */
(function (root) {
    function parseComplexTaskQuery(search) {
        var params = new URLSearchParams(String(search || '').replace(/^\?/, ''));
        var kind = params.get('kind') || '';
        var id = params.get('id') || '';
        var planRaw = params.get('plan_item_id');
        var planItemId = planRaw != null && String(planRaw).trim() !== '' ? Number(planRaw) : NaN;
        var kindOk = kind === 'pattern' || kind === 'adv';
        var active = kindOk && !!id && !isNaN(planItemId) && planItemId > 0;
        return {
            active: active,
            kind: kind === 'adv' ? 'adv' : 'pattern',
            id: id,
            planItemId: active ? planItemId : null,
            unitId: params.get('unit_id') || '',
            contentVersion: params.get('content_version') || '1'
        };
    }

    function isSentenceFullyDone(progress) {
        return !!(progress && progress.a && progress.sh && progress.sp);
    }

    /**
     * previousKeys: 本次页面已经上报过的句号（字符串）。
     * fullyDone 为真且句号是新的时，追加一条 scope_key。
     * 凑满 total（目录 scope_total，默认 10）才附带打勾消息。
     */
    function scopeReportForSentence(previousKeys, sentenceIndex, fullyDone, total) {
        var keys = (previousKeys || []).map(function (k) { return String(k); });
        var seen = {};
        keys.forEach(function (k) { if (k) seen[k] = true; });
        keys = keys.filter(function (k) { return !!k; });
        var idx = String(sentenceIndex);
        var added = false;
        if (fullyDone && idx && !seen[idx]) {
            keys.push(idx);
            seen[idx] = true;
            added = true;
        }
        var need = Number(total) > 0 ? Number(total) : 10;
        return {
            keys: keys,
            added: added,
            scopeDone: keys.length,
            scopeTotal: need,
            complete: keys.length >= need
        };
    }

    function buildTaskMessages(task, report) {
        if (!task || !task.active || !report || !report.added) return [];
        var lastKey = report.keys[report.keys.length - 1];
        var out = [{
            type: 'taskScopeProgress',
            plan_item_id: task.planItemId,
            unit_id: task.unitId || '',
            content_version: task.contentVersion || '1',
            scope_key: lastKey
        }];
        if (report.complete) {
            out.push({
                type: 'taskUnitComplete',
                plan_item_id: task.planItemId,
                unit_id: task.unitId || '',
                content_version: task.contentVersion || '1',
                scope_done: report.scopeTotal
            });
        }
        return out;
    }

    /**
     * 本机已经三步通过的句号一次性提交（学生点按钮，不在打开页面时自动打勾）。
     * indexes 只应包含调用方已确认 a/sh/sp 都为真的句号。
     */
    function messagesForDoneIndexes(task, indexes, total) {
        if (!task || !task.active) return [];
        var need = Number(total) > 0 ? Number(total) : 10;
        var seen = {};
        var keys = [];
        (indexes || []).forEach(function (raw) {
            var key = String(raw);
            if (!key || seen[key]) return;
            seen[key] = true;
            keys.push(key);
        });
        var out = keys.map(function (key) {
            return {
                type: 'taskScopeProgress',
                plan_item_id: task.planItemId,
                unit_id: task.unitId || '',
                content_version: task.contentVersion || '1',
                scope_key: key
            };
        });
        if (keys.length >= need) {
            out.push({
                type: 'taskUnitComplete',
                plan_item_id: task.planItemId,
                unit_id: task.unitId || '',
                content_version: task.contentVersion || '1',
                scope_done: need
            });
        }
        return out;
    }

    var api = {
        parseComplexTaskQuery: parseComplexTaskQuery,
        isSentenceFullyDone: isSentenceFullyDone,
        scopeReportForSentence: scopeReportForSentence,
        buildTaskMessages: buildTaskMessages,
        messagesForDoneIndexes: messagesForDoneIndexes
    };
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
    root.ComplexTask = api;
})(typeof window !== 'undefined' ? window : globalThis);
