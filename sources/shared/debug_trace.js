/* Student debug trace. Not shown on the teacher timeline.
   Records clicks, field changes, errors and page lifetime, then posts them
   to /api/debug/trace. Password values are never sent. */
(function () {
    if (window.__ieltsDebugTrace) return;
    window.__ieltsDebugTrace = true;

    var KEY = 'ielts_debug_trace_v1';
    var MAX = 200;
    var queue = [];
    try {
        var saved = JSON.parse(sessionStorage.getItem(KEY) || '[]');
        if (Array.isArray(saved)) queue = saved;
    } catch (e) {}

    function clip(value, limit) {
        var text = String(value == null ? '' : value).replace(/\s+/g, ' ').trim();
        return text.length > limit ? text.slice(0, limit) : text;
    }

    function isSecret(el) {
        if (!el) return false;
        var type = String(el.type || '').toLowerCase();
        var hint = (String(el.id || '') + ' ' + String(el.name || '') + ' ' +
            String(el.placeholder || '') + ' ' + String(el.getAttribute && el.getAttribute('aria-label') || '')).toLowerCase();
        return type === 'password' || hint.indexOf('password') >= 0 || hint.indexOf('密码') >= 0;
    }

    function describe(el) {
        if (!el || !el.tagName) return '';
        var tag = String(el.tagName).toLowerCase();
        var id = el.id ? ('#' + el.id) : '';
        var text = '';
        if (!isSecret(el)) {
            text = clip(el.getAttribute && (el.getAttribute('aria-label') || el.getAttribute('title')) || el.innerText || '', 60);
        }
        return clip(tag + id + (text ? (' ' + text) : ''), 160);
    }

    function persist() {
        try { sessionStorage.setItem(KEY, JSON.stringify(queue)); } catch (e) {}
    }

    var timer = null;
    function schedule() {
        if (timer) return;
        timer = setTimeout(flush, 1200);
    }

    function push(action, detail) {
        detail = detail || {};
        queue.push({
            t: new Date().toISOString(),
            action: action,
            page: clip(location.pathname + location.search, 240),
            target: clip(detail.target || '', 160),
            detail: detail
        });
        if (queue.length > MAX) queue = queue.slice(queue.length - MAX);
        persist();
        schedule();
    }

    function flush() {
        timer = null;
        if (!queue.length) return;
        var batch = queue.slice(0, 40);
        fetch('/api/debug/trace', {
            method: 'POST',
            credentials: 'include',
            keepalive: true,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: batch })
        }).then(function (res) {
            if (res.status === 401 || res.status === 403) return;
            if (!res.ok) return;
            queue = queue.slice(batch.length);
            persist();
            if (queue.length) schedule();
        }).catch(function () {});
    }

    document.addEventListener('click', function (ev) {
        var el = ev.target;
        if (el && el.closest) {
            el = el.closest('button, a, [role="button"], input, label, summary') || el;
        }
        push('click', { target: describe(el) });
    }, true);

    document.addEventListener('change', function (ev) {
        var el = ev.target;
        if (isSecret(el)) {
            push('input', { target: describe(el), secret: true });
            return;
        }
        var value = el && 'value' in el ? clip(el.value, 80) : '';
        push('change', { target: describe(el), value: value });
    }, true);

    document.addEventListener('submit', function (ev) {
        push('submit', { target: describe(ev.target) });
    }, true);

    window.addEventListener('error', function (ev) {
        push('js_error', {
            message: clip(ev.message, 200),
            source: clip(ev.filename, 120),
            line: ev.lineno || 0
        });
    });

    window.addEventListener('unhandledrejection', function (ev) {
        var reason = ev.reason;
        var message = reason && reason.message ? reason.message : reason;
        push('js_error', { message: clip(message, 200), kind: 'rejection' });
    });

    document.addEventListener('visibilitychange', function () {
        push('visibility', { state: document.visibilityState });
    });

    window.addEventListener('pagehide', function () {
        push('pagehide', {});
        flush();
    });

    push('page', { title: clip(document.title, 80) });
    window.__ieltsDebugTracePush = push;
})();
