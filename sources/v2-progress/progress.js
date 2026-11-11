(function () {
    'use strict';

    var Model = window.V2ProgressModel;
    var Demo = window.V2ProgressDemo;
    var POLL_MS = 15000;
    var API = '/api/v2/progress/me';
    var TZ = 'Asia/Shanghai';

    var params = new URLSearchParams(window.location.search);
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var state = {
        mode: params.has('demo') ? 'demo' : 'live',
        raw: null,
        view: null,
        selectedSubject: null,
        selectedStage: null,
        selectedUnit: null,
        lastOkAt: null,
        pollTimer: null,
        loading: false,
        demoStart: null,
        demoNow: null
    };

    var $ = function (id) { return document.getElementById(id); };

    function esc(s) {
        return String(s === null || s === undefined ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    var timeFmt = new Intl.DateTimeFormat('zh-CN', { timeZone: TZ, hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    var dateFmt = new Intl.DateTimeFormat('zh-CN', { timeZone: TZ, month: 'numeric', day: 'numeric' });
    function fmtTime(ms) { return timeFmt.format(new Date(ms)); }
    function fmtDate(ms) { return ms === null || ms === undefined ? '—' : dateFmt.format(new Date(ms)); }
    // Floor so a value just under a threshold never displays as the threshold itself.
    function pct(v) { return Math.floor(v * 100 + 1e-9) + '%'; }

    function masteryWord(state) {
        return { strong: '掌握牢固', fading: '开始褪色', review: '需要复测', none: '—' }[state] || '—';
    }

    // —— 数据获取 ——

    function setStatus() {
        var el = $('status');
        if (state.mode === 'demo') {
            el.innerHTML = '<span class="dot demo"></span>数据来源：示例数据（交互演示）';
            return;
        }
        if (!state.lastOkAt) { el.textContent = '正在读取…'; return; }
        var stale = !!$('errorNotice').textContent && !$('errorNotice').hidden;
        el.innerHTML = '<span class="dot' + (stale ? ' stale' : '') + '"></span>' +
            '数据来源：平台数据库（原系统计划清单 + 阶段测记录）· 最近更新 ' +
            esc(fmtTime(state.lastOkAt)) + '（北京时间）· 每 15 秒自动查询，不是推送';
    }

    function showState(kind, detail) {
        var el = $('stateView');
        ['hero', 'subjects', 'detail', 'review', 'justNow'].forEach(function (id) { $(id).hidden = true; });
        el.hidden = false;
        if (kind === 'loading') {
            el.innerHTML = '<h2>正在读取你的计划清单…</h2><div class="loading-line"></div>';
        } else if (kind === 'login') {
            el.innerHTML = '<h2>需要先登录学生端</h2>' +
                '<p>这张路线图读取的是你在学习平台里的计划清单和测试记录，登录后会自动显示。</p>' +
                '<div class="actions"><a class="btn-act" href="/tinglidanciceshi/">去学生端登录</a>' +
                '<a class="btn-quiet" href="?demo=1">先看交互演示（示例数据）</a></div>';
        } else if (kind === 'empty') {
            el.innerHTML = '<h2>还没有计划清单</h2>' +
                '<p>总路线就是助教给你排的计划清单。助教排好后，这里会出现你的路线，不需要你做任何设置。</p>' +
                (detail ? '<p>' + esc(detail) + '</p>' : '') +
                '<div class="actions"><a class="btn-quiet" href="?demo=1">看交互演示（示例数据）</a></div>';
        } else if (kind === 'error') {
            el.innerHTML = '<h2>暂时读不到进度</h2><p>' + esc(detail || '') + '</p>' +
                '<div class="actions"><button type="button" class="btn-act" id="retryBtn">重试</button>' +
                '<a class="btn-quiet" href="?demo=1">看交互演示（示例数据）</a></div>';
            $('retryBtn').addEventListener('click', function () { loadLive(); });
        }
    }

    function showError(msg) {
        var el = $('errorNotice');
        if (!msg) { el.hidden = true; el.textContent = ''; setStatus(); return; }
        el.hidden = false;
        el.innerHTML = '<strong>更新失败</strong>' + esc(msg) +
            (state.lastOkAt ? '。仍显示 ' + esc(fmtTime(state.lastOkAt)) + ' 的数据。' : '') +
            '<button type="button" class="btn-quiet" id="errorRetry">重试</button>';
        $('errorRetry').addEventListener('click', function () { loadLive(); });
        setStatus();
    }

    function schedulePoll() {
        clearTimeout(state.pollTimer);
        if (state.mode !== 'live') return;
        state.pollTimer = setTimeout(function () {
            if (document.visibilityState === 'visible') loadLive();
            else schedulePoll();
        }, POLL_MS);
    }

    function loadLive() {
        if (state.loading) return;
        state.loading = true;
        if (!state.view) showState('loading');
        fetch(API, { credentials: 'same-origin', cache: 'no-store' })
            .then(function (res) {
                if (res.status === 401) { var e = new Error('login'); e.login = true; throw e; }
                return res.json().then(function (body) {
                    if (!res.ok || body.error) throw new Error((body.error && body.error.message) || ('HTTP ' + res.status));
                    return body.data;
                });
            })
            .then(function (raw) {
                state.lastOkAt = Date.now();
                showError(null);
                accept(raw, Date.now(), null);
            })
            .catch(function (err) {
                if (err.login) {
                    state.view = null;
                    showState('login');
                    setStatus();
                    $('status').textContent = '未登录';
                    return;
                }
                var msg = err && err.message ? err.message : '网络错误';
                if (state.view) showError(msg);
                else showState('error', msg);
            })
            .then(function () {
                state.loading = false;
                schedulePoll();
            });
    }

    // —— 数据进入 → 推导 → 对比 → 渲染 ——

    function planStoreKey(view) { return 'v2progress.plan.' + (view.student.id || 'unknown'); }

    function accept(raw, nowMs, event) {
        var prev = state.view;
        var prevRaw = state.raw;
        var view = Model.build(raw, nowMs);
        state.raw = raw;
        state.view = view;

        if (!view.units.length) {
            showState('empty', raw.plan_meta && raw.plan_meta.draft_pending
                ? '助教已保存一份新清单，' + (raw.plan_meta.draft_effective_from || '') + ' 起生效。'
                : '');
            setStatus();
            return;
        }
        $('stateView').hidden = true;

        var changes = Model.diff(prev, view);
        if (!prev && state.mode === 'live') changes.plan = storedPlanChange(view);
        rememberPlan(view);
        var attemptsNew = newAttempts(prevRaw, raw);

        if (state.selectedSubject && !view.subjects.some(function (s) { return s.moduleType === state.selectedSubject; })) {
            state.selectedSubject = null; state.selectedStage = null; state.selectedUnit = null;
        }
        if (state.selectedUnit && !view.unitById[state.selectedUnit]) state.selectedUnit = null;

        render(prev, changes, attemptsNew, event);
    }

    function storedPlanChange(view) {
        if (state.mode !== 'live') return null;
        try {
            var stored = JSON.parse(window.localStorage.getItem(planStoreKey(view)) || 'null');
            if (!stored || !stored.length) return null;
            if (stored.slice().sort().join('|') === view.planSignature) return null;
            return Model.planChange(stored, view);
        } catch (e) { return null; }
    }

    function rememberPlan(view) {
        if (state.mode !== 'live') return;
        try {
            window.localStorage.setItem(planStoreKey(view), JSON.stringify(view.units.map(function (u) { return u.unitId; })));
        } catch (e) { /* 隐私模式下无法记住清单，下次只是不提示变化 */ }
    }

    function newAttempts(prevRaw, raw) {
        if (!prevRaw) return [];
        var seen = {};
        (prevRaw.test_attempts || []).forEach(function (a) { seen[a.id] = true; });
        return (raw.test_attempts || []).filter(function (a) { return !seen[a.id]; });
    }

    // —— 渲染 ——

    function render(prev, changes, attemptsNew, event) {
        var view = state.view;
        ['hero', 'subjects', 'review'].forEach(function (id) { $(id).hidden = false; });
        renderHero(prev, changes);
        renderSubjects(changes);
        renderDetail(changes);
        renderReview();
        renderJustNow(changes, attemptsNew, event);
        renderPlanNotice(changes.plan);
        if (state.mode === 'demo') renderDemoClock();
        setStatus();
        requestAnimationFrame(placePin);
        $('review').hidden = !view.reviewQueue.length;
    }

    function cellClasses(u, changes) {
        var cls = ['cell', u.route === 'passed' ? 'passed' : u.route === 'pending' ? 'pending' : 'open'];
        if (u.route === 'open' && u.studied) cls.push('studied');
        var ms = state.view.nextMilestone;
        if (ms && ms.nextUnitId === u.unitId) cls.push('next');
        if (!reduceMotion && changes && changes.passed.indexOf(u.unitId) >= 0) cls.push('just-passed');
        return cls.join(' ');
    }

    function masteryClasses(u, changes) {
        var cls = ['cell'];
        if (u.route === 'passed' && u.mastery.state !== 'none') cls.push('m-' + u.mastery.state);
        if (!reduceMotion && changes) {
            if (changes.dropped.indexOf(u.unitId) >= 0) cls.push('just-dropped');
            if (changes.restored.indexOf(u.unitId) >= 0) cls.push('just-restored');
        }
        return cls.join(' ');
    }

    function renderHero(prev, changes) {
        var view = state.view;
        var r = view.route;
        $('countTotal').textContent = r.total;
        var from = prev ? prev.route.passed : r.passed;
        animateNumber($('countPassed'), from, r.passed);

        var sub = [];
        sub.push('还剩 ' + r.remaining + ' 关');
        if (r.pending) sub.push('<span class="pending">另有 ' + r.pending + ' 关旧阶段测已达标，折算待定，暂不计入</span>');
        if (r.studiedOnly) sub.push(r.studiedOnly + ' 关已学完但还没测过（不计）');
        $('countSub').innerHTML = sub.join(' · ');

        var segHtml = view.subjects.map(function (s) {
            var track = '';
            var mastery = '';
            s.units.forEach(function (u, i) {
                var next = s.units[i + 1];
                var stageEnd = next && next.stageKey !== u.stageKey ? ' stage-end' : '';
                track += '<span class="' + cellClasses(u, changes) + stageEnd + '" data-unit="' + esc(u.unitId) + '" title="' + esc(u.title) + '"></span>';
                mastery += '<span class="' + masteryClasses(u, changes) + stageEnd + '" data-munit="' + esc(u.unitId) + '"></span>';
            });
            return '<div class="seg" style="flex:' + s.units.length + ' 1 0">' +
                '<button type="button" class="seg-name" data-subject="' + esc(s.moduleType) + '" title="' + esc(s.name) + '">' + esc(s.name) + ' ' + s.passed + '/' + s.total + '</button>' +
                '<div class="seg-track">' + track + '</div>' +
                '<div class="seg-mastery">' + mastery + '</div></div>';
        }).join('');
        var segs = $('routeSegments');
        segs.innerHTML = segHtml;
        var ms = view.nextMilestone;
        segs.setAttribute('aria-label', '总路线共 ' + r.total + ' 关：已过关 ' + r.passed + ' 关，折算待定 ' + r.pending +
            ' 关，未过关 ' + (r.total - r.passed - r.pending) + ' 关。' + (ms ? '下一关：' + ms.subjectName + ' ' + ms.nextUnitTitle + '。' : ''));
        segs.querySelectorAll('.seg-name').forEach(function (b) {
            b.addEventListener('click', function () { selectSubject(b.getAttribute('data-subject'), null, null, true); });
        });

        renderMilestone(ms, changes);
    }

    function renderMilestone(ms, changes) {
        var el = $('milestone');
        if (!ms) {
            el.innerHTML = '<div class="ms-label">下一个里程碑</div><div class="ms-main">计划清单全部过关</div>' +
                '<p class="ms-sub">接下来是保持掌握度：留意需要复测的单元。</p>';
            return;
        }
        var main = ms.subjectName + ' · ' + ms.stageLabel;
        var subLine = ms.stagePassed
            ? '已过 ' + ms.stagePassed + '/' + ms.stageTotal + '，还差 ' + ms.remaining + ' 关完成本段'
            : '本段共 ' + ms.stageTotal + ' 关，还没开始';
        var warn = '';
        if (ms.multiUnitTest) warn = '这一关没有单独的单元测试，只有阶段测「' + ms.testTitle + '」一次覆盖 ' + ms.stageTotal + ' 个单元；达标后能否算作单元过关尚未定。';
        else if (ms.noTest) warn = '这一关还没有安排任何测试，没有测试就无法过关。';
        el.innerHTML = '<div class="ms-label">下一个里程碑</div>' +
            '<div class="ms-main">' + esc(main) + '</div>' +
            '<p class="ms-sub">' + esc(subLine) + '</p>' +
            (ms.nextUnitTitle ? '<p class="ms-sub">下一关：' + esc(ms.nextUnitTitle) + '</p>' : '') +
            (warn ? '<p class="ms-warn">' + esc(warn) + '</p>' : '');
        if (!reduceMotion && changes && (changes.passed.length || changes.pending.length)) {
            el.classList.remove('updated');
            void el.offsetWidth;
            setTimeout(function () { el.classList.add('updated'); }, 900);
        }
    }

    function placePin() {
        var pin = $('routePin');
        var ms = state.view && state.view.nextMilestone;
        var cell = ms && ms.nextUnitId ? document.querySelector('.seg-track [data-unit="' + cssEscape(ms.nextUnitId) + '"]') : null;
        if (!cell) { pin.hidden = true; return; }
        var body = pin.parentElement.getBoundingClientRect();
        var rect = cell.getBoundingClientRect();
        pin.hidden = false;
        pin.style.left = (rect.left - body.left + rect.width / 2) + 'px';
        pin.style.top = (rect.bottom - body.top + 16) + 'px';
    }

    function cssEscape(s) {
        return window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/"/g, '\\"');
    }

    function animateNumber(el, from, to) {
        if (reduceMotion || from === to) { el.textContent = to; return; }
        el.textContent = from;
        var start = null;
        var dur = 700;
        setTimeout(function () {
            function step(ts) {
                if (start === null) start = ts;
                var k = Math.min(1, (ts - start) / dur);
                el.textContent = Math.round(from + (to - from) * k);
                if (k < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
        }, 1200);
    }

    function renderSubjects(changes) {
        var view = state.view;
        var html = view.subjects.map(function (s) {
            var current = s.currentStage;
            var strip = s.stages.map(function (st) {
                var pulse = !reduceMotion && changes && st.unitIds.some(function (id) {
                    return changes.passed.indexOf(id) >= 0 || changes.pending.indexOf(id) >= 0;
                });
                var cells = st.unitIds.map(function (id) {
                    var u = view.unitById[id];
                    return '<span class="cell ' + (u.route === 'passed' ? 'passed' : u.route === 'pending' ? 'pending' : '') + '"></span>';
                }).join('');
                return '<span class="stage-chunk' + (pulse ? ' pulse' : '') + '" data-stage="' + esc(st.key) + '" style="flex:' + st.total + ' 1 0">' + cells + '</span>';
            }).join('');
            var mastery;
            if (s.masteryAvg === null) mastery = '掌握度 —';
            else if (s.review) mastery = '<span class="m-review">' + s.review + ' 需复测</span>' + (s.fading ? ' · ' + s.fading + ' 褪色' : '');
            else if (s.fading) mastery = s.fading + ' 开始褪色';
            else mastery = '都牢固';
            var nowText = current ? '当前 ' + current.label + ' · ' + current.passed + '/' + current.total : '全部过关';
            return '<li><button type="button" class="subject-row" data-subject="' + esc(s.moduleType) + '"' +
                (state.selectedSubject === s.moduleType ? ' aria-current="true"' : '') + '>' +
                '<span class="subject-name">' + esc(s.name) + '<span class="subject-stage-now">' + esc(nowText) + '</span></span>' +
                '<span class="stage-strip" aria-hidden="true">' + strip + '</span>' +
                '<span class="subject-count">' + s.passed + '/' + s.total + ' 关' + (s.pending ? '<small>待定 ' + s.pending + '</small>' : '') + '</span>' +
                '<span class="subject-mastery">' + mastery + '</span>' +
                '</button></li>';
        }).join('');
        var list = $('subjectList');
        list.innerHTML = html;
        list.querySelectorAll('.subject-row').forEach(function (b) {
            b.addEventListener('click', function () { selectSubject(b.getAttribute('data-subject'), null, null, true); });
        });
    }

    function selectSubject(mt, stageKey, unitId, focus) {
        state.selectedSubject = mt;
        state.selectedStage = stageKey;
        state.selectedUnit = unitId;
        renderSubjects(null);
        renderDetail(null);
        if (focus) {
            var d = $('detail');
            d.focus({ preventScroll: true });
            d.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        }
    }

    function renderDetail(changes) {
        var view = state.view;
        var d = $('detail');
        var subj = view.subjects.filter(function (s) { return s.moduleType === state.selectedSubject; })[0];
        if (!subj) { d.hidden = true; return; }
        d.hidden = false;
        var stage = subj.stages.filter(function (s) { return s.key === state.selectedStage; })[0] || null;

        var crumbs = '<button type="button" data-crumb="route">总路线 ' + view.route.passed + '/' + view.route.total + '</button><span class="sep">›</span>';
        if (stage) {
            crumbs += '<button type="button" data-crumb="subject">' + esc(subj.name) + '</button><span class="sep">›</span>' +
                '<span aria-current="page">' + esc(stage.label) + '</span>';
        } else {
            crumbs += '<span aria-current="page">' + esc(subj.name) + '</span>';
        }
        $('crumbs').innerHTML = crumbs;
        $('crumbs').querySelectorAll('button').forEach(function (b) {
            b.addEventListener('click', function () {
                if (b.getAttribute('data-crumb') === 'route') {
                    state.selectedSubject = null; state.selectedStage = null; state.selectedUnit = null;
                    renderSubjects(null); renderDetail(null);
                    $('hero').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
                    var firstSeg = $('routeSegments').querySelector('.seg-name');
                    if (firstSeg) firstSeg.focus({ preventScroll: true });
                } else {
                    selectSubject(subj.moduleType, null, state.selectedUnit, false);
                }
            });
        });

        $('detailTitle').textContent = subj.name + ' · 已过 ' + subj.passed + '/' + subj.total + ' 关' + (subj.pending ? ' · 待定 ' + subj.pending : '');
        var nextId = view.nextMilestone && view.nextMilestone.nextUnitId;
        var stages = stage ? [stage] : subj.stages;
        var html = stages.map(function (st) {
            var missing = st.total - st.withUnitTest;
            var meta;
            if (st.noStageTest) {
                meta = !missing ? '每个单元单独测试'
                    : missing + ' 个单元还没有安排测试' + (st.withUnitTest ? '，其余单独测试' : '');
            } else {
                meta = '阶段测「' + st.testTitle + '」覆盖 ' + st.total + ' 个单元' +
                    (st.withUnitTest ? '；其中 ' + st.withUnitTest + ' 个另有单元测试' : '');
            }
            var flag = st.pending ? '阶段测已达标 · ' + st.pending + ' 个单元折算待定' : '';
            var stations = st.unitIds.map(function (id, i) {
                var u = view.unitById[id];
                var nextU = view.unitById[st.unitIds[i + 1]];
                var on = u.route === 'passed' && nextU && nextU.route === 'passed';
                var cls = ['station', u.route];
                if (u.route === 'passed' && u.mastery.state !== 'none') cls.push('m-' + u.mastery.state);
                if (u.unitId === nextId) cls.push('next');
                if (!reduceMotion && changes && changes.passed.indexOf(u.unitId) >= 0) cls.push('just-passed');
                var stText = u.unitId === nextId ? '下一关'
                    : u.route === 'passed' ? '已过 · ' + masteryWord(u.mastery.state)
                    : u.route === 'pending' ? '折算待定'
                    : u.studied ? '已学 · 未测' : '未过';
                return '<li class="' + (on ? 'on' : '') + '"><button type="button" class="' + cls.join(' ') + '" data-unit="' + esc(u.unitId) + '" aria-pressed="' + (state.selectedUnit === u.unitId) + '">' +
                    '<span class="node"><span class="ring"></span></span>' +
                    '<span class="st-title">' + esc(u.title) + '</span>' +
                    '<span class="st-state">' + esc(stText) + '</span></button></li>';
            }).join('');
            return '<div class="stage' + (stage ? ' focus' : '') + '">' +
                '<div class="stage-head"><h3>' + (stage ? esc(st.label) : '<button type="button" class="btn-quiet" data-stage="' + esc(st.key) + '">' + esc(st.label) + '</button>') + '</h3>' +
                '<span class="stage-meta">' + st.passed + '/' + st.total + ' 关 · ' + esc(meta) + '</span>' +
                (flag ? '<span class="stage-flag">' + esc(flag) + '</span>' : '') + '</div>' +
                '<ol class="stations">' + stations + '</ol></div>';
        }).join('');
        var list = $('stageList');
        list.innerHTML = html;
        list.querySelectorAll('[data-stage]').forEach(function (b) {
            b.addEventListener('click', function () { selectSubject(subj.moduleType, b.getAttribute('data-stage'), null, false); });
        });
        list.querySelectorAll('.station').forEach(function (b) {
            b.addEventListener('click', function () {
                state.selectedUnit = b.getAttribute('data-unit');
                list.querySelectorAll('.station').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
                renderUnitInfo();
            });
        });
        renderUnitInfo();
    }

    function renderUnitInfo() {
        var el = $('unitInfo');
        var u = state.selectedUnit && state.view.unitById[state.selectedUnit];
        if (!u) { el.hidden = true; return; }
        el.hidden = false;
        var M = Model.MASTERY;
        var html = '<h3>' + esc(u.title) + '</h3>';
        if (u.route === 'passed') {
            var m = u.mastery;
            var att = u.evidence.attempts.filter(function (a) { return a.passed; });
            var last = att[att.length - 1];
            html += '<p>已过关 · 证据：「' + esc(u.evidence.testTitle) + '」' +
                (last ? fmtDate(Date.parse(last.at)) + ' 达标（' + last.score + ' 分，达标线 ' + last.threshold + '）' : '') + '</p>';
            if (m.value === null) {
                html += '<p class="muted">' + esc(m.note || '暂无掌握度') + '</p>';
            } else {
                html += '<p>掌握度 <b>' + pct(m.value) + '</b> · ' + masteryWord(m.state) +
                    (m.retestFailed ? ' · 最近一次复测未过' : '') + '</p>' +
                    '<div class="meter" aria-hidden="true"><i class="' + (m.state === 'review' ? 'review' : '') + '" style="width:' + (m.value * 100).toFixed(1) + '%"></i>' +
                    '<span class="tick" style="left:' + (M.reviewBelow * 100) + '%"><span>80%</span></span>' +
                    '<span class="tick" style="left:' + (M.strongAt * 100) + '%"><span>90%</span></span></div>' +
                    '<p class="muted">' + (m.retestFailed || m.state === 'review'
                        ? '建议现在复测，通过后会重新描深。'
                        : '按暂定模型，约 ' + fmtDate(m.reviewAt) + ' 会降到 80% 以下，届时提示复测。') +
                    '路程不受影响。</p>';
            }
        } else if (u.route === 'pending') {
            html += '<p>旧阶段测「' + esc(u.evidence.testTitle) + '」' + (u.evidence.passedAt ? '于 ' + fmtDate(u.evidence.passedAt) + ' ' : '') +
                '已达标，这次测试覆盖 ' + u.evidence.coveredCount + ' 个单元。</p>' +
                '<p class="muted">一次测多个单元达标后，能否算作每个单元过关还没有定，所以暂不计入路程，也不计算掌握度。</p>';
        } else {
            html += u.studied ? '<p>已学完（打勾），但还没有测试达标，不计入路程。</p>' : '<p>还没过关。</p>';
            if (u.hasUnitTest) {
                html += '<p class="muted">先学还是先测都可以，过关只看这个单元的测试。</p>';
            } else if (u.stageTests && u.stageTests.length) {
                html += '<p class="muted">这个单元没有单独的测试，只有阶段测「' + esc(u.stageTests[0].title) +
                    '」一次覆盖 ' + u.stageTests[0].covered.length + ' 个单元；它达标后能否算作单元过关尚未定。</p>';
            } else {
                html += '<p class="muted">这个单元还没有安排任何测试，没有测试就无法过关。</p>';
            }
        }
        el.innerHTML = html;
    }

    function renderReview() {
        var q = state.view.reviewQueue;
        $('reviewList').innerHTML = q.map(function (u) {
            var m = u.mastery;
            return '<li><button type="button" data-subject="' + esc(u.moduleType) + '" data-unit="' + esc(u.unitId) + '">' +
                '<span class="r-title">' + esc(u.title) + '</span><br><span class="r-sub">' + esc(u.subjectName) +
                ' · 最近达标 ' + fmtDate(m.lastPassAt) + (m.retestFailed ? ' · 复测未过' : '') + '</span></button>' +
                '<span class="r-state ' + m.state + '">' + masteryWord(m.state) + '<br>掌握度 ' + pct(m.value) + '</span></li>';
        }).join('');
        $('reviewList').querySelectorAll('button').forEach(function (b) {
            b.addEventListener('click', function () {
                var u = state.view.unitById[b.getAttribute('data-unit')];
                selectSubject(u.moduleType, u.stageKey, u.unitId, true);
            });
        });
    }

    function stageOf(u) {
        var s = state.view.subjects.filter(function (x) { return x.moduleType === u.moduleType; })[0];
        return { subject: s, stage: s.stages.filter(function (x) { return x.key === u.stageKey; })[0] };
    }

    function renderJustNow(changes, attemptsNew, event) {
        var el = $('justNow');
        var view = state.view;
        var parts = [];
        changes.passed.forEach(function (id) {
            var u = view.unitById[id];
            var ctx = stageOf(u);
            parts.push('<b>' + esc(u.title) + '</b> 过关 → ' + esc(ctx.subject.name) + ' ' + esc(ctx.stage.label) + ' ' +
                ctx.stage.passed + '/' + ctx.stage.total + ' → 总路线 ' + view.route.passed + '/' + view.route.total + '。');
        });
        var pendingTests = {};
        changes.pending.forEach(function (id) {
            var u = view.unitById[id];
            pendingTests[u.evidence.testTitle] = u.evidence.coveredCount;
        });
        Object.keys(pendingTests).forEach(function (t) {
            parts.push('「' + esc(t) + '」已达标，覆盖 ' + pendingTests[t] + ' 个单元；折算政策未定，暂不计入路程。');
        });
        changes.dropped.forEach(function (id) {
            var u = view.unitById[id];
            parts.push('<b>' + esc(u.title) + '</b> 掌握度降到 ' + pct(u.mastery.value) + '，需要复测；路程不变，仍是 ' + view.route.passed + '/' + view.route.total + '。');
        });
        changes.restored.forEach(function (id) {
            var u = view.unitById[id];
            parts.push('<b>' + esc(u.title) + '</b> 复测通过，掌握度回到 ' + pct(u.mastery.value) + '；路程不变。');
        });
        if (!changes.passed.length && !changes.pending.length && !changes.restored.length) {
            attemptsNew.filter(function (a) { return !a.passed; }).forEach(function (a) {
                parts.push('「' + esc(a.test_title) + '」这次 ' + a.score + ' 分，达标线 ' + a.threshold + '，还没过；可以先练错题再测。');
            });
        }
        if (changes.plan) {
            parts.push('计划清单调整，总关数 ' + changes.plan.totalBefore + ' → ' + changes.plan.totalAfter +
                '；已过关 ' + view.route.passed + ' 关全部保留。');
        }
        if (event === 'time' && !changes.dropped.length) parts.push('时间过去了 10 天，部分单元掌握度变淡。路程不变。');
        if (!parts.length) {
            if (event) { el.hidden = false; el.innerHTML = '刚刚：没有变化。'; }
            return;
        }
        el.hidden = false;
        el.innerHTML = '刚刚：' + parts.join(' ') +
            (view.nextMilestone && (changes.passed.length || changes.pending.length) ? ' 下一个里程碑：' + esc(view.nextMilestone.subjectName + ' ' + view.nextMilestone.stageLabel) + '。' : '');
    }

    function renderPlanNotice(plan) {
        var el = $('planNotice');
        var meta = state.view.planMeta || {};
        var lines = [];
        if (plan) {
            var parts = [];
            if (plan.added.length) parts.push('新增 ' + plan.added.length + ' 关');
            if (plan.removed.length) parts.push('移除 ' + plan.removed.length + ' 关');
            lines.push('<strong>计划清单有调整</strong>总关数 ' + plan.totalBefore + ' → ' + plan.totalAfter + '（' + parts.join('，') + '）' +
                (meta.applied_at ? '，' + fmtDate(Date.parse(meta.applied_at)) + ' 生效' : '') +
                '。进度已按新清单重算；已有的测试达标记录都保留，没有因此倒退。');
        }
        if (meta.draft_pending) {
            lines.push('<strong>即将调整</strong>助教已保存一份新清单，' + esc(meta.draft_effective_from || '') + ' 起生效，生效后这里会按新清单重算。');
        }
        if (!lines.length) {
            if (!el.dataset.keep) el.hidden = true;
            return;
        }
        el.hidden = false;
        el.innerHTML = lines.join('<br>');
        el.dataset.keep = plan ? '1' : '';
    }

    // —— 演示 ——

    function renderDemoClock() {
        var days = Math.round((state.demoNow - state.demoStart) / Model.DAY_MS);
        $('demoClock').textContent = '演示时间：' + (days ? '今天之后第 ' + days + ' 天' : '今天') + '。所有变化都来自下面的按钮，不会自动变化。';
        var v = state.view;
        var passedUnits = v.units.filter(function (u) { return u.route === 'passed'; });
        document.querySelector('[data-demo="pass"]').disabled = !v.nextMilestone;
        document.querySelector('[data-demo="fail"]').disabled = !v.nextMilestone;
        document.querySelector('[data-demo="retest"]').disabled = !passedUnits.length;
        document.querySelector('[data-demo="retestFail"]').disabled = !passedUnits.length;
    }

    function demoAction(kind) {
        var raw = state.raw;
        var v = state.view;
        var now = state.demoNow;
        if (kind === 'reset') { startDemo(); return; }
        if (kind === 'time') {
            state.demoNow = now + 10 * Model.DAY_MS;
            raw.server_time = new Date(state.demoNow).toISOString();
        } else if (kind === 'pass' || kind === 'fail') {
            if (!v.nextMilestone) return;
            state.demoNow = now + 60 * 1000;
            Demo.addAttempt(raw, v.nextMilestone.nextUnitId, kind === 'pass', state.demoNow);
        } else if (kind === 'retest' || kind === 'retestFail') {
            var passed = v.units.filter(function (u) { return u.route === 'passed'; });
            var target = kind === 'retest'
                ? (v.reviewQueue[0] || passed[0])
                : passed.slice().sort(function (a, b) { return b.mastery.value - a.mastery.value; })[0];
            if (!target) return;
            state.demoNow = now + 60 * 1000;
            Demo.addAttempt(raw, target.unitId, kind === 'retest', state.demoNow);
            state.selectedSubject = target.moduleType;
            state.selectedStage = null;
            state.selectedUnit = target.unitId;
        } else if (kind === 'plan') {
            state.demoNow = now + 60 * 1000;
            Demo.addUnits(raw, 'sentence', 3, state.demoNow);
        }
        accept(raw, state.demoNow, kind);
    }

    function startDemo() {
        state.demoStart = Date.now();
        state.demoNow = state.demoStart;
        state.view = null;
        state.raw = null;
        state.selectedSubject = null; state.selectedStage = null; state.selectedUnit = null;
        $('justNow').hidden = true;
        $('planNotice').hidden = true;
        $('planNotice').dataset.keep = '';
        accept(Demo.create(state.demoStart), state.demoNow, null);
    }

    // —— 启动 ——

    function init() {
        $('refreshBtn').addEventListener('click', function () {
            if (state.mode === 'demo') { accept(state.raw, state.demoNow, 'refresh'); return; }
            loadLive();
        });
        window.addEventListener('resize', function () { requestAnimationFrame(placePin); });
        if (state.mode === 'demo') {
            $('demoNotice').hidden = false;
            $('demoControls').hidden = false;
            document.querySelectorAll('[data-demo]').forEach(function (b) {
                b.addEventListener('click', function () { demoAction(b.getAttribute('data-demo')); });
            });
            $('refreshBtn').textContent = '重新计算';
            startDemo();
            return;
        }
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'visible') loadLive();
        });
        window.addEventListener('focus', function () { loadLive(); });
        loadLive();
    }

    init();
}());
