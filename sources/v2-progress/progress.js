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
        demoNow: null,
        goalId: null,
        goalAchieved: null
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
        SECTIONS.concat(['detail']).forEach(function (id) { $(id).hidden = true; });
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
        if (!prev) state.goalId = loadGoal(view);
        if (state.goalId && changes.passed.indexOf(state.goalId) >= 0) {
            state.goalAchieved = view.unitById[state.goalId].title;
            saveGoal(null);
        }
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

    // 演示模式会原地修改同一份数据，所以按已见过的记录 id 判断「新测试」
    function newAttempts(prevRaw, raw) {
        var first = !prevRaw || !state.seenAttempts;
        var seen = state.seenAttempts || {};
        var fresh = (raw.test_attempts || []).filter(function (a) { return !seen[a.id]; });
        fresh.forEach(function (a) { seen[a.id] = true; });
        state.seenAttempts = seen;
        return first ? [] : fresh;
    }

    // —— 渲染 ——

    var SECTIONS = ['quest', 'rulesStrip', 'feedback', 'choose', 'zones'];

    function goalStoreKey(view) { return 'v2progress.goal.' + (view.student.id || 'unknown'); }

    function loadGoal(view) {
        if (state.mode !== 'live') return state.goalId;
        try { return window.localStorage.getItem(goalStoreKey(view)) || null; } catch (e) { return state.goalId; }
    }

    function saveGoal(unitId) {
        state.goalId = unitId;
        if (state.mode !== 'live' || !state.view) return;
        try {
            if (unitId) window.localStorage.setItem(goalStoreKey(state.view), unitId);
            else window.localStorage.removeItem(goalStoreKey(state.view));
        } catch (e) { /* 记不住也没关系，只是下次回到系统推荐 */ }
    }

    // 目标 = 学生自己选的那一关（没过关时）；否则用系统推荐的下一关
    function currentGoal() {
        var view = state.view;
        var mine = state.goalId && view.unitById[state.goalId];
        if (mine && mine.route !== 'passed') return { unit: mine, chosen: true };
        var ms = view.nextMilestone;
        var rec = ms && ms.nextUnitId ? view.unitById[ms.nextUnitId] : null;
        return rec ? { unit: rec, chosen: false } : null;
    }

    function subjectOf(u) {
        return state.view.subjects.filter(function (x) { return x.moduleType === u.moduleType; })[0];
    }

    function stageOf(u) {
        var s = subjectOf(u);
        return { subject: s, stage: s.stages.filter(function (x) { return x.key === u.stageKey; })[0] };
    }

    function zoneOf(subject) {
        return state.view.zones.filter(function (z) { return z.key === subject.zoneKey; })[0];
    }

    function badgeName(subject, stage) { return subject.name + ' ' + stage.label; }

    function unitNo(u) { return u.unitNo || (u.indexInSubject + 1); }

    // 本次更新里新点亮的段徽章
    function newBadges(prev, changes) {
        if (!prev || !changes) return [];
        var out = [];
        state.view.subjects.forEach(function (s) {
            s.stages.forEach(function (st) {
                if (!st.complete) return;
                var was = st.unitIds.every(function (id) { return prev.unitById[id] && prev.unitById[id].route === 'passed'; });
                if (!was) out.push(st.key);
            });
        });
        return out;
    }

    function render(prev, changes, attemptsNew, event) {
        SECTIONS.forEach(function (id) { $(id).hidden = false; });
        var lit = newBadges(prev, changes);
        renderQuest(prev, changes);
        renderZones(changes, lit);
        renderDetail(changes);
        renderReview();
        renderChoices();
        renderWeek();
        renderJustNow(changes, attemptsNew, event, lit);
        renderPlanNotice(changes.plan);
        if (state.mode === 'demo') renderDemoClock();
        setStatus();
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

    function flash(el, cls, delay) {
        if (reduceMotion) return;
        el.classList.remove(cls);
        void el.offsetWidth;
        setTimeout(function () { el.classList.add(cls); }, delay || 0);
    }

    // —— ① 目标 + 地图总览 ——

    function renderQuest(prev, changes) {
        var view = state.view;
        var r = view.route;
        $('countTotal').textContent = r.total;
        animateNumber($('countPassed'), prev ? prev.route.passed : r.passed, r.passed);
        var sub = ['还剩 ' + r.remaining + ' 关'];
        if (r.pending) sub.push('<span class="pending">另有 ' + r.pending + ' 关旧阶段测已达标，折算待定，暂不计入</span>');
        if (r.studiedOnly) sub.push(r.studiedOnly + ' 关已学完但还没测过（不计）');
        $('countSub').innerHTML = sub.join(' · ');

        $('zoneMini').innerHTML = view.zones.map(function (z) {
            var pw = z.total ? (z.passed / z.total * 100) : 0;
            var qw = z.total ? (z.pending / z.total * 100) : 0;
            return '<li><span class="zm-name">' + esc(z.name) + '</span>' +
                '<span class="zm-bar" aria-hidden="true"><i class="p" style="width:' + pw.toFixed(2) + '%"></i>' +
                '<i class="q" style="left:' + pw.toFixed(2) + '%;width:' + qw.toFixed(2) + '%"></i></span>' +
                '<span class="zm-count">' + z.passed + '/' + z.total + '</span></li>';
        }).join('');
        $('badgeTotal').innerHTML = '段徽章 <b>' + view.badges.earned + '</b> / ' + view.badges.total + ' 已点亮';

        renderGoal(changes);
    }

    function renderGoal(changes) {
        var g = currentGoal();
        var goalEl = $('goal');
        var actions = $('goalActions');
        if (!g) {
            var pending = view.route.pending;
            $('goalKind').textContent = pending ? '能单独过的都过了' : '全部过关';
            $('questTitle').textContent = pending ? '剩下的格子在等折算' : '计划清单里的每一关都过了';
            $('goalWhere').textContent = pending
                ? '还有 ' + pending + ' 格是旧阶段测达标、折算待定。能不能算过关还没定，不需要再测。'
                : '接下来想描深哪一格，由你决定。';
            $('goalBadge').innerHTML = '';
            $('goalWarn').hidden = true;
            actions.innerHTML = '';
            return;
        }
        var u = g.unit;
        var ctx = stageOf(u);
        var zone = zoneOf(ctx.subject);
        $('goalKind').textContent = g.chosen ? '你选的目标' : '下一关（系统推荐，可以换）';
        $('questTitle').textContent = u.title;
        $('goalWhere').textContent = (zone ? zone.name + ' · ' : '') + ctx.subject.name + ' · 第 ' + unitNo(u) + ' 关';

        var st = ctx.stage;
        var dots = st.unitIds.map(function (id) {
            var x = state.view.unitById[id];
            var cls = id === u.unitId ? 'me' : x.route === 'passed' ? 'on' : x.route === 'pending' ? 'pend' : '';
            return '<i class="' + cls + '"></i>';
        }).join('');
        var after = st.passed + (u.route === 'pending' || !u.hasUnitTest ? 0 : 1);
        var line;
        if (!u.hasUnitTest) {
            line = '这一格还不能单独点亮 · ' + esc(badgeName(ctx.subject, st)) + ' 已过 ' + st.passed + '/' + st.total;
        } else if (after === st.total) {
            line = '过了它 → 点亮徽章「' + esc(badgeName(ctx.subject, st)) + '」';
        } else {
            line = '过了它 → ' + esc(badgeName(ctx.subject, st)) + ' ' + after + '/' + st.total + '，离徽章还差 ' + (st.total - after) + ' 关';
        }
        $('goalBadge').innerHTML = '<span class="gb-dots" aria-hidden="true">' + dots + '</span><span>' + line + '</span>';

        var warn = '';
        if (!u.hasUnitTest && u.stageTests && u.stageTests.length) {
            warn = '这一关没有单独的单元测试，只有阶段测「' + u.stageTests[0].title + '」一次覆盖 ' + u.stageTests[0].covered.length + ' 个单元；达标后能否算作单元过关尚未定。';
        } else if (!u.hasUnitTest) {
            warn = '这一关还没有安排测试，暂时无法过关；可以先学，或换一个目标。';
        }
        $('goalWarn').hidden = !warn;
        $('goalWarn').textContent = warn;

        var html = '';
        if (state.mode === 'demo') {
            html += '<button type="button" class="btn-act" data-goal-act="pass">演示：测这一关（达标）</button>' +
                '<button type="button" class="btn-quiet" data-goal-act="fail">演示：测这一关（没达标）</button>';
        } else {
            html += '<a class="btn-act" href="/tinglidanciceshi/" target="_blank" rel="noopener" id="goalGo">去原系统做这一关<span class="sr-only">（新窗口）</span> ↗</a>';
        }
        if (g.chosen) html += '<button type="button" class="btn-quiet" data-goal-act="clear">换回系统推荐</button>';
        else html += '<button type="button" class="btn-quiet" data-goal-act="pick">自己换一关</button>';
        html += '<p class="goal-note">' + (state.mode === 'demo'
            ? '演示里按钮直接写入示例测试记录。'
            : '学习和测试都在原系统里做，先学还是先测你定；这里只看结果，做完回来会自动更新。') + '</p>';
        actions.innerHTML = html;
        actions.querySelectorAll('[data-goal-act]').forEach(function (b) {
            b.addEventListener('click', function () {
                var act = b.getAttribute('data-goal-act');
                if (act === 'clear') { saveGoal(null); rerender(); }
                else if (act === 'pick') focusZones();
                else demoAction(act);
            });
        });
        if (changes && (changes.passed.length || changes.pending.length)) flash(goalEl, 'updated', 900);
    }

    function rerender() {
        renderQuest(null, null);
        renderZones(null, []);
        renderDetail(null);
        renderChoices();
    }

    function focusZones() {
        var z = $('zones');
        z.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        var first = z.querySelector('.tile.open, .tile');
        (first || z).focus({ preventScroll: true });
    }

    // —— ③ 反馈 ——

    function renderWeek() {
        var a = state.view.activity;
        $('week').innerHTML =
            '<div><dt>近 ' + a.days + ' 天测试</dt><dd>' + a.attempts + '<small>次</small></dd></div>' +
            '<div><dt>新过关</dt><dd>' + a.newPasses + '<small>关</small></dd></div>' +
            '<div><dt>复测描深</dt><dd>' + a.retestPasses + '<small>次</small></dd></div>' +
            '<div><dt>段徽章</dt><dd>' + state.view.badges.earned + '<small>/ ' + state.view.badges.total + '</small></dd></div>';
    }

    function renderJustNow(changes, attemptsNew, event, lit) {
        var el = $('justNow');
        var view = state.view;
        var parts = [];
        if (state.goalAchieved) {
            parts.push('你选的目标<b>「' + esc(state.goalAchieved) + '」</b>达成！');
            state.goalAchieved = null;
        }
        changes.passed.forEach(function (id) {
            var u = view.unitById[id];
            var ctx = stageOf(u);
            var zone = zoneOf(ctx.subject);
            parts.push('<b>' + esc(u.title) + '</b> 过关，格子点亮 → ' + esc(ctx.subject.name) + ' ' + ctx.subject.passed + '/' + ctx.subject.total +
                (zone ? ' → ' + esc(zone.name) + ' ' + zone.passed + '/' + zone.total : '') +
                ' → 地图 ' + view.route.passed + '/' + view.route.total + '。');
        });
        lit.forEach(function (key) {
            view.subjects.forEach(function (s) {
                s.stages.forEach(function (st) {
                    if (st.key === key) parts.push('点亮徽章<b>「' + esc(badgeName(s, st)) + '」</b>！');
                });
            });
        });
        var pendingTests = {};
        changes.pending.forEach(function (id) {
            var u = view.unitById[id];
            pendingTests[u.evidence.testTitle] = u.evidence.coveredCount;
        });
        Object.keys(pendingTests).forEach(function (t) {
            parts.push('「' + esc(t) + '」已达标，覆盖 ' + pendingTests[t] + ' 个单元；折算政策未定，暂不计入。');
        });
        if (changes.dropped.length > 2) {
            parts.push(changes.dropped.length + ' 格色条变淡（' + changes.dropped.slice(0, 3).map(function (id) {
                var u = view.unitById[id];
                return esc(u.title) + ' ' + pct(u.mastery.value);
            }).join('、') + (changes.dropped.length > 3 ? ' 等' : '') + '），需要复测；格子仍然亮着，过关数不变。');
        } else {
            changes.dropped.forEach(function (id) {
                var u = view.unitById[id];
                parts.push('<b>' + esc(u.title) + '</b> 掌握度降到 ' + pct(u.mastery.value) + '，色条变淡了；格子仍然亮着，过关数不变。');
            });
        }
        changes.restored.forEach(function (id) {
            var u = view.unitById[id];
            parts.push('<b>' + esc(u.title) + '</b> 复测通过，色条描深到 ' + pct(u.mastery.value) + '。');
        });
        if (!changes.passed.length && !changes.pending.length && !changes.restored.length) {
            attemptsNew.filter(function (a) { return !a.passed; }).forEach(function (a) {
                parts.push('「' + esc(a.test_title) + '」这次 ' + a.score + ' 分，达标线 ' + a.threshold + '，差 ' +
                    Math.max(0, Math.round((a.threshold - a.score) * 10) / 10) + ' 分；练练错题再来，随时可以重测。');
            });
        }
        if (changes.plan) {
            parts.push('计划清单调整，总关数 ' + changes.plan.totalBefore + ' → ' + changes.plan.totalAfter +
                '；已过的 ' + view.route.passed + ' 关全部保留。');
        }
        if (event === 'time' && !changes.dropped.length) parts.push('时间过去了 10 天，部分单元色条变淡。过关数不变。');
        if (!parts.length) {
            if (event) el.innerHTML = '刚刚：没有变化。';
            return;
        }
        var g = currentGoal();
        el.innerHTML = '<span class="jn-label">刚刚</span>' + parts.join(' ') +
            (g && (changes.passed.length || changes.pending.length) ? ' 下一个目标：' + esc(g.unit.title) + '。' : '');
        flash($('feedback'), 'updated', 200);
    }

    // —— ④ 你来选 ——

    function renderChoices() {
        var view = state.view;
        var g = currentGoal();
        var fade = view.reviewQueue.length;
        var html =
            '<button type="button" class="choice" data-choice="goal"' + (g ? '' : ' disabled') + '>' +
            '<b>冲一关</b><span>' + (g ? esc(g.unit.title) : '已经全部过关') + '</span></button>' +
            '<button type="button" class="choice" data-choice="review" aria-expanded="' + !$('review').hidden + '"' + (fade ? '' : ' disabled') + '>' +
            '<b>描深 ' + fade + ' 格</b><span>' + (fade ? '褪色的格子，复测通过就描深' : '现在没有褪色的格子') + '</span></button>' +
            '<button type="button" class="choice" data-choice="pick">' +
            '<b>自己挑一关</b><span>在单元区点任意一格，设为目标</span></button>';
        var el = $('choices');
        el.innerHTML = html;
        el.querySelectorAll('[data-choice]').forEach(function (b) {
            b.addEventListener('click', function () {
                var c = b.getAttribute('data-choice');
                if (c === 'goal') {
                    $('quest').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
                    var go = $('goalActions').querySelector('a, button');
                    if (go) go.focus({ preventScroll: true });
                } else if (c === 'review') {
                    $('review').hidden = !$('review').hidden;
                    b.setAttribute('aria-expanded', String(!$('review').hidden));
                } else focusZones();
            });
        });
        if (!fade) $('review').hidden = true;
    }

    function renderReview() {
        var q = state.view.reviewQueue;
        $('reviewList').innerHTML = q.map(function (u) {
            var m = u.mastery;
            return '<li><button type="button" class="chip m-' + m.state + '" data-unit="' + esc(u.unitId) + '"' +
                ' aria-label="' + esc(u.subjectName + ' ' + u.title + '：' + masteryWord(m.state) + '，掌握度 ' + pct(m.value) + '，最近达标 ' + fmtDate(m.lastPassAt)) + '">' +
                '<span class="c-sub">' + esc(u.subjectName) + '</span>' +
                '<span class="c-title">' + esc(u.title) + '</span>' +
                '<span class="c-m"><i style="width:' + (m.value * 100).toFixed(1) + '%"></i></span>' +
                '<span class="c-state">' + masteryWord(m.state) + ' · ' + pct(m.value) + (m.retestFailed ? ' · 复测未过' : '') + '</span></button></li>';
        }).join('');
        $('reviewList').querySelectorAll('button').forEach(function (b) {
            b.addEventListener('click', function () { openUnit(b.getAttribute('data-unit')); });
        });
    }

    // —— 单元区仪表盘 ——

    function tileHtml(u, changes, goalId) {
        var cls = ['tile', u.route];
        if (u.route === 'open' && u.studied) cls.push('studied');
        if (u.unitId === goalId) cls.push('goal');
        if (u.route === 'passed' && u.mastery.state !== 'none') cls.push('m-' + u.mastery.state);
        if (state.selectedUnit === u.unitId) cls.push('selected');
        if (!reduceMotion && changes) {
            if (changes.passed.indexOf(u.unitId) >= 0) cls.push('just-passed');
            if (changes.dropped.indexOf(u.unitId) >= 0) cls.push('just-dropped');
            if (changes.restored.indexOf(u.unitId) >= 0) cls.push('just-restored');
        }
        var stateText = u.route === 'passed' ? '已过关，' + masteryWord(u.mastery.state) + (u.mastery.value !== null ? ' ' + pct(u.mastery.value) : '')
            : u.route === 'pending' ? '旧阶段测已达标，折算待定'
            : u.studied ? '已学，还没测过' : '未过关';
        var mw = u.route === 'passed' && u.mastery.value !== null ? (u.mastery.value * 100).toFixed(1) : 0;
        return '<button type="button" class="' + cls.join(' ') + '" data-unit="' + esc(u.unitId) + '"' +
            ' aria-label="第 ' + unitNo(u) + ' 关 ' + esc(u.title) + '：' + esc(stateText) + (u.unitId === goalId ? '，当前目标' : '') + '"' +
            ' title="' + esc(u.title) + '">' +
            (u.unitId === goalId ? '<span class="t-flag" aria-hidden="true">目标</span>' : '') +
            '<span class="t-no">' + unitNo(u) + '</span>' +
            '<span class="t-title">' + esc(u.title) + '</span>' +
            '<span class="t-m" aria-hidden="true"><i style="width:' + mw + '%"></i></span></button>';
    }

    function medalHtml(subject, st, lit) {
        var cls = ['medal'];
        if (st.complete) cls.push('earned');
        else if (st.pending) cls.push('pend');
        else if (st.passed) cls.push('part');
        if (!reduceMotion && lit.indexOf(st.key) >= 0) cls.push('just-lit');
        var label = badgeName(subject, st) + '：' + (st.complete ? '徽章已点亮' : '已过 ' + st.passed + '/' + st.total +
            (st.pending ? '，待定 ' + st.pending : ''));
        return '<button type="button" class="' + cls.join(' ') + '" data-stage="' + esc(st.key) + '" data-subject="' + esc(subject.moduleType) + '" title="' + esc(label) + '" aria-label="' + esc(label) + '">' + (st.index + 1) + '</button>';
    }

    function renderZones(changes, lit) {
        var view = state.view;
        var g = currentGoal();
        var goalId = g ? g.unit.unitId : null;
        $('zoneList').innerHTML = view.zones.map(function (z) {
            var pw = z.total ? z.passed / z.total * 100 : 0;
            var mods = z.subjects.map(function (s) {
                var groups = s.stages.map(function (st) {
                    return '<div class="tile-group' + (st.complete ? ' complete' : '') + '">' +
                        st.unitIds.map(function (id) { return tileHtml(view.unitById[id], changes, goalId); }).join('') + '</div>';
                }).join('');
                var mNote = s.review ? '<span class="m-review">' + s.review + ' 格需复测</span>' : s.fading ? s.fading + ' 格开始褪色' : '';
                return '<div class="module">' +
                    '<div class="module-head">' +
                    '<button type="button" class="module-name" data-subject="' + esc(s.moduleType) + '">' + esc(s.name) + '</button>' +
                    '<span class="module-count"><b>' + s.passed + '</b>/' + s.total + ' 关' + (s.pending ? ' · 待定 ' + s.pending : '') + '</span>' +
                    '<span class="medals" aria-label="段徽章">' + s.stages.map(function (st) { return medalHtml(s, st, lit); }).join('') + '</span>' +
                    (mNote ? '<span class="module-note">' + mNote + '</span>' : '') +
                    '</div>' +
                    '<div class="tiles">' + groups + '</div></div>';
            }).join('');
            return '<article class="zone zone-' + esc(z.key) + '" aria-label="' + esc(z.name) + '">' +
                '<header class="zone-head"><h3>' + esc(z.name) + '</h3>' +
                '<span class="zone-bar" aria-hidden="true"><i style="width:' + pw.toFixed(2) + '%"></i></span>' +
                '<span class="zone-count"><b>' + z.passed + '</b> / ' + z.total + ' 关 · 徽章 ' + z.badges + '/' + z.badgesTotal + '</span></header>' +
                mods + '</article>';
        }).join('');
        var list = $('zoneList');
        list.querySelectorAll('.tile').forEach(function (b) {
            b.addEventListener('click', function () { openUnit(b.getAttribute('data-unit')); });
        });
        list.querySelectorAll('.module-name').forEach(function (b) {
            b.addEventListener('click', function () { selectSubject(b.getAttribute('data-subject'), null, null, true); });
        });
        list.querySelectorAll('.medal').forEach(function (b) {
            b.addEventListener('click', function () { selectSubject(b.getAttribute('data-subject'), b.getAttribute('data-stage'), null, true); });
        });
    }

    function openUnit(unitId) {
        var u = state.view.unitById[unitId];
        if (!u) return;
        selectSubject(u.moduleType, u.stageKey, u.unitId, true);
    }

    function selectSubject(mt, stageKey, unitId, focus) {
        state.selectedSubject = mt;
        state.selectedStage = stageKey;
        state.selectedUnit = unitId;
        renderZones(null, []);
        renderDetail(null);
        if (focus) {
            var d = $('detail');
            d.focus({ preventScroll: true });
            d.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        }
    }

    function backToZones() {
        var id = state.selectedUnit;
        state.selectedSubject = null; state.selectedStage = null; state.selectedUnit = null;
        renderZones(null, []); renderDetail(null);
        var z = $('zones');
        z.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        var tile = id ? z.querySelector('.tile[data-unit="' + cssEscape(id) + '"]') : null;
        (tile || z).focus({ preventScroll: true });
    }

    function cssEscape(s) {
        return window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/"/g, '\\"');
    }

    function renderDetail(changes) {
        var view = state.view;
        var d = $('detail');
        var subj = view.subjects.filter(function (s) { return s.moduleType === state.selectedSubject; })[0];
        if (!subj) { d.hidden = true; return; }
        d.hidden = false;
        var stage = subj.stages.filter(function (s) { return s.key === state.selectedStage; })[0] || null;
        var zone = zoneOf(subj);

        var crumbs = '<button type="button" data-crumb="route">整张地图 ' + view.route.passed + '/' + view.route.total + '</button><span class="sep">›</span>' +
            (zone ? '<span>' + esc(zone.name) + '</span><span class="sep">›</span>' : '');
        if (stage) {
            crumbs += '<button type="button" data-crumb="subject">' + esc(subj.name) + '</button><span class="sep">›</span>' +
                '<span aria-current="page">' + esc(stage.label) + '</span>';
        } else {
            crumbs += '<span aria-current="page">' + esc(subj.name) + '</span>';
        }
        $('crumbs').innerHTML = crumbs;
        $('crumbs').querySelectorAll('button').forEach(function (b) {
            b.addEventListener('click', function () {
                if (b.getAttribute('data-crumb') === 'route') backToZones();
                else selectSubject(subj.moduleType, null, state.selectedUnit, false);
            });
        });

        $('detailTitle').textContent = subj.name + ' · 已过 ' + subj.passed + '/' + subj.total + ' 关' + (subj.pending ? ' · 待定 ' + subj.pending : '');
        var g = currentGoal();
        var goalId = g ? g.unit.unitId : null;
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
            var flag = st.complete ? '徽章已点亮' : st.pending ? '阶段测已达标 · ' + st.pending + ' 个单元折算待定' : '';
            var stations = st.unitIds.map(function (id, i) {
                var u = view.unitById[id];
                var nextU = view.unitById[st.unitIds[i + 1]];
                var on = u.route === 'passed' && nextU && nextU.route === 'passed';
                var cls = ['station', u.route];
                if (u.route === 'passed' && u.mastery.state !== 'none') cls.push('m-' + u.mastery.state);
                if (u.unitId === goalId) cls.push('next');
                if (!reduceMotion && changes && changes.passed.indexOf(u.unitId) >= 0) cls.push('just-passed');
                var stText = u.unitId === goalId ? '目标'
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
                (flag ? '<span class="stage-flag' + (st.complete ? ' earned' : '') + '">' + esc(flag) + '</span>' : '') + '</div>' +
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
                renderZones(null, []);
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
        var g = currentGoal();
        var isGoal = g && g.unit.unitId === u.unitId;
        var html = '<h3>第 ' + unitNo(u) + ' 关 · ' + esc(u.title) + '</h3>';
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
                        ? '想描深的话可以复测，通过后色条回到满格。'
                        : '按暂定模型，约 ' + fmtDate(m.reviewAt) + ' 会降到 80% 以下。') +
                    '过关数不受影响。</p>';
            }
        } else if (u.route === 'pending') {
            html += '<p>旧阶段测「' + esc(u.evidence.testTitle) + '」' + (u.evidence.passedAt ? '于 ' + fmtDate(u.evidence.passedAt) + ' ' : '') +
                '已达标，这次测试覆盖 ' + u.evidence.coveredCount + ' 个单元。</p>' +
                '<p class="muted">一次测多个单元达标后，能否算作每个单元过关还没有定，所以暂不计入，也不计算掌握度。</p>';
        } else {
            html += u.studied ? '<p>已学完（打勾），但还没有测试达标，不计入过关。</p>' : '<p>还没过关。</p>';
            if (u.hasUnitTest) {
                html += '<p class="muted">先学还是先测都可以，过关只看这个单元的测试。</p>';
            } else if (u.stageTests && u.stageTests.length) {
                html += '<p class="muted">这个单元没有单独的测试，只有阶段测「' + esc(u.stageTests[0].title) +
                    '」一次覆盖 ' + u.stageTests[0].covered.length + ' 个单元；它达标后能否算作单元过关尚未定。</p>';
            } else {
                html += '<p class="muted">这个单元还没有安排任何测试，没有测试就无法过关。</p>';
            }
            html += isGoal
                ? '<p class="goal-mark">这是你现在的目标。</p>'
                : '<button type="button" class="btn-act" id="setGoalBtn">设为我的目标</button>';
        }
        html += '<button type="button" class="btn-quiet back-zones" id="backZonesBtn">回到单元区</button>';
        el.innerHTML = html;
        var setBtn = $('setGoalBtn');
        if (setBtn) {
            setBtn.addEventListener('click', function () {
                saveGoal(u.unitId);
                rerender();
                $('justNow').innerHTML = '<span class="jn-label">刚刚</span>你把<b>「' + esc(u.title) + '」</b>设为目标。';
                $('quest').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
                var go = $('goalActions').querySelector('a, button');
                if (go) go.focus({ preventScroll: true });
            });
        }
        $('backZonesBtn').addEventListener('click', backToZones);
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
        document.querySelector('[data-demo="pass"]').disabled = !currentGoal();
        document.querySelector('[data-demo="fail"]').disabled = !currentGoal();
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
            var g = currentGoal();
            if (!g) return;
            state.demoNow = now + 60 * 1000;
            Demo.addAttempt(raw, g.unit.unitId, kind === 'pass', state.demoNow);
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
        state.goalId = null;
        state.seenAttempts = null;
        $('justNow').textContent = '打开页面后，你每过一关，这里会马上告诉你点亮了什么。';
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
