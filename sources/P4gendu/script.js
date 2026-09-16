const defaultLessons = Array.isArray(window.GENDU_LESSONS) ? window.GENDU_LESSONS : [];

const elements = {
    p1List: document.getElementById('p1List'),
    p4List: document.getElementById('p4List')
};

function queryParam(name) {
    try {
        return new URLSearchParams(window.location.search).get(name);
    } catch (e) {
        return null;
    }
}

function isTaskMode() {
    return !!(queryParam('plan_item_id') || queryParam('unit_id'));
}

function isTestMode() {
    return (queryParam('mode') || '') === 'test';
}

function passThreshold() {
    const raw = Number(queryParam('pass_threshold'));
    return isFinite(raw) && raw > 0 ? raw : 70;
}

function lessonsByPart(part) {
    return defaultLessons.filter(function (item) {
        return item.part === part;
    });
}

function findLesson(raw) {
    if (raw == null || raw === '') return null;
    const value = String(raw).trim();
    if (value === '1') {
        return defaultLessons.find(function (item) {
            return item.code === 'C4T1S4';
        }) || defaultLessons[0] || null;
    }
    return defaultLessons.find(function (item) {
        return item.code === value || String(item.id) === value;
    }) || null;
}

function buildTestUrl(lesson) {
    const url = new URL('../P4genduceshi/index.html', window.location.href);
    try {
        const current = new URLSearchParams(window.location.search);
        current.forEach(function (value, key) {
            if (key === 'v') return;
            url.searchParams.set(key, value);
        });
    } catch (e) {}
    url.searchParams.set('lessonId', lesson.code);
    url.searchParams.set('part', lesson.part || '');
    url.searchParams.set('v', '20260904g');
    return url.href;
}

function openLesson(lesson) {
    if (!lesson) return;
    window.location.href = buildTestUrl(lesson);
}

function createLessonItem(lesson) {
    const item = document.createElement('a');
    item.className = 'lesson-item';
    item.href = buildTestUrl(lesson);
    item.dataset.code = lesson.code;

    const summary = document.createElement('div');
    const title = document.createElement('div');
    title.className = 'lesson-title';
    title.textContent = lesson.title;
    const duration = document.createElement('div');
    duration.className = 'lesson-duration';
    duration.textContent = lesson.duration || '';
    summary.append(title, duration);
    item.appendChild(summary);
    return item;
}

function renderHub() {
    if (!elements.p1List || !elements.p4List) return;
    const p1Block = document.getElementById('p1Block');
    const title = document.querySelector('header h1');
    const sub = document.querySelector('header .subtitle');
    const p4Desc = document.getElementById('p4Desc');
    if (isTestMode()) {
        if (p1Block) p1Block.style.display = 'none';
        if (title) title.textContent = 'P4 跟读测试';
        if (sub) sub.textContent = '选一篇 Part 4 讲座跟读，识别率达到 ' + passThreshold() + '% 即计入测试进度';
        if (p4Desc) p4Desc.textContent = '测试只计 P4 讲座。跟读识别率 ≥ ' + passThreshold() + '% 为达标。';
        document.title = 'P4 跟读测试';
    }
    elements.p1List.replaceChildren();
    elements.p4List.replaceChildren();
    if (!isTestMode()) {
        lessonsByPart('p1').forEach(function (lesson) {
            elements.p1List.appendChild(createLessonItem(lesson));
        });
    }
    lessonsByPart('p4').forEach(function (lesson) {
        elements.p4List.appendChild(createLessonItem(lesson));
    });
}

function init() {
    renderHub();

    const requested = findLesson(queryParam('lessonId') || queryParam('code'));
    if (requested) {
        if (isTestMode() && requested.part !== 'p4') {
            return;
        }
        openLesson(requested);
        return;
    }
    if (isTaskMode()) {
        const part = (queryParam('part') || '').toLowerCase();
        const first = (part === 'p1' || part === 'p4') ? lessonsByPart(part)[0] : defaultLessons[0];
        if (first) openLesson(first);
    }
}

document.addEventListener('DOMContentLoaded', init);
