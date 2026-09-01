// 学生端：登录、学习与测试
var currentTestMode = 'random';
var testWords = [];
var testResults = [];
var currentTestIndex = 0;
var timerInterval = null;
var timeLeft = 6;
var isPlaying = false;
var forcePasswordChange = false;


function rememberStudentSession(student) {
    try {
        localStorage.setItem(STUDENT_SESSION_KEY, JSON.stringify({
            student_id: student.student_id,
            expires_at: Date.now() + STUDENT_SESSION_DAYS * 24 * 60 * 60 * 1000
        }));
    } catch (e) {
        console.warn('保存学生登录态失败:', e);
    }
}

function clearStudentSession() {
    try { localStorage.removeItem(STUDENT_SESSION_KEY); } catch (e) {}
}

async function restoreStudentSession() {
    try {
        const me = await authMe('student');
        if (!me.data || me.data.role !== 'student' || !me.data.student) {
            clearStudentSession();
            return;
        }
        currentStudent = me.data.student;
        rememberStudentSession(me.data.student);
        if (!me.data.student.is_password_changed) {
            showScreen('studentLoginScreen');
            showChangePasswordModal(true);
            return;
        }
        showStudentHome();
    } catch (e) {
        console.error('恢复学生登录态失败:', e);
    }
}

// 学生登录
async function studentLogin() {
    const studentId = document.getElementById('studentId').value.trim();
    const password = document.getElementById('studentPassword').value;
    if (!studentId || !password) { showToast('请输入学号和密码', 'error'); return; }
    try {
        const result = await apiFetch('/api/auth/student/login', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId, password: password })
        });
        if (result.error || !result.data || !result.data.student) {
            showToast((result.error && result.error.message) || '学号或密码错误', 'error');
            return;
        }
        currentStudent = result.data.student;
        rememberStudentSession(result.data.student);
        if (!result.data.student.is_password_changed) {
            showChangePasswordModal(true);
        } else {
            showStudentHome();
        }
    } catch (e) {
        console.error('登录失败:', e);
        showToast('登录失败：' + (e.message || '请稍后再试'), 'error');
    }
}

function showStudentHome() {
    showScreen('studentHome');
    document.getElementById('studentWelcome').textContent = '你好，' + currentStudent.name + '！';
    refreshWritingUnseenCount(true).finally(function() {
        loadTodayTasks();
        loadProgressTable();
    });
}

function formatTaskMinutes(m) {
    const n = Number(m) || 0;
    if (n <= 0) return '0';
    if (n < 10 && Math.abs(n - Math.round(n)) > 0.05) {
        return String(Math.round(n * 10) / 10);
    }
    return String(Math.round(n));
}

function renderTaskItemTimeCompare(est, actual) {
    const e = Number(est) || 0;
    const a = Number(actual) || 0;
    let actualColor = '#64748b';
    if (a > 0 && e > 0 && a > e * 1.2) actualColor = '#b45309';
    if (a > 0 && e > 0 && a <= e) actualColor = '#16a34a';
    return ' <span style="color:#94a3b8;font-size:0.85rem;">预计 ' + formatTaskMinutes(e) +
        '′ · 已练 <span style="color:' + actualColor + ';">' + formatTaskMinutes(a) + '′</span></span>';
}

async function loadTodayTasks() {
    const panel = document.getElementById('taskTodayPanel');
    const planPanel = document.getElementById('taskPlanProgressPanel');
    if (!panel) return;
    panel.innerHTML = '<p style="color:#666;">加载今日任务…</p>';
    const result = await apiFetch('/api/task/me/today');
    if (result.error) {
        panel.innerHTML = '<p style="color:#c00;">加载失败：' +
            ((result.error && result.error.message) || '请稍后再试') + '</p>';
        return;
    }
    const data = result.data || {};
    const items = data.items || [];
    const progress = data.progress || {};
    let html = '<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;">';
    html += '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">';
    html += '<h3 style="margin:0;">① 今日任务</h3>';
    const estTotal = Number(data.est_total_minutes) || 0;
    const actualTotal = Number(data.actual_total_minutes) || 0;
    const budgetMin = Number(data.budget_minutes) || 0;
    const budgetPct = budgetMin > 0 ? Math.min(100, Math.round(actualTotal / budgetMin * 100)) : 0;
    let actualColor = '#334155';
    if (actualTotal > budgetMin && budgetMin > 0) actualColor = '#b45309';
    else if (actualTotal > estTotal && estTotal > 0) actualColor = '#b45309';
    else if (actualTotal > 0) actualColor = '#16a34a';
    html += '<div style="text-align:right;min-width:200px;">';
    html += '<div style="color:#64748b;font-size:0.9rem;">预计 ' + formatTaskMinutes(estTotal) +
        '′ · 已练 <span style="color:' + actualColor + ';font-weight:600;">' +
        formatTaskMinutes(actualTotal) + '′</span> · 预算 ' + formatTaskMinutes(budgetMin) + '′</div>';
    if (budgetMin > 0) {
        html += '<div style="margin-top:6px;height:6px;background:#e2e8f0;border-radius:999px;overflow:hidden;">';
        html += '<div style="height:100%;width:' + budgetPct + '%;background:' +
            (budgetPct > 100 ? '#f59e0b' : '#667eea') + ';border-radius:999px;"></div></div>';
    }
    html += '</div></div>';
    if (actualTotal > budgetMin && budgetMin > 0 && items.length) {
        html += '<p style="color:#b45309;margin:8px 0 0;font-size:0.85rem;">' +
            '已练时长超过今日预算，仍可继续完成任务。</p>';
    }
    if (data.pending_plan_change) {
        var eff = data.pending_effective_from;
        var todayStr = (function() {
            var d = new Date();
            var m = d.getMonth() + 1;
            var day = d.getDate();
            return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (day < 10 ? '0' : '') + day;
        })();
        if (eff && eff <= todayStr) {
            html += '<p style="color:#b45309;margin:8px 0 0;">计划有待合并的更新，请下拉刷新本页；若仍无变化请联系助教将生效日设为今天并重新保存。</p>';
        } else {
            var effText = eff ? (eff + ' 起生效') : '稍后生效';
            html += '<p style="color:#b45309;margin:8px 0 0;">计划已更新，' + effText + '（到期前今日任务仍按原清单）</p>';
        }
    }
    if (!items.length) {
        html += '<p style="margin:16px 0 0;color:#64748b;">' +
            (data.empty_message || '今日暂无任务，请联系助教') + '</p>';
    } else {
        const byMod = {};
        items.forEach(function(it) {
            const mt = it.module_type || 'other';
            if (!byMod[mt]) byMod[mt] = [];
            byMod[mt].push(it);
        });
        Object.keys(byMod).forEach(function(mt) {
            const p = progress[mt] || {};
            const mod = getModuleById(mt);
            const name = (mod && mod.name) || mt;
            html += '<div style="margin-top:14px;padding-top:12px;border-top:1px solid #e2e8f0;">';
            html += '<div style="font-weight:600;margin-bottom:8px;">' + name +
                ' <span style="font-weight:400;color:#64748b;font-size:0.9rem;">计划学习 ' +
                (p.study_x || 0) + '/' + (p.study_y || 0) +
                (p.pass_b ? (' · 过关 ' + (p.pass_a || 0) + '/' + p.pass_b) : '') +
                '</span></div>';
            byMod[mt].forEach(function(it) {
                const done = it.state === 'done_study' || it.state === 'done_pass';
                const fail = it.state === 'done_fail';
                let btn = '';
                if (done) {
                    btn = '<span style="color:#16a34a;">已完成</span>';
                } else if (fail) {
                    btn = '<span style="color:#dc2626;">未过关 · 可重测</span> ' +
                        '<button class="btn btn-secondary" type="button" onclick="openTaskItem(' +
                        it.plan_item_id + ')">继续测试</button>';
                } else if (it.item_type === 'test') {
                    btn = '<button class="btn btn-primary" type="button" onclick="openTaskItem(' +
                        it.plan_item_id + ')">去测试</button>';
                } else {
                    btn = '<button class="btn btn-primary" type="button" onclick="openTaskItem(' +
                        it.plan_item_id + ')">去学习</button>';
                }
                html += '<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 0;">';
                html += '<div><span style="color:#64748b;font-size:0.85rem;">' +
                    (it.item_type === 'test' ? '测' : '学') + '</span> ' +
                    escapeHtml(it.title || '') +
                    renderTaskItemTimeCompare(it.est_minutes, it.actual_minutes) +
                    (it.scope_total ? (' <span style="color:#94a3b8;font-size:0.85rem;">本单元 ' +
                        (it.scope_done || 0) + '/' + it.scope_total + (it.scope_unit || '') +
                        '</span>') : '') +
                    '</div><div>' + btn + '</div></div>';
            });
            html += '</div>';
        });
    }
    html += '</div>';
    panel.innerHTML = html;

    if (planPanel) {
        let phtml = '<div style="border:1px solid #e2e8f0;border-radius:12px;padding:14px;">';
        phtml += '<h3 style="margin:0 0 10px;">② 我的计划进度</h3>';
        const keys = Object.keys(progress);
        if (!keys.length) {
            phtml += '<p style="color:#64748b;margin:0;">暂无已排科目</p>';
        } else {
            keys.forEach(function(mt) {
                const p = progress[mt];
                const mod = getModuleById(mt);
                phtml += '<div style="padding:6px 0;">' + ((mod && mod.name) || mt) +
                    ' · 学习 ' + (p.study_x || 0) + '/' + (p.study_y || 0) +
                    (p.pass_b ? (' · 过关 ' + (p.pass_a || 0) + '/' + p.pass_b) : '') +
                    '</div>';
            });
        }
        phtml += '</div>';
        planPanel.innerHTML = phtml;
    }
    window._todayTaskItems = items;
}

function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
}

function openTaskItem(planItemId) {
    const items = window._todayTaskItems || [];
    const it = items.find(function(x) { return x.plan_item_id === planItemId; });
    if (!it) {
        showToast('任务不存在，请刷新', 'error');
        return;
    }
    if (it.item_type === 'test') {
        // MVP: simple stage test via prompt score
        const raw = window.prompt('阶段测得分（MVP 手填，正式版接测试页）', '85');
        if (raw == null) return;
        const score = Number(raw);
        if (isNaN(score)) {
            showToast('请输入数字', 'error');
            return;
        }
        apiFetch('/api/task/me/submit-test', {
            method: 'POST',
            body: JSON.stringify({
                plan_item_id: planItemId,
                score: score,
                threshold: 80
            })
        }).then(function(result) {
            if (result.error) {
                showToast((result.error && result.error.message) || '提交失败', 'error');
                return;
            }
            showToast(result.data && result.data.passed ? '已过关' : '未过关', result.data && result.data.passed ? 'success' : 'error');
            loadTodayTasks();
        });
        return;
    }
    let url = it.study_url || '';
    if (!url) {
        showToast('该单元暂无学习链接', 'error');
        return;
    }
    window._currentTaskContext = {
        plan_item_id: it.plan_item_id,
        unit_id: it.unit_id,
        content_version: it.content_version || '1',
        daily_task_id: it.daily_task_id
    };
    const mod = getModuleById(it.module_type) || { id: it.module_type, name: it.module_type };
    if ((it.module_type === 'dictation' || it.module_type === 'listening_basic') &&
        typeof openListeningIframe === 'function') {
        const groupMatch = /[?&]group=(\d+)/.exec(url);
        const groupIndex = groupMatch ? Number(groupMatch[1]) : 0;
        openListeningIframe(it.module_type, {
            group: groupIndex,
            task_id: it.daily_task_id,
            plan_item_id: it.plan_item_id,
            unit_id: it.unit_id,
            content_version: it.content_version || '1'
        });
        return;
    }
    openGenericIframe(mod.id, mod.name || it.title, url, 'study');
}

async function completeCurrentTaskStudy(payload) {
    const ctx = window._currentTaskContext || {};
    const planItemId = (payload && payload.plan_item_id) || ctx.plan_item_id;
    const contentVersion = (payload && payload.content_version) || ctx.content_version || '1';
    if (!planItemId) {
        showToast('无任务上下文', 'error');
        return;
    }
    const result = await apiFetch('/api/task/me/complete-study', {
        method: 'POST',
        body: JSON.stringify({
            plan_item_id: planItemId,
            content_version: contentVersion
        })
    });
    if (result.error) {
        showToast((result.error && result.error.message) || '打勾失败', 'error');
        return;
    }
    showToast('任务已完成', 'success');
    window._currentTaskContext = null;
    showStudentHome();
    switchStudentTab('tasks');
}

function switchStudentTab(tab) {
    document.querySelectorAll('#studentHome [data-student-tab]').forEach(function(t) {
        t.classList.toggle('active', t.getAttribute('data-student-tab') === tab);
    });
    var tasksEl = document.getElementById('studentTabTasks');
    if (tasksEl) tasksEl.style.display = tab === 'tasks' ? 'block' : 'none';
    document.getElementById('studentTabProgress').style.display = tab === 'progress' ? 'block' : 'none';
    document.getElementById('studentTabHistory').style.display = tab === 'history' ? 'block' : 'none';
    if (tab === 'history') {
        loadStudentHistory();
    }
    if (tab === 'tasks') {
        loadTodayTasks();
    }
}

async function refreshWritingUnseenCount(showTip) {
    window._writingUnseenCount = 0;
    if (!currentStudent || !currentStudent.student_id) return 0;
    try {
        const resp = await fetch('/api/writing/student/records?student_id=' + encodeURIComponent(currentStudent.student_id));
        const result = await resp.json();
        const unseen = Number((result && result.unseenCount) || 0);
        window._writingUnseenCount = unseen;
        if (showTip && unseen > 0) {
            showToast('老师已批改 ' + unseen + ' 篇作文，请到「作文批改 → 历史」查看', 'info');
        }
        return unseen;
    } catch (e) {
        window._writingUnseenCount = 0;
        return 0;
    }
}

function openWritingCorrectionHistory() {
    openGenericIframe(
        'writing_correction',
        '作文批改历史',
        '../xiezuopigai/ielts-writing-backend/teacher.html?role=student&v=12',
        'history'
    );
}

async function loadProgressTable() {
    const progressResult = await apiFetch('/api/student/progress');
    if (progressResult.error) {
        showToast((progressResult.error && progressResult.error.message) || '加载进度失败', 'error');
        return;
    }
    const records = (progressResult.data && progressResult.data.test_records) || [];
    const allSessions = (progressResult.data && progressResult.data.study_sessions) || [];
    const sessions = getStudySessions(allSessions);
    window._wrongBookCounts = (progressResult.data && progressResult.data.wrong_book_counts) || {};
    const wrongCount = Object.keys(window._wrongBookCounts).reduce(function(sum, key) {
        return sum + Number(window._wrongBookCounts[key] || 0);
    }, 0);
    const todayKey = getChinaDateKey();
    const totalStudySeconds = window.TrackingUtils.sumPracticeSeconds(allSessions, records);
    const todayStudySeconds = window.TrackingUtils.sumPracticeSeconds(allSessions, records, {
        createdAt: function(iso) { return getChinaDateKey(iso) === todayKey; }
    });
    const availableModules = MODULES.filter(isModuleAvailable);
    const testableModules = availableModules.filter(function(m) { return isBuiltinDictationModule(m.id) || m.test_url; });
    let totalProgressForTests = 0;

    const container = document.getElementById('progressTable');
    let html = '<table style="width:100%; border-collapse: collapse;">';
    html += '<thead><tr style="background:#f8f9fa;">';
    html += '<th style="padding:12px; text-align:left; border-bottom:2px solid #dee2e6;">科目</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">达标线</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">测试进度</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">练习时长</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">操作</th>';
    html += '</tr></thead><tbody>';

    for (let i = 0; i < availableModules.length; i++) {
        const m = availableModules[i];
        const moduleTarget = getModuleTarget(m);
        const moduleRecords = getModuleRecords(records, m.id);
        const modSessions = getModuleStudySessions(sessions, m.id);
        const modSeconds = window.TrackingUtils.sumPracticeSeconds(allSessions, records, { moduleId: m.id });
        const speakingPracticed = m.id === 'speaking' ? getSpeakingPracticedCount(modSessions) : 0;
        const bestScore = getBestScore(moduleRecords);
        const passCount = getPassCount(moduleRecords);
        const progressPercent = bestScore > 0 ? Math.min(100, Math.round((bestScore / moduleTarget) * 100)) : 0;
        const isTestable = !isStudyOnlyModule(m) && (isBuiltinDictationModule(m.id) || !!m.test_url);
        if (isTestable) totalProgressForTests += progressPercent;

        let statusClass = 'badge-info';
        let statusText = '未开始';
        if (!isStudyOnlyModule(m) && bestScore >= moduleTarget && bestScore > 0) {
            statusClass = 'badge-success';
            statusText = '达标';
        } else if (moduleRecords.length > 0 || modSeconds > 0 || speakingPracticed > 0) {
            statusClass = 'badge-warning';
            statusText = '进行中';
        }

        const progressColor = progressPercent >= 100 ? '#28a745' : '#667eea';
        let scoreDisplay;
        if (isStudyOnlyModule(m)) {
            scoreDisplay = '—';
        } else if (moduleRecords.length > 0) {
            scoreDisplay = formatTargetValue(bestScore, m.unit);
        } else {
            scoreDisplay = modSeconds > 0 ? '学习中' : (m.unit === '分' ? '0分' : '0%');
        }
        html += '<tr style="border-bottom:1px solid #dee2e6;">';
        html += '<td style="padding:15px 12px;"><strong>' + m.name + '</strong></td>';
        html += '<td style="padding:15px 12px; text-align:center;">' + (isStudyOnlyModule(m) ? '—' : formatTargetValue(moduleTarget, m.unit)) + '</td>';
        html += '<td style="padding:15px 12px; min-width:180px;">';
        html += '<div style="display:flex; align-items:center; gap:10px;">';
        if (!isStudyOnlyModule(m)) {
            html += '<div style="flex:1; background:#e9ecef; border-radius:10px; height:8px; overflow:hidden;">';
            html += '<div style="width:' + progressPercent + '%; background:' + progressColor + '; height:100%; transition:width 0.3s;"></div>';
            html += '</div>';
            html += '<span style="min-width:60px; text-align:right;">' + scoreDisplay + '</span>';
        }
        html += '<span class="badge ' + statusClass + '" style="font-size:0.75rem;">' + statusText + '</span>';
        html += '</div>';
        if (m.id === 'speaking') {
            const practiced = getSpeakingPracticedCount(modSessions);
            const totalQ = getSpeakingTotalQuestions(modSessions);
            html += '<div style="margin-top:6px; color:#666; font-size:0.8rem;">已练 ' + practiced + (totalQ > 0 ? (' / ' + totalQ) : '') + ' 题；AI评分 ' + moduleRecords.length + ' 次，达标 ' + passCount + ' 次</div>';
        } else if (isStudyOnlyModule(m)) {
            html += '<div style="margin-top:6px; color:#666; font-size:0.8rem;">仅练习，不计测试</div>';
        } else {
            html += '<div style="margin-top:6px; color:#666; font-size:0.8rem;">测试 ' + moduleRecords.length + ' 次，达标 ' + passCount + ' 次</div>';
        }
        html += '</td>';
        html += '<td style="padding:15px 12px; text-align:center; color:#667eea;">' + formatDuration(modSeconds) + '</td>';
        html += '<td style="padding:15px 12px; text-align:center;">';
        html += '<div class="student-actions progress-actions">';

        if (isBuiltinDictationModule(m.id)) {
            html += '<button class="btn btn-study" onclick="openListeningIframe(\'' + m.id + '\')">学习</button>';
            html += '<button class="btn btn-sm btn-secondary" onclick="startTest(\'random\', \'' + m.id + '\')">测试</button>';
            html += '<button class="btn btn-sm btn-success" onclick="openWrongBook(\'' + m.id + '\')">' + wrongBookButtonLabel(m.id) + '</button>';
        } else if (m.id === 'writing_correction') {
            const writingUnseen = Number(window._writingUnseenCount || 0);
            const historyLabel = writingUnseen > 0 ? ('历史 · ' + writingUnseen + '新') : '历史';
            html += '<button class="btn btn-study" onclick="openGenericIframe(\'' + m.id + '\', \'' + m.name + '\', \'' + m.url + '\', \'study\')">作文批改</button>';
            html += '<button class="btn btn-sm btn-success" onclick="openWritingCorrectionHistory()">' + historyLabel + '</button>';
        } else {
            if (m.url) {
                html += '<button class="btn btn-study" onclick="openGenericIframe(\'' + m.id + '\', \'' + m.name + '\', \'' + m.url + '\', \'study\')">' + (isStudyOnlyModule(m) ? '练习' : '学习') + '</button>';
            } else {
                html += '<button class="btn btn-study" disabled title="该模块暂未配置学习页面">学习待接入</button>';
            }
            if (!isStudyOnlyModule(m)) {
                if (m.test_url) {
                    html += '<button class="btn btn-sm btn-secondary" onclick="openGenericIframe(\'' + m.id + '\', \'' + m.name + '\', \'' + m.test_url + '\', \'test\')">测试</button>';
                } else {
                    html += '<button class="btn btn-sm btn-secondary" disabled title="该模块暂未配置测试页面">测试待接入</button>';
                }
                if (hasWrongBook(m)) {
                    html += '<button class="btn btn-sm btn-success" onclick="openWrongBook(\'' + m.id + '\')">' + wrongBookButtonLabel(m.id) + '</button>';
                } else {
                    html += '<button class="btn btn-sm btn-success" onclick="switchStudentTab(\'history\')">历史</button>';
                }
            }
        }
        html += '</div></td></tr>';
    }

    html += '</tbody></table>';
    const overallProgress = testableModules.length > 0 ? Math.round(totalProgressForTests / testableModules.length) : 0;
    const passedRecords = records.filter(function(r) { return !!r.is_passed; }).length;
    html += '<div style="margin-top:30px; padding:20px; background:#f8f9fa; border-radius:10px;">';
    html += '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:16px; text-align:center;">';
    html += '<div><div style="font-size:1.4rem; font-weight:bold; color:#667eea;">' + records.length + '</div><div style="color:#666; font-size:0.9rem;">总测试次数</div></div>';
    html += '<div><div style="font-size:1.4rem; font-weight:bold; color:#28a745;">' + overallProgress + '%</div><div style="color:#666; font-size:0.9rem;">测试汇总进度</div></div>';
    html += '<div><div style="font-size:1.4rem; font-weight:bold; color:#11998e;">' + (records.length > 0 ? Math.round(passedRecords / records.length * 100) : 0) + '%</div><div style="color:#666; font-size:0.9rem;">总达标率</div></div>';
    html += '<div><div style="font-size:1.4rem; font-weight:bold; color:#764ba2;">' + formatDuration(totalStudySeconds) + '</div><div style="color:#666; font-size:0.9rem;">总练习时长</div></div>';
    html += '<div><div style="font-size:1.4rem; font-weight:bold; color:#dc3545;">' + formatDuration(todayStudySeconds) + '</div><div style="color:#666; font-size:0.9rem;">今日练习时长</div></div>';
    html += '</div><div style="margin-top:12px;color:#666;font-size:0.9rem;">待复习错题：' + wrongCount + ' 个。各科点「错题本」复习。练习时长含学习与测试，5分钟无操作自动停表。</div></div>';

    container.innerHTML = html;
}

async function loadStudentHistory() {
    const result = await apiFetch('/api/student/test-records');
    const container = document.getElementById('studentHistoryList');
    const records = result.data;
    
    if (!records || records.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">暂无测试记录</p>';
        document.getElementById('historyChart').innerHTML = '';
        return;
    }
    
    let html = '';
    for (let i = 0; i < records.length; i++) {
        const r = records[i];
        const module = getModuleById(r.module_type);
        const moduleName = r.module_name || (module ? module.name : normalizeModuleType(r.module_type));
        const typeText = window.TrackingUtils.getTestTypeLabel(r.test_type);
        const dateStr = new Date(r.created_at).toLocaleString('zh-CN');
        const color = r.is_passed ? 'color:#28a745;' : 'color:#dc3545;';
        const badgeClass = r.is_passed ? 'badge-success' : 'badge-danger';
        const statusText = r.is_passed ? '达标' : '未达标';
        const wrongWords = window.TrackingUtils.getWrongWordDetails(r.details);
        const wrongCount = Math.max(0, Number(r.total_count) - Number(r.correct_count));
        const wrongWordList = wrongWords.map(function(w) { return w.word; }).join(',');
        
        html += '<div style="padding:15px;border-bottom:1px solid #eee; cursor:pointer;" onclick="toggleHistoryDetail(' + i + ')">';
        html += '<div style="display:flex;justify-content:space-between;align-items:center;">';
        html += '<div><span style="font-weight:600;">' + escapeHtml(moduleName) + '</span>';
        html += '<span class="badge badge-info" style="margin-left:8px;">' + escapeHtml(typeText) + '</span>';
        html += '<span style="color:#666;font-size:0.85rem;margin-left:10px;">' + escapeHtml(dateStr) + '</span></div>';
        html += '<div><span style="font-size:1.2rem;font-weight:bold;' + color + '">' + r.score + '%</span>';
        html += '<span class="badge ' + badgeClass + '" style="margin-left:10px;">' + statusText + '</span></div>';
        html += '</div>';
        html += '<div style="margin-top:8px;font-size:0.85rem;color:#666;">';
        html += '<span style="color:#28a745;">正确: ' + r.correct_count + '/' + r.total_count + '</span>';
        html += ' <span style="color:#dc3545;margin-left:10px;">错题: ' + wrongCount + '个</span>';
        html += ' <span style="color:#666;margin-left:10px;">达标线: ' + r.pass_threshold + '%</span>';
        if (Number(r.duration_seconds) > 0) {
            html += ' <span style="color:#666;margin-left:10px;">测试时长: ' + escapeHtml(formatDuration(r.duration_seconds)) + '</span>';
        }
        if (wrongWords.length > 0) {
            html += ' <span style="color:#667eea;margin-left:10px;">(点击查看详情)</span>';
        }
        html += '</div>';
        
        if (wrongWordList) {
            html += '<div style="margin-top:10px;">';
            html += '<button class="btn btn-sm" style="padding:6px 16px;font-size:0.85rem;" onclick="event.stopPropagation();startWrongWordsTestFromHistory(\'' + escapeJsString(wrongWordList) + '\', \'' + escapeJsString(normalizeModuleType(r.module_type || 'dictation')) + '\')">测错题</button>';
            html += '</div>';
        }
        
        // 错题详情区域
        if (wrongWords.length > 0) {
            html += '<div id="historyDetail_' + i + '" style="display:none;margin-top:12px;padding:12px;background:#fff3cd;border-radius:8px;">';
            html += '<div style="font-weight:600;margin-bottom:8px;color:#856404;">错题详情:</div>';
            for (let j = 0; j < wrongWords.length; j++) {
                const w = wrongWords[j];
                html += '<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px dashed #e0d6b8;">';
                html += '<div><span style="font-weight:600;color:#333;">' + escapeHtml(w.word) + '</span>';
                if (w.phonetic) {
                    html += ' <span style="color:#666;font-size:0.85rem;">' + escapeHtml(w.phonetic) + '</span>';
                }
                html += '</div>';
                html += '<div style="color:#dc3545;font-size:0.9rem;">你的答案: ' + escapeHtml(w.userAnswer || '未作答') + '</div>';
                html += '</div>';
            }
            html += '</div>';
        }
        
        html += '</div>';
    }
    container.innerHTML = html;
    
    // 简单图表
    const reversed = records.slice(0, 20).reverse();
    let chartHtml = '<div style="display:flex;align-items:flex-end;height:150px;padding:10px;background:#f8f9fa;border-radius:10px;">';
    for (let i = 0; i < reversed.length; i++) {
        const r = reversed[i];
        const height = r.score / 100 * 150;
        const color = r.is_passed ? '#28a745' : '#dc3545';
        chartHtml += '<div style="flex:1;display:flex;flex-direction:column;align-items:center;">';
        chartHtml += '<div style="width:20px;background:' + color + ';height:' + height + 'px;min-height:5px;border-radius:5px 5px 0 0;"></div>';
        chartHtml += '<span style="font-size:0.7rem;color:#666;margin-top:5px;">' + r.score + '%</span></div>';
    }
    chartHtml += '</div>';
    document.getElementById('historyChart').innerHTML = chartHtml;
}

function toggleHistoryDetail(index) {
    const detailDiv = document.getElementById('historyDetail_' + index);
    if (detailDiv) {
        detailDiv.style.display = detailDiv.style.display === 'none' ? 'block' : 'none';
    }
}

function wrongBookButtonLabel(moduleId) {
    const n = Number((window._wrongBookCounts || {})[moduleId] || 0);
    return n > 0 ? ('错题本 · ' + n) : '错题本';
}

function extractWrongItemResults(moduleType, details) {
    const list = Array.isArray(details) ? details : [];
    const out = [];
    for (let i = 0; i < list.length; i++) {
        const item = list[i] || {};
        if (moduleType === 'reading_synonym') {
            const key = String(item.item_key != null ? item.item_key : (item.srcIndex != null ? item.srcIndex : ''));
            if (!key) continue;
            out.push({
                item_key: key,
                title: item.title || ((item.words && item.words[0]) || key),
                payload: { words: item.words || [], marked: item.marked || item.wrongClicks || [] },
                is_correct: !!item.is_correct,
                skipped: !!item.skipped
            });
        } else if (moduleType === 'sentence') {
            const key = String(item.item_key != null ? item.item_key : (item.num != null ? item.num : ''));
            if (!key) continue;
            out.push({
                item_key: key,
                title: item.title || item.original || key,
                payload: { num: item.num, original: item.original || '', pattern: item.pattern || '' },
                is_correct: !!item.is_correct,
                skipped: !!item.skipped
            });
        } else if (moduleType === 'listening_synonym') {
            const key = String(item.item_key != null ? item.item_key : (item.id != null ? item.id : ''));
            if (!key) continue;
            const ok = item.is_correct != null ? !!item.is_correct : !!item.isCorrect;
            out.push({
                item_key: key,
                title: item.title || item.original || key,
                payload: { id: item.id || Number(key), original: item.original || item.title || '' },
                is_correct: ok,
                skipped: !!item.skipped
            });
        } else if (moduleType === 'writing_phrase') {
            const key = String(item.item_key || item.en || '');
            if (!key) continue;
            out.push({
                item_key: key,
                title: item.title || item.zh || key,
                payload: { zh: item.zh || item.title || '', en: item.en || key },
                is_correct: !!item.correct || !!item.is_correct,
                skipped: !!item.skipped
            });
        } else if (moduleType === 'writing_translate') {
            const key = String(item.item_key != null ? item.item_key : (item.id != null ? item.id : ''));
            if (!key) continue;
            out.push({
                item_key: key,
                title: item.title || item.en || key,
                payload: { id: item.id || Number(key), zh: item.zh || '', en: item.en || item.title || '' },
                is_correct: !!item.correct || !!item.is_correct,
                skipped: !!item.skipped
            });
        }
    }
    return out;
}

function ensureWrongBookScreen() {
    if (document.getElementById('wrongBookScreen')) return;
    const el = document.createElement('div');
    el.id = 'wrongBookScreen';
    el.className = 'screen';
    el.innerHTML =
        '<div class="card wrong-book-card">' +
            '<div class="wrong-book-head">' +
                '<button type="button" class="btn btn-sm btn-secondary" onclick="closeWrongBook()">返回</button>' +
                '<h2 id="wrongBookTitle">错题本</h2>' +
            '</div>' +
            '<p class="wrong-book-sub" id="wrongBookSub"></p>' +
            '<div class="wrong-book-actions" id="wrongBookActions"></div>' +
            '<div id="wrongBookList"></div>' +
        '</div>';
    const host = document.querySelector('.container') || document.body;
    host.appendChild(el);
}

async function openWrongBook(moduleId) {
    const m = getModuleById(moduleId);
    if (!m || !hasWrongBook(m)) {
        showToast('该科目没有错题本', 'info');
        return;
    }
    window._wrongBookModuleId = m.id;
    ensureWrongBookScreen();
    showScreen('wrongBookScreen');
    document.getElementById('wrongBookTitle').textContent = m.name + ' · 错题本';
    document.getElementById('wrongBookSub').textContent = '连对 3 次后移出；再错则连对清零。';
    document.getElementById('wrongBookList').innerHTML = '<p style="color:#666;padding:20px;text-align:center;">加载中…</p>';
    document.getElementById('wrongBookActions').innerHTML = '';
    const result = await apiFetch('/api/student/wrong-items?module_type=' + encodeURIComponent(m.id) + '&unmastered=1');
    if (result.error) {
        document.getElementById('wrongBookList').innerHTML = '<p style="color:#dc3545;padding:20px;text-align:center;">' + escapeHtml((result.error && result.error.message) || '加载失败') + '</p>';
        return;
    }
    const items = result.data || [];
    window._wrongBookItems = items;
    const size = WRONG_BOOK_TEST_SIZE[m.id] || 10;
    let actions = '';
    if (items.length > 0) {
        actions += '<button class="btn btn-sm btn-secondary" onclick="startWrongBookTest(\'' + m.id + '\')">开始测试（每次 ' + size + ' 题）</button>';
    }
    document.getElementById('wrongBookActions').innerHTML = actions;
    if (items.length === 0) {
        document.getElementById('wrongBookList').innerHTML = '<p style="color:#666;padding:24px;text-align:center;">暂无错题</p>';
        return;
    }
    let html = '<div class="wrong-book-count">待复习 ' + items.length + ' 条</div>';
    html += '<div class="wrong-book-catalog">';
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const streak = Number(item.correct_streak || 0);
        const payload = item.payload || {};
        let extra = '';
        if (m.id === 'reading_synonym' && payload.words && payload.words.length) {
            extra += '<div class="wrong-book-words">';
            for (let w = 0; w < payload.words.length; w++) {
                const word = payload.words[w];
                const marked = (payload.marked || []).indexOf(word) >= 0;
                extra += '<span class="wrong-book-word' + (marked ? ' marked' : '') + '">' + escapeHtml(word) + '</span>';
            }
            extra += '</div>';
        }
        const clickable = m.id === 'listening_synonym';
        html += '<div class="wrong-book-item"' + (clickable ? ' onclick="openWrongBookLearn(\'' + m.id + '\',\'' + escapeJsString(item.item_key) + '\')"' : '') + '>';
        html += '<div class="wrong-book-item-title">' + escapeHtml(item.title || item.item_key) + '</div>';
        if (m.id === 'writing_phrase' && payload.en) {
            html += '<div class="wrong-book-item-sub">' + escapeHtml(payload.en) + '</div>';
        }
        if (m.id === 'writing_translate' && payload.zh) {
            html += '<div class="wrong-book-item-sub">' + escapeHtml(payload.zh) + '</div>';
        }
        extra && (html += extra);
        html += '<div class="wrong-book-meta">连对 ' + streak + ' / 3</div>';
        if (clickable) html += '<div class="wrong-book-hint">点击按学习模式练这一句</div>';
        html += '</div>';
    }
    html += '</div>';
    document.getElementById('wrongBookList').innerHTML = html;
}

function closeWrongBook() {
    window._wrongBookModuleId = null;
    showStudentHome();
}

function startWrongBookTest(moduleId) {
    const m = getModuleById(moduleId);
    if (!m) return;
    window._wrongBookReturn = moduleId;
    if (isBuiltinDictationModule(moduleId)) {
        startTest('wrong_words', moduleId);
        return;
    }
    if (!m.test_url) {
        showToast('该科目没有测试页', 'info');
        return;
    }
    const joiner = m.test_url.indexOf('?') >= 0 ? '&' : '?';
    openGenericIframe(m.id, m.name, m.test_url + joiner + 'wrongbook=1', 'test');
}

function openWrongBookLearn(moduleId, itemKey) {
    const m = getModuleById(moduleId);
    if (!m || !m.url) return;
    window._wrongBookReturn = moduleId;
    const joiner = m.url.indexOf('?') >= 0 ? '&' : '?';
    openGenericIframe(m.id, m.name, m.url + joiner + 'qid=' + encodeURIComponent(itemKey), 'study');
}

async function startWrongWordsTestFromHistory(wordListStr, moduleId) {
    if (!wordListStr) {
        showToast('没有错题可练习', 'info');
        return;
    }
    const words = wordListStr.split(',').filter(function(w) { return w.trim(); });
    if (words.length === 0) {
        showToast('没有错题可练习', 'info');
        return;
    }
    unlockAudio();
    testStartTime = Date.now();
    currentDictationModuleId = normalizeModuleType(moduleId || currentDictationModuleId || 'dictation');
    currentTestMode = 'wrong_words';
    document.getElementById('testModeLabel').textContent = '历史错题测试';
    document.getElementById('testModeLabel').style.background = '#f8d7da';
    testWords = words;
    testResults = [];
    currentTestIndex = 0;
    showScreen('testScreen');
    showQuestion();
}

function studentLogout() {
    currentStudent = null;
    clearStudentSession();
    authLogout('student').finally(function() {
        showScreen('studentLoginScreen');
        document.getElementById('studentId').value = '';
        document.getElementById('studentPassword').value = '';
    });
}

function showChangePasswordModal(force) {
    forcePasswordChange = !!force;
    var modal = document.getElementById('changePasswordModal');
    if (modal) {
        var hint = modal.querySelector('#changePasswordHint');
        if (!hint) {
            hint = document.createElement('p');
            hint.id = 'changePasswordHint';
            hint.style.cssText = 'color:#666;font-size:0.9rem;margin-bottom:12px;line-height:1.5;';
            var header = modal.querySelector('.modal-header');
            if (header && header.parentNode) {
                header.parentNode.insertBefore(hint, header.nextSibling);
            }
        }
        hint.textContent = forcePasswordChange
            ? '教师已重置密码或首次登录，请设置新密码（至少4位）后才能进入学习。'
            : '';
        hint.style.display = forcePasswordChange ? 'block' : 'none';
        var closeBtn = modal.querySelector('.modal-close');
        var cancelBtn = modal.querySelector('#changePasswordCancelBtn');
        if (closeBtn) closeBtn.style.display = forcePasswordChange ? 'none' : '';
        if (cancelBtn) cancelBtn.style.display = forcePasswordChange ? 'none' : '';
    }
    showModal('changePasswordModal');
}

var _closeModalForStudent = closeModal;
closeModal = function(modalId) {
    if (modalId === 'changePasswordModal' && forcePasswordChange) {
        showToast('请先设置新密码', 'error');
        return;
    }
    _closeModalForStudent(modalId);
};

async function changePassword() {
    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;
    if (!newPwd || newPwd.length < 4) { showToast('密码至少4位', 'error'); return; }
    if (newPwd !== confirmPwd) { showToast('两次密码不一致', 'error'); return; }
    const result = await apiFetch('/api/student/change-password', {
        method: 'POST',
        body: JSON.stringify({ password: newPwd })
    });
    if (result.error) { showToast((result.error && result.error.message) || '修改失败', 'error'); return; }
    if (result.data && result.data.student) {
        currentStudent = result.data.student;
        rememberStudentSession(result.data.student);
    } else {
        currentStudent.is_password_changed = true;
    }
    // 必须先清强制改密标记，否则包装过的 closeModal 会拦截并提示「请先设置新密码」
    forcePasswordChange = false;
    closeModal('changePasswordModal');
    showToast('密码修改成功', 'success');
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';
    if (!document.getElementById('studentHome').classList.contains('active')) {
        showStudentHome();
    }
}


function unlockAudio() {
    if (audioUnlocked) return;
    audioUnlocked = true;
    // 播放一个无声音频来解锁
    var silentAudio = new Audio('data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=');
    silentAudio.play().catch(function(){});
    // 同时解锁 speechSynthesis
    if (window.speechSynthesis) {
        var u = new SpeechSynthesisUtterance('');
        u.volume = 0;
        speechSynthesis.speak(u);
    }
    console.log('音频上下文已解锁');
}

var _practiceClock = null;
var _practiceIdleUnbinds = [];

function startPracticeClock() {
    stopPracticeClock();
    if (!window.TrackingUtils || typeof window.TrackingUtils.createIdleClock !== 'function') return;
    _practiceClock = window.TrackingUtils.createIdleClock();
    _practiceClock.touch();
    _practiceIdleUnbinds.push(window.TrackingUtils.bindIdleClock(document, _practiceClock));
}

function bindIframePracticeClock(iframe) {
    if (!iframe || !_practiceClock || !window.TrackingUtils) return;
    function bindDoc() {
        try {
            var doc = iframe.contentDocument;
            if (!doc) return;
            _practiceIdleUnbinds.push(window.TrackingUtils.bindIdleClock(doc, _practiceClock));
        } catch (e) {}
    }
    iframe.addEventListener('load', bindDoc);
    bindDoc();
}

function practiceElapsedSeconds(startedAt) {
    if (_practiceClock) return _practiceClock.elapsedSeconds();
    if (!startedAt) return 0;
    return Math.max(0, Math.round((Date.now() - startedAt) / 1000));
}

function stopPracticeClock() {
    while (_practiceIdleUnbinds.length) {
        var unbind = _practiceIdleUnbinds.pop();
        try { if (typeof unbind === 'function') unbind(); } catch (e) {}
    }
    if (_practiceClock) {
        try { _practiceClock.stop(); } catch (e) {}
    }
    _practiceClock = null;
}

function wordsFromWrongBookCache() {
    const cached = window._wrongBookItems;
    if (!cached || !cached.length) return [];
    return cached.map(function(item) {
        return String((item && (item.word || item.item_key || item.title)) || '').trim();
    }).filter(Boolean);
}

async function startTest(mode, moduleId) {
    // 用户点击了开始测试，解锁音频
    unlockAudio();
    isPlaying = false;
    testStartTime = Date.now(); // 记录测试开始时间
    startPracticeClock();
    currentDictationModuleId = normalizeModuleType(moduleId || currentDictationModuleId || 'dictation');
    const dictation = getBuiltinDictation(currentDictationModuleId);
    const bank = dictation.words;
    
    currentTestMode = mode;
    document.getElementById('testModeLabel').textContent = mode === 'random' ? '随机测试' : '错题测试';
    document.getElementById('testModeLabel').style.background = mode === 'random' ? '#e9ecef' : '#d4edda';
    if (mode === 'random') {
        testWords = shuffleArray(bank.slice()).slice(0, 50);
    } else {
        // 错题本目录已经拉过清单：同步开测，避免 await 丢掉点击手势导致没声音
        testWords = wordsFromWrongBookCache();
        if (!testWords.length) {
            const result = await apiFetch('/api/student/wrong-words?module_type=' + encodeURIComponent(currentDictationModuleId) + '&unmastered=1');
            if (result.error) {
                showToast((result.error && result.error.message) || '加载错题失败', 'error');
                return;
            }
            if (!result.data || result.data.length === 0) {
                showToast('暂无错题可练习', 'info');
                return;
            }
            testWords = result.data.map(function(w) { return w.word; });
        }
        if (window._wrongBookReturn) {
            const size = WRONG_BOOK_TEST_SIZE[currentDictationModuleId] || 10;
            testWords = shuffleArray(testWords.slice()).slice(0, size);
        } else if (testWords.length < 50) {
            const more = shuffleArray(bank.filter(function(w) { return testWords.indexOf(w) === -1; })).slice(0, 50 - testWords.length);
            testWords = testWords.concat(more);
        }
    }
    testResults = [];
    currentTestIndex = 0;
    isSaving = false;
    testFinished = false;
    showScreen('testScreen');
    showQuestion();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        const temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

function showQuestion() {
    document.getElementById('questionCounter').textContent = '第 ' + (currentTestIndex + 1) + ' / ' + testWords.length + ' 题';
    document.getElementById('progressFill').style.width = ((currentTestIndex + 1) / testWords.length * 100) + '%';
    document.getElementById('answerInput').value = '';
    document.getElementById('timerDisplay').textContent = '准备中...';
    document.getElementById('timerDisplay').className = '';
    document.getElementById('statusIcon').textContent = '';
    document.getElementById('statusIcon').className = '';
    playWord();
}

var audioEl = new Audio();
var timerStarted = false;
var playTimeout = null; // 存储播放超时 ID
var testStartTime = 0; // 测试开始时间

function getDictationAudioBase() {
    var dictation = getBuiltinDictation(currentDictationModuleId);
    return (dictation && dictation.audioBase) ? dictation.audioBase : 'audio/words/';
}

function finishPlayWord() {
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    isPlaying = false;
    safeStartTimer();
}

function speakDictationWord(word, onDone) {
    if (!window.speechSynthesis) {
        if (onDone) onDone();
        return;
    }
    try { speechSynthesis.cancel(); } catch (e) {}
    var uttered = new SpeechSynthesisUtterance(word);
    uttered.lang = 'en-GB';
    uttered.rate = 0.85;
    uttered.onend = function() { if (onDone) onDone(); };
    uttered.onerror = function() { if (onDone) onDone(); };
    try {
        speechSynthesis.speak(uttered);
    } catch (e) {
        if (onDone) onDone();
    }
}

function playWord() {
    if (isPlaying) return;
    isPlaying = true;
    timerStarted = false;
    // 取消上一题的 timeout 和计时器
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    var word = testWords[currentTestIndex];
    var usedFallback = false;
    
    // 超时保护：6秒后强制开始计时
    playTimeout = setTimeout(function() {
        if (isPlaying) {
            try { audioEl.pause(); } catch(e) {}
            try { speechSynthesis.cancel(); } catch(e) {}
            finishPlayWord();
        }
    }, 6000);

    function fallbackToTts() {
        if (usedFallback) return;
        usedFallback = true;
        speakDictationWord(word, finishPlayWord);
    }

    // 本地有 MP3 就播文件，没有则退回浏览器朗读
    var localUrl = getDictationAudioBase() + encodeURIComponent(word) + '.mp3';
    audioEl.onended = function() { finishPlayWord(); };
    audioEl.onerror = fallbackToTts;
    audioEl.src = localUrl;
    audioEl.play().catch(fallbackToTts);
}

// 安全启动计时器（每题只启动一次）
function safeStartTimer() {
    if (timerStarted) return;
    timerStarted = true;
    startTimer();
}

function startTimer() {
    timeLeft = 6;
    updateTimerDisplay();
    timerInterval = setInterval(function() {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById('timerDisplay').textContent = '时间到！';
            setTimeout(autoSubmit, 800);
        }
    }, 1000);
}

function updateTimerDisplay() {
    const display = document.getElementById('timerDisplay');
    display.textContent = '剩余 ' + timeLeft + ' 秒';
    display.className = timeLeft <= 2 ? 'fail' : '';
}

function autoSubmit() {
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    isPlaying = false;
    timerStarted = false; // 重置，让下一题正常启动
    try { audioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const userAnswer = document.getElementById('answerInput').value.trim().toLowerCase();
    const correctAnswer = testWords[currentTestIndex].toLowerCase();
    const isCorrect = userAnswer === correctAnswer;
    testResults.push({
        word: testWords[currentTestIndex],
        userAnswer: userAnswer || '(未作答)',
        isCorrect: isCorrect,
        skipped: userAnswer === ''
    });
    nextQuestion();
}

function submitAnswer() {
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    isPlaying = false;
    timerStarted = false; // 重置，让下一题正常启动
    try { audioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const userAnswer = document.getElementById('answerInput').value.trim().toLowerCase();
    const correctAnswer = testWords[currentTestIndex].toLowerCase();
    const isCorrect = userAnswer === correctAnswer;
    testResults.push({
        word: testWords[currentTestIndex],
        userAnswer: userAnswer || '(未作答)',
        isCorrect: isCorrect,
        skipped: userAnswer === ''
    });
    nextQuestion();
}

function skipWord() {
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    isPlaying = false;
    timerStarted = false; // 重置，让下一题正常启动
    try { audioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    testResults.push({
        word: testWords[currentTestIndex],
        userAnswer: '(跳过)',
        isCorrect: false,
        skipped: true
    });
    nextQuestion();
}

function nextQuestion() {
    currentTestIndex++;
    if (currentTestIndex >= testWords.length) {
        finishTest();
    } else {
        showQuestion();
    }
}

let isSaving = false;
var testFinished = false;

async function finishTest() {
    // 防止重复提交（含结果页再次触发）：避免错题本被重复累加
    if (isSaving || testFinished) {
        console.log('正在保存中或已完成，请勿重复提交');
        return;
    }
    isSaving = true;
    
    const correctCount = testResults.filter(function(r) { return r.isCorrect; }).length;
    const incorrectCount = testResults.filter(function(r) { return !r.isCorrect && !r.skipped; }).length;
    const skippedCount = testResults.filter(function(r) { return r.skipped; }).length;
    const score = Math.round((correctCount / testResults.length) * 100);
    
    const dictation = getBuiltinDictation(currentDictationModuleId);
    const threshold = await getPassThreshold(dictation.id, currentStudent);
    const isPassed = score >= threshold;

    const durationSeconds = practiceElapsedSeconds(testStartTime);
    const insertResult = await saveModuleTestRecord({
        student_id: currentStudent.student_id,
        module_type: dictation.id,
        module_name: dictation.name,
        test_type: currentTestMode,
        score_percent: score,
        correct_count: correctCount,
        total_count: testResults.length,
        is_passed: isPassed,
        pass_threshold: threshold,
        duration_seconds: durationSeconds,
        started_at: testStartTime > 0 ? new Date(testStartTime).toISOString() : null,
        ended_at: new Date().toISOString(),
        details: testResults
    });
    
    if (insertResult.error) {
        console.error('保存测试记录失败:', insertResult.error);
        showToast('保存测试记录失败: ' + insertResult.error.message, 'error');
        isSaving = false;
        return;
    }

    testFinished = true;
    stopPracticeClock();
    
    let newWrongCount = 0;
    const applyResult = await applyDictationWrongBookResults(testResults, dictation.id);
    if (applyResult && applyResult.error) {
        console.error('同步错题失败:', applyResult.error);
        showToast('测试已保存，但错题同步失败', 'error');
    } else {
        newWrongCount = Number((applyResult && applyResult.data && applyResult.data.new_wrong_count) || 0);
    }
    
    showScreen('resultScreen');
    document.getElementById('resultStudentInfo').textContent = currentStudent.name + ' - ' + dictation.name;
    document.getElementById('resultPassStatus').className = 'pass-status ' + (isPassed ? 'pass' : 'fail');
    document.getElementById('resultPassStatus').textContent = isPassed ? '达标！' : '未达标';
    document.getElementById('resultScore').textContent = score + '%';
    document.getElementById('resultThreshold').textContent = threshold + '%';
    document.getElementById('resultCorrect').textContent = correctCount;
    document.getElementById('resultIncorrect').textContent = incorrectCount;
    document.getElementById('resultSkipped').textContent = skippedCount;
    document.getElementById('resultWrongCount').textContent = newWrongCount;
    
    const errors = testResults.filter(function(r) { return !r.isCorrect; });
    let errorHtml = '';
    if (errors.length > 0) {
        errorHtml = '<h4 style="margin-top:20px;">错误/跳过单词</h4><div class="error-list">';
        for (let i = 0; i < errors.length; i++) {
            errorHtml += '<div class="error-item"><span>' + errors[i].word + '</span><span style="color:#666;">你的答案: ' + errors[i].userAnswer + '</span></div>';
        }
        errorHtml += '</div>';
    } else {
        errorHtml = '<p style="text-align:center;color:#28a745;padding:20px;">太棒了！全部正确！</p>';
    }
    document.getElementById('resultErrorList').innerHTML = errorHtml;
    
    isSaving = false;
}

function downloadResult() {
    const correctCount = testResults.filter(function(r) { return r.isCorrect; }).length;
    const score = Math.round((correctCount / testResults.length) * 100);
    const errors = testResults.filter(function(r) { return !r.isCorrect; });
    let content = '英语听写测试结果\n';
    content += '学生：' + currentStudent.name + '\n';
    content += '学号：' + currentStudent.student_id + '\n';
    content += '目标分数：' + currentStudent.target_score + '分\n';
    content += '测试类型：' + (currentTestMode === 'random' ? '随机测试' : '错题测试') + '\n';
    content += '正确率：' + score + '%\n';
    content += '正确：' + correctCount + ' 错误：' + errors.length + ' 跳过：' + testResults.filter(function(r) { return r.skipped; }).length + '\n';
    content += '\n错误单词：\n';
    for (let i = 0; i < errors.length; i++) {
        content += (i + 1) + '. ' + errors[i].word + ' (你的答案: ' + errors[i].userAnswer + ')\n';
    }
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '听写结果_' + currentStudent.name + '_' + new Date().toISOString().slice(0,10) + '.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function backToStudentHome() {
    const returnId = window._wrongBookReturn;
    window._wrongBookReturn = null;
    if (returnId) {
        openWrongBook(returnId);
        return;
    }
    showStudentHome();
}

function applyDictationWrongBookResults(results, moduleId) {
    if (!results || !results.length) return Promise.resolve(null);
    return apiFetch('/api/student/wrong-words/apply', {
        method: 'POST',
        body: JSON.stringify({
            module_type: moduleId,
            results: results.map(function(r) {
                return {
                    word: r.word,
                    is_correct: !!r.isCorrect,
                    skipped: !!r.skipped
                };
            })
        })
    });
}

async function cancelTestAndReturn() {
    if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    isPlaying = false;
    timerStarted = false;
    var dictation = getBuiltinDictation(currentDictationModuleId);
    var pendingApply = (testResults && testResults.length)
        ? applyDictationWrongBookResults(testResults, dictation.id)
        : null;
    var elapsed = practiceElapsedSeconds(testStartTime);
    if (elapsed >= 3 && currentStudent) {
        saveStudySession({
            student_id: currentStudent.student_id,
            module_type: dictation.id,
            module_name: dictation.name,
            session_kind: 'test',
            duration_seconds: elapsed,
            started_at: testStartTime > 0 ? new Date(testStartTime).toISOString() : null,
            ended_at: new Date().toISOString()
        }).catch(function(e) { console.error('保存中途退出测试时长失败:', e); });
    }
    testStartTime = 0;
    stopPracticeClock();
    try {
        audioEl.pause();
        audioEl.currentTime = 0;
    } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const answerInput = document.getElementById('answerInput');
    if (answerInput) {
        answerInput.value = '';
    }
    if (pendingApply) {
        try {
            const applyResult = await pendingApply;
            if (applyResult && applyResult.error) {
                console.error('同步错题失败:', applyResult.error);
            }
        } catch (e) {
            console.error('同步错题失败:', e);
        }
        try { loadProgressTable(); } catch (e) {}
    }
    backToStudentHome();
}

// ==================== 学习功能 ====================

var learnSession = null;
var learnTimerInterval = null;
var learnStartTime = null;

// 学习状态管理
function initLearnSession() {
    return {
        phase: 'initial', // initial, group_practice, group_test, final_review
        words: [],
        wrongWords: [],
        currentGroups: [],
        currentGroupIndex: 0,
        currentWordIndex: 0,
        practiceAttempts: {}, // word -> count
        groupTestResults: [],
        finalReviewResults: [],
        initialCorrect: 0,
        initialWrong: 0,
        masteredInSession: 0,
        completedGroups: 0,
        startTime: Date.now()
    };
}

// 显示学习界面
async function showLearnScreen() {
    showScreen('learnScreen');
    await loadLearnStats();
    startLearnTimer();
}

// 退出学习
function exitLearn() {
    stopLearnTimer();
    stopPracticeClock();
    if (learnSession && learnSession.phase !== 'initial') {
        saveLearnProgress();
    }
    showStudentHome();
}

// 学习计时器
function startLearnTimer() {
    learnStartTime = Date.now();
    startPracticeClock();
    learnTimerInterval = setInterval(updateLearnTimer, 1000);
}

function stopLearnTimer() {
    if (learnTimerInterval) {
        clearInterval(learnTimerInterval);
        learnTimerInterval = null;
    }
}

function updateLearnTimer() {
    const elapsed = practiceElapsedSeconds(learnStartTime);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    document.getElementById('learnTime').textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}

// 加载学习统计
async function loadLearnStats() {
    const result = await apiFetch('/api/student/word-mastery');
    if (result.error) {
        console.error('加载学习统计失败:', result.error);
        return;
    }
    const masteryData = result.data || [];
    
    let mastered = 0, learning = 0, notStarted = 0;
    
    // 已掌握：初始正确或对过3次
    mastered = masteryData.filter(m => m.is_initial_correct || m.correct_count >= 3).length;
    
    // 学习中：初始错且对过1-2次
    learning = masteryData.filter(m => !m.is_initial_correct && m.correct_count >= 1 && m.correct_count < 3).length;
    
    // 未接触：从未测试过
    notStarted = allWords.length - masteryData.length;
    
    document.getElementById('learnMastered').textContent = mastered;
    document.getElementById('learnLearning').textContent = learning;
    document.getElementById('learnNew').textContent = notStarted;
}

// 开始学习会话
async function startLearnSession() {
    // 用户点击了开始学习，解锁音频
    unlockAudio();
    
    learnSession = initLearnSession();
    
    // 获取学生已掌握的词汇（对过3次的）
    const masteryResult = await apiFetch('/api/student/word-mastery');
    if (masteryResult.error) {
        showToast((masteryResult.error && masteryResult.error.message) || '加载掌握数据失败', 'error');
        return;
    }
    const masteredWords = (masteryResult.data || [])
        .filter(m => m.correct_count >= 3 || m.is_initial_correct)
        .map(m => m.word);
    
    // 从未掌握或未接触的词中随机选50个
    const availableWords = allWords.filter(w => masteredWords.indexOf(w) === -1);
    learnSession.words = shuffleArray(availableWords.slice()).slice(0, 50);
    
    if (learnSession.words.length === 0) {
        showToast('太棒了！你已经掌握了所有词汇', 'success');
        return;
    }
    
    // 开始初始测试
    startInitialTest();
}

// 第一阶段：初始测试
function startInitialTest() {
    learnSession.phase = 'initial';
    learnSession.currentWordIndex = 0;
    learnSession.wrongWords = [];
    learnSession.initialCorrect = 0;
    learnSession.initialWrong = 0;
    
    document.getElementById('learnModeLabel').textContent = '初始测试';
    document.getElementById('learnModeLabel').style.background = '#e9ecef';
    showScreen('learnTestScreen');
    showLearnQuestion();
}

function showLearnQuestion() {
    const word = learnSession.words[learnSession.currentWordIndex];
    document.getElementById('learnQuestionCounter').textContent = '第 ' + (learnSession.currentWordIndex + 1) + ' / ' + learnSession.words.length + ' 题';
    document.getElementById('learnProgressFill').style.width = ((learnSession.currentWordIndex + 1) / learnSession.words.length * 100) + '%';
    document.getElementById('learnAnswerInput').value = '';
    document.getElementById('learnTimerDisplay').textContent = '准备中...';
    document.getElementById('learnTimerDisplay').className = '';
    document.getElementById('learnStatusIcon').textContent = '';
    document.getElementById('learnStatusIcon').className = '';
    
    // 播放单词（playLearnWord 会启动计时器）
    playLearnWord();
}

// 学习板块音频元素
var learnAudioEl = new Audio();
var learnTimerStarted = false;
var learnIsPlaying = false;
var learnPlayTimeout = null; // 存储播放超时 ID

function playLearnWord() {
    if (learnIsPlaying) return;
    learnIsPlaying = true;
    learnTimerStarted = false;
    // 取消上一题的 timeout 和计时器
    if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
    if (learnTimerInterval) { clearInterval(learnTimerInterval); learnTimerInterval = null; }
    
    // 根据当前阶段获取正确的单词
    let word;
    if (learnSession.phase === 'group_test') {
        word = learnSession.currentTestWords[learnSession.currentWordIndex];
    } else if (learnSession.phase === 'final_review') {
        word = learnSession.finalReviewWords[learnSession.currentWordIndex];
    } else {
        word = learnSession.words[learnSession.currentWordIndex];
    }
    
    var usedFallback = false;
    function fallbackToTts() {
        if (usedFallback) return;
        usedFallback = true;
        speakDictationWord(word, function() {
            if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
            learnIsPlaying = false;
            learnSafeStartTimer();
        });
    }
    
    // 超时保护：6秒后强制开始计时
    learnPlayTimeout = setTimeout(function() {
        if (learnIsPlaying) {
            try { learnAudioEl.pause(); } catch(e) {}
            try { speechSynthesis.cancel(); } catch(e) {}
            learnIsPlaying = false;
            learnSafeStartTimer();
        }
    }, 6000);
    
    var localUrl = getDictationAudioBase() + encodeURIComponent(word) + '.mp3';
    learnAudioEl.onended = function() { if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; } learnIsPlaying = false; learnSafeStartTimer(); };
    learnAudioEl.onerror = fallbackToTts;
    learnAudioEl.src = localUrl;
    learnAudioEl.play().catch(fallbackToTts);
}

// 学习板块安全启动计时器
function learnSafeStartTimer() {
    if (learnTimerStarted) return;
    learnTimerStarted = true;
    learnStartTimer();
}

// 学习板块启动计时器
function learnStartTimer() {
    var timeLeft = 6;
    document.getElementById('learnTimerDisplay').textContent = '剩余 ' + timeLeft + ' 秒';
    learnTimerInterval = setInterval(function() {
        timeLeft--;
        document.getElementById('learnTimerDisplay').textContent = '剩余 ' + timeLeft + ' 秒';
        if (timeLeft <= 2) {
            document.getElementById('learnTimerDisplay').className = 'fail';
        }
        if (timeLeft <= 0) {
            clearInterval(learnTimerInterval);
            learnTimerInterval = null;
            document.getElementById('learnTimerDisplay').textContent = '时间到！';
            // 根据阶段调用正确的提交函数
            setTimeout(function() {
                if (learnSession.phase === 'group_test') {
                    groupTestAutoSubmit();
                } else if (learnSession.phase === 'final_review') {
                    finalReviewAutoSubmit();
                } else {
                    learnAutoSubmit();
                }
            }, 800);
        }
    }, 1000);
}

function learnSubmitAnswer() {
    if (learnTimerInterval) { clearInterval(learnTimerInterval); learnTimerInterval = null; }
    if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
    learnIsPlaying = false;
    learnTimerStarted = false; // 重置，让下一题正常启动
    try { learnAudioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const userAnswer = document.getElementById('learnAnswerInput').value.trim().toLowerCase();
    const correctAnswer = learnSession.words[learnSession.currentWordIndex].toLowerCase();
    const isCorrect = userAnswer === correctAnswer;
    
    processLearnAnswer(isCorrect, userAnswer);
}

function learnSkipWord() {
    if (learnTimerInterval) { clearInterval(learnTimerInterval); learnTimerInterval = null; }
    if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
    learnIsPlaying = false;
    learnTimerStarted = false; // 重置，让下一题正常启动
    try { learnAudioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    processLearnAnswer(false, '(跳过)');
}

function learnAutoSubmit() {
    if (learnTimerInterval) { clearInterval(learnTimerInterval); learnTimerInterval = null; }
    if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
    learnIsPlaying = false;
    learnTimerStarted = false; // 重置，让下一题正常启动
    try { learnAudioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const userAnswer = document.getElementById('learnAnswerInput').value.trim().toLowerCase();
    const correctAnswer = learnSession.words[learnSession.currentWordIndex].toLowerCase();
    const isCorrect = userAnswer === correctAnswer && userAnswer !== '';
    processLearnAnswer(isCorrect, userAnswer || '(未作答)');
}

function processLearnAnswer(isCorrect, userAnswer) {
    const word = learnSession.words[learnSession.currentWordIndex];
    
    if (isCorrect) {
        learnSession.initialCorrect++;
        // 保存到数据库：初始正确
        saveWordMastery(word, true, true);
    } else {
        learnSession.initialWrong++;
        learnSession.wrongWords.push(word);
        // 保存到数据库：初始错误
        saveWordMastery(word, false, true);
    }
    
    learnSession.currentWordIndex++;
    
    if (learnSession.currentWordIndex < learnSession.words.length) {
        showLearnQuestion();
    } else {
        // 初始测试完成，开始分组学习
        startGroupLearning();
    }
}

// 保存单词掌握状态
async function saveWordMastery(word, isCorrect, isInitial) {
    const result = await apiFetch('/api/student/word-mastery', {
        method: 'POST',
        body: JSON.stringify({
            word: word,
            is_correct: !!isCorrect,
            is_initial: !!isInitial
        })
    });
    if (result.error) {
        console.error('保存单词掌握状态失败:', result.error);
    }
}

// 第二阶段：分组学习
function startGroupLearning() {
    if (learnSession.wrongWords.length === 0) {
        // 全对，直接完成
        showLearnResult();
        return;
    }
    
    // 分成10词一组
    learnSession.currentGroups = [];
    for (let i = 0; i < learnSession.wrongWords.length; i += 10) {
        learnSession.currentGroups.push(learnSession.wrongWords.slice(i, i + 10));
    }
    
    learnSession.currentGroupIndex = 0;
    startGroupPractice();
}

// 2.1 三次拼写练习
function startGroupPractice() {
    learnSession.phase = (learnSession.phase === 'final_practice') ? 'final_practice' : 'group_practice';
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    learnSession.currentWordIndex = 0;
    
    // 初始化练习次数
    for (let i = 0; i < group.length; i++) {
        if (!learnSession.practiceAttempts[group[i]]) {
            learnSession.practiceAttempts[group[i]] = 0;
        }
    }
    
    showPracticeScreen();
}

function showPracticeScreen() {
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    const word = group[learnSession.currentWordIndex];
    const attempts = learnSession.practiceAttempts[word] || 0;
    
    document.getElementById('practiceGroupNum').textContent = learnSession.currentGroupIndex + 1;
    document.getElementById('practiceRemaining').textContent = group.length;
    document.getElementById('practiceProgress').textContent = '(' + (attempts + 1) + '/3)';
    document.getElementById('practiceWord').textContent = word;
    document.getElementById('practiceHint').textContent = '第 ' + (learnSession.currentWordIndex + 1) + ' / ' + group.length + ' 个单词';
    document.getElementById('practiceInput').value = '';
    document.getElementById('practiceFeedback').style.display = 'none';
    
    showScreen('practiceScreen');
    
    // 自动播放读音
    setTimeout(function() { playPracticeWord(); }, 500);
}

function playPracticeWord() {
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    const word = group[learnSession.currentWordIndex];
    var localUrl = '/tinglidanciceshi/audio/words/' + encodeURIComponent(word) + '.mp3';
    var audio = new Audio(localUrl);
    audio.onerror = function() { showToast('本地音频缺失：' + word, 'error'); };
    audio.play().catch(function() {
        showToast('音频播放失败：' + word, 'error');
    });
}

function submitPractice() {
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    const word = group[learnSession.currentWordIndex];
    const userAnswer = document.getElementById('practiceInput').value.trim().toLowerCase();
    const isCorrect = userAnswer === word.toLowerCase();
    
    const feedback = document.getElementById('practiceFeedback');
    
    if (isCorrect) {
        learnSession.practiceAttempts[word]++;
        
        if (learnSession.practiceAttempts[word] >= 3) {
            // 完成3次，标记为暂时掌握
            feedback.style.display = 'block';
            feedback.style.background = '#d4edda';
            feedback.style.color = '#155724';
            feedback.textContent = ' 完成3次拼写！进入下一个单词';
            
            setTimeout(function() {
                nextPracticeWord();
            }, 1000);
        } else {
            // 继续下一次拼写，播放读音
            feedback.style.display = 'block';
            feedback.style.background = '#d1ecf1';
            feedback.style.color = '#0c5460';
            feedback.textContent = ' 正确！还有 ' + (3 - learnSession.practiceAttempts[word]) + ' 次拼写';
            document.getElementById('practiceInput').value = '';
            document.getElementById('practiceProgress').textContent = '(' + (learnSession.practiceAttempts[word] + 1) + '/3)';
            setTimeout(function() { playPracticeWord(); }, 1000);
        }
    } else {
        // 错误，归零重新计数
        learnSession.practiceAttempts[word] = 0;
        feedback.style.display = 'block';
        feedback.style.background = '#f8d7da';
        feedback.style.color = '#721c24';
        feedback.innerHTML = ' 错误！正确拼写：<strong>' + word + '</strong><br>重新从第1次开始';
        document.getElementById('practiceInput').value = '';
        document.getElementById('practiceProgress').textContent = '(1/3)';
        setTimeout(function() { playPracticeWord(); }, 1500);
    }
}

function nextPracticeWord() {
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    learnSession.currentWordIndex++;
    
    if (learnSession.currentWordIndex < group.length) {
        showPracticeScreen();
    } else {
        // 本组练习完成，进入听写测试
        startGroupTest();
    }
}

// 2.2 听写当前组
function startGroupTest() {
    learnSession.phase = (learnSession.phase === 'final_practice') ? 'final_practice' : 'group_test';
    const group = learnSession.currentGroups[learnSession.currentGroupIndex];
    learnSession.groupTestResults = [];
    learnSession.currentWordIndex = 0;
    
    // 打乱顺序
    learnSession.currentTestWords = shuffleArray(group.slice());
    
    document.getElementById('learnModeLabel').textContent = '第' + (learnSession.currentGroupIndex + 1) + '组听写';
    document.getElementById('learnModeLabel').style.background = '#fff3cd';
    showScreen('learnTestScreen');
    showGroupTestQuestion();
}

function showGroupTestQuestion() {
    const word = learnSession.currentTestWords[learnSession.currentWordIndex];
    document.getElementById('learnQuestionCounter').textContent = '第 ' + (learnSession.currentWordIndex + 1) + ' / ' + learnSession.currentTestWords.length + ' 题';
    document.getElementById('learnProgressFill').style.width = ((learnSession.currentWordIndex + 1) / learnSession.currentTestWords.length * 100) + '%';
    document.getElementById('learnAnswerInput').value = '';
    document.getElementById('learnTimerDisplay').textContent = '准备中...';
    document.getElementById('learnTimerDisplay').className = '';
    document.getElementById('learnStatusIcon').textContent = '';
    document.getElementById('learnStatusIcon').className = '';
    
    // 使用统一的 playLearnWord（它会启动计时器）
    playLearnWord();
}

function groupTestAutoSubmit() {
    const userAnswer = document.getElementById('learnAnswerInput').value.trim().toLowerCase();
    const word = learnSession.currentTestWords[learnSession.currentWordIndex];
    const isCorrect = userAnswer === word.toLowerCase() && userAnswer !== '';
    processGroupTestAnswer(isCorrect, userAnswer || '(未作答)');
}

function processGroupTestAnswer(isCorrect, userAnswer) {
    const word = learnSession.currentTestWords[learnSession.currentWordIndex];
    
    learnSession.groupTestResults.push({
        word: word,
        isCorrect: isCorrect,
        userAnswer: userAnswer
    });
    
    if (isCorrect) {
        // 保存正确
        saveWordMastery(word, true, false);
    }
    
    learnSession.currentWordIndex++;
    
    if (learnSession.currentWordIndex < learnSession.currentTestWords.length) {
        showGroupTestQuestion();
    } else {
        // 本组听写完成，检查是否有错词
        const wrongInTest = learnSession.groupTestResults.filter(r => !r.isCorrect).map(r => r.word);
        
        if (wrongInTest.length > 0) {
            // 有错词，更新当前组为错词，重新拼写练习
            learnSession.currentGroups[learnSession.currentGroupIndex] = wrongInTest;
            learnSession.practiceAttempts = {};
            // 重置错词的练习次数
            for (var k = 0; k < wrongInTest.length; k++) {
                learnSession.practiceAttempts[wrongInTest[k]] = 0;
            }
            showToast('本组有 ' + wrongInTest.length + ' 个词需要继续拼写', 'info');
            startGroupPractice();
        } else {
            // 本组全对
            learnSession.completedGroups++;
            learnSession.currentGroupIndex++;
            
            if (learnSession.currentGroupIndex < learnSession.currentGroups.length) {
                // 下一组
                startGroupPractice();
            } else {
                // 所有组完成
                if (learnSession.phase === 'final_practice') {
                    // 第四阶段：回到听写测试
                    learnSession.finalReviewRound++;
                    learnSession.finalReviewWords = shuffleArray(learnSession.wrongWords.slice());
                    learnSession.finalReviewResults = [];
                    learnSession.currentWordIndex = 0;
                    document.getElementById('learnModeLabel').textContent = '全部错词听写（第' + learnSession.finalReviewRound + '轮）';
                    document.getElementById('learnModeLabel').style.background = '#d4edda';
                    showScreen('learnTestScreen');
                    showFinalReviewQuestion();
                } else {
                    // 第二阶段：进入最终复习
                    startFinalReview();
                }
            }
        }
    }
}

// 第四阶段：对所有错词进行听写测试
function startFinalReview() {
    learnSession.phase = 'final_review';
    learnSession.finalReviewRound = 1;
    // 所有错词一起测
    learnSession.finalReviewWords = shuffleArray(learnSession.wrongWords.slice());
    learnSession.finalReviewResults = [];
    learnSession.currentWordIndex = 0;
    
    document.getElementById('learnModeLabel').textContent = '全部错词听写（第' + learnSession.finalReviewRound + '轮）';
    document.getElementById('learnModeLabel').style.background = '#d4edda';
    showScreen('learnTestScreen');
    showFinalReviewQuestion();
}

function showFinalReviewQuestion() {
    const word = learnSession.finalReviewWords[learnSession.currentWordIndex];
    document.getElementById('learnQuestionCounter').textContent = '第 ' + (learnSession.currentWordIndex + 1) + ' / ' + learnSession.finalReviewWords.length + ' 题';
    document.getElementById('learnProgressFill').style.width = ((learnSession.currentWordIndex + 1) / learnSession.finalReviewWords.length * 100) + '%';
    document.getElementById('learnAnswerInput').value = '';
    document.getElementById('learnTimerDisplay').textContent = '准备中...';
    document.getElementById('learnTimerDisplay').className = '';
    document.getElementById('learnStatusIcon').textContent = '';
    document.getElementById('learnStatusIcon').className = '';
    
    // 使用统一的 playLearnWord
    playLearnWord();
}

function finalReviewAutoSubmit() {
    if (learnTimerInterval) { clearInterval(learnTimerInterval); learnTimerInterval = null; }
    if (learnPlayTimeout) { clearTimeout(learnPlayTimeout); learnPlayTimeout = null; }
    learnIsPlaying = false;
    learnTimerStarted = false;
    try { learnAudioEl.pause(); } catch(e) {}
    try { speechSynthesis.cancel(); } catch(e) {}
    const userAnswer = document.getElementById('learnAnswerInput').value.trim().toLowerCase();
    const word = learnSession.finalReviewWords[learnSession.currentWordIndex];
    const isCorrect = userAnswer === word.toLowerCase() && userAnswer !== '';
    processFinalReviewAnswer(isCorrect, userAnswer || '(未作答)');
}

function processFinalReviewAnswer(isCorrect, userAnswer) {
    const word = learnSession.finalReviewWords[learnSession.currentWordIndex];
    
    learnSession.finalReviewResults.push({
        word: word,
        isCorrect: isCorrect,
        userAnswer: userAnswer
    });
    
    if (isCorrect) {
        learnSession.masteredInSession++;
        saveWordMastery(word, true, false);
    }
    
    learnSession.currentWordIndex++;
    
    if (learnSession.currentWordIndex < learnSession.finalReviewWords.length) {
        showFinalReviewQuestion();
    } else {
        // 本轮听写完成，检查错词
        const wrongInFinal = learnSession.finalReviewResults.filter(r => !r.isCorrect).map(r => r.word);
        
        if (wrongInFinal.length > 0) {
            // 有错词：分组拼写训练  听写  循环
            startFinalReviewPractice(wrongInFinal);
        } else {
            // 全部正确，学习完成
            showLearnResult();
        }
    }
}

// 第四阶段补充：对错词进行分组拼写训练
function startFinalReviewPractice(wrongWords) {
    learnSession.phase = 'final_practice';
    // 分成10词一组
    learnSession.currentGroups = [];
    for (let i = 0; i < wrongWords.length; i += 10) {
        learnSession.currentGroups.push(wrongWords.slice(i, i + 10));
    }
    learnSession.currentGroupIndex = 0;
    learnSession.practiceAttempts = {};
    
    startGroupPractice();
}

// 显示学习结果
function showLearnResult() {
    stopLearnTimer();
    
    const elapsed = practiceElapsedSeconds(learnSession.startTime);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    
    document.getElementById('learnResultTime').textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    document.getElementById('learnResultInitial').textContent = learnSession.initialCorrect;
    document.getElementById('learnResultWrong').textContent = learnSession.initialWrong;
    document.getElementById('learnResultMastered').textContent = learnSession.masteredInSession;
    document.getElementById('learnResultGroups').textContent = learnSession.completedGroups;
    
    showScreen('learnResultScreen');
    
    stopPracticeClock();
    saveLearnSession(elapsed);
}

// 保存学习会话记录
async function saveLearnSession(elapsedSeconds) {
    const elapsed = elapsedSeconds != null ? elapsedSeconds : practiceElapsedSeconds(learnSession.startTime);
    await saveStudySession({
        student_id: currentStudent.student_id,
        module_type: 'dictation',
        module_name: '听力1000词',
        session_kind: 'study',
        words_tested: learnSession.words.length,
        initial_correct: learnSession.initialCorrect,
        initial_wrong: learnSession.initialWrong,
        groups_completed: learnSession.completedGroups,
        duration_seconds: elapsed,
        started_at: learnSession.startTime ? new Date(learnSession.startTime).toISOString() : null,
        ended_at: new Date().toISOString()
    });
}

// 保存学习进度（退出时）
async function saveLearnProgress() {
    // 保存当前进度到本地存储或数据库
    // 实现按组保存的逻辑
}

// 学习功能相关函数绑定到全局
window.showLearnScreen = showLearnScreen;
window.exitLearn = exitLearn;
window.startLearnSession = startLearnSession;
window.learnSubmitAnswer = learnSubmitAnswer;
window.learnSkipWord = learnSkipWord;
window.playPracticeWord = playPracticeWord;
window.submitPractice = submitPractice;

// ══════════════════════════════════════════════════
// 写作词伙练习功能
// ══════════════════════════════════════════════════
var phraseState = {
    category: null,
    vocab: [],
    currentIndex: 0,
    selectedWords: [],
    correctCount: 0,
    totalAnswered: 0
};

// 初始化分类页面
function initPhraseCategoryPage() {
    const gridXiao = document.getElementById('phraseGridXiao');
    const gridDa = document.getElementById('phraseGridDa');
    
    gridXiao.innerHTML = '';
    gridDa.innerHTML = '';
    
    phraseCategories.forEach(function(cat) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-secondary';
        btn.style.cssText = 'padding:15px; text-align:left; font-size:0.9rem;';
        btn.innerHTML = '<span style="font-size:20px; margin-right:10px;">' + cat.icon + '</span>' + cat.name + ' <span style="color:#999; font-size:0.8rem;">(' + cat.vocab.length + '词)</span>';
        btn.onclick = function() { selectPhraseCategory(cat.id); };
        
        if (cat.group === '小作文') {
            gridXiao.appendChild(btn);
        } else {
            gridDa.appendChild(btn);
        }
    });
}

function selectPhraseCategory(catId) {
    let catName, catVocab;
    
    if (catId === '__foundation__') {
        catName = '⭐ 基础必背词伙';
        catVocab = foundationPhrases.slice();
    } else {
        const cat = phraseCategories.find(function(c) { return c.id === catId; });
        if (!cat) return;
        catName = cat.icon + ' ' + cat.name;
        catVocab = cat.vocab.slice();
    }
    
    phraseState.category = catId;
    phraseState.vocab = shuffleArray(catVocab);
    phraseState.currentIndex = 0;
    phraseState.selectedWords = [];
    phraseState.correctCount = 0;
    phraseState.totalAnswered = 0;
    
    document.getElementById('phraseCategoryBadge').textContent = catName;
    document.getElementById('phraseCategoryPage').style.display = 'none';
    document.getElementById('phrasePracticePage').style.display = 'block';
    document.getElementById('phraseFinishPage').style.display = 'none';
    
    loadPhraseQuestion();
}

function loadPhraseQuestion() {
    if (phraseState.currentIndex >= phraseState.vocab.length) {
        showPhraseFinish();
        return;
    }
    
    const q = phraseState.vocab[phraseState.currentIndex];
    phraseState.selectedWords = [];
    
    document.getElementById('phraseQuestionNum').textContent = String(phraseState.currentIndex + 1).padStart(2, '0') + ' / ' + phraseState.vocab.length;
    document.getElementById('phraseChinese').textContent = q.zh;
    document.getElementById('phraseProgress').textContent = phraseState.currentIndex + '/' + phraseState.vocab.length;
    document.getElementById('phraseCorrect').textContent = phraseState.correctCount;
    document.getElementById('phraseHint').textContent = '点击下方单词组成答案';
    document.getElementById('phraseHint').style.color = '#666';
    
    buildPhraseWordPool(q);
    updatePhraseAnswerSlots();
}

function buildPhraseWordPool(q) {
    const pool = document.getElementById('phraseWordPool');
    pool.innerHTML = '';
    
    // 正确答案的单词
    const correctWords = q.en.split(' ');
    const allWords = correctWords.slice();
    
    // 从其他词伙中获取干扰词
    const otherWords = [];
    phraseCategories.forEach(function(cat) {
        cat.vocab.forEach(function(v) {
            if (v.en !== q.en) {
                v.en.split(' ').forEach(function(w) {
                    if (otherWords.indexOf(w) === -1) {
                        otherWords.push(w);
                    }
                });
            }
        });
    });
    foundationPhrases.forEach(function(v) {
        if (v.en !== q.en) {
            v.en.split(' ').forEach(function(w) {
                if (otherWords.indexOf(w) === -1) {
                    otherWords.push(w);
                }
            });
        }
    });
    
    // 随机选择干扰词
    const shuffledOthers = shuffleArray(otherWords);
    const targetCount = Math.max(correctWords.length + 4, 8);
    for (let i = 0; allWords.length < targetCount && i < shuffledOthers.length; i++) {
        if (allWords.indexOf(shuffledOthers[i]) === -1) {
            allWords.push(shuffledOthers[i]);
        }
    }
    
    const shuffledAll = shuffleArray(allWords);
    
    shuffledAll.forEach(function(word) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-secondary';
        btn.style.cssText = 'padding:8px 16px; font-size:1rem; border-radius:8px;';
        btn.textContent = word;
        btn.dataset.word = word;
        btn.onclick = function() { togglePhraseWord(word, btn); };
        pool.appendChild(btn);
    });
}

function findPhraseSelectedIndexByBtn(btn) {
    for (let i = 0; i < phraseState.selectedWords.length; i++) {
        if (phraseState.selectedWords[i].btn === btn) return i;
    }
    return -1;
}

function togglePhraseWord(word, btn) {
    // 按按钮实例判断选中，允许答案中出现重复词（如 curb crime / deter crime）
    const idx = findPhraseSelectedIndexByBtn(btn);
    if (idx >= 0) {
        phraseState.selectedWords.splice(idx, 1);
        btn.classList.remove('btn-success');
        btn.classList.add('btn-secondary');
    } else {
        phraseState.selectedWords.push({ word: word, btn: btn });
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-success');
    }
    updatePhraseAnswerSlots();
}

function updatePhraseAnswerSlots() {
    const slotsEl = document.getElementById('phraseAnswerSlots');
    slotsEl.innerHTML = '';
    
    if (phraseState.selectedWords.length === 0) {
        slotsEl.innerHTML = '<span style="color:#999;">点击下方单词组成答案 </span>';
        return;
    }
    
    phraseState.selectedWords.forEach(function(entry) {
        const slot = document.createElement('span');
        slot.style.cssText = 'background:#667eea; color:white; padding:8px 16px; border-radius:8px; font-size:1rem;';
        slot.textContent = entry.word;
        slotsEl.appendChild(slot);
    });
}

function phraseClearSelection() {
    phraseState.selectedWords = [];
    document.querySelectorAll('#phraseWordPool button').forEach(function(btn) {
        btn.classList.remove('btn-success');
        btn.classList.add('btn-secondary');
    });
    updatePhraseAnswerSlots();
}

function phraseCheckAnswer() {
    if (phraseState.selectedWords.length === 0) return;
    
    const q = phraseState.vocab[phraseState.currentIndex];
    
    // 比较答案（忽略顺序）
    const userSorted = phraseState.selectedWords.map(function(e) { return e.word.toLowerCase(); }).sort().join(' ');
    const correctSorted = q.en.toLowerCase().split(' ').sort().join(' ');
    
    phraseState.totalAnswered++;
    
    if (userSorted === correctSorted) {
        phraseState.correctCount++;
        document.getElementById('phraseHint').textContent = ' 正确！';
        document.getElementById('phraseHint').style.color = '#28a745';
        
        setTimeout(function() {
            phraseState.currentIndex++;
            loadPhraseQuestion();
        }, 800);
    } else {
        document.getElementById('phraseHint').textContent = ' 正确答案：' + q.en;
        document.getElementById('phraseHint').style.color = '#dc3545';
        
        setTimeout(function() {
            phraseState.currentIndex++;
            loadPhraseQuestion();
        }, 1500);
    }
}

function showPhraseFinish() {
    document.getElementById('phrasePracticePage').style.display = 'none';
    document.getElementById('phraseFinishPage').style.display = 'block';
    
    const score = Math.round(phraseState.correctCount / phraseState.vocab.length * 100);
    document.getElementById('phraseFinalScore').textContent = score + '%';
    document.getElementById('phraseFinalCorrect').textContent = phraseState.correctCount;
    document.getElementById('phraseFinalWrong').textContent = phraseState.vocab.length - phraseState.correctCount;
}

function phraseRestart() {
    selectPhraseCategory(phraseState.category);
}

function phraseBackToCategory() {
    document.getElementById('phraseCategoryPage').style.display = 'block';
    document.getElementById('phrasePracticePage').style.display = 'none';
    document.getElementById('phraseFinishPage').style.display = 'none';
}

function openPhraseIframe() {
    showScreen('phraseScreen');
    document.getElementById('phraseIframe').src = 'https://raysu672-glitch.github.io/xiezuocihuo/';
}

// 打开任意配置了 url 的模块（通用 iframe）
function openGenericIframe(moduleId, moduleName, url, mode) {
    const finalMode = mode || 'study';
    const normalizedModuleId = normalizeModuleType(moduleId);
    const ctx = window._currentTaskContext || {};
    window._currentModule = {
        id: normalizedModuleId,
        name: moduleName,
        mode: finalMode,
        startedAt: Date.now(),
        reported: false,
        plan_item_id: ctx.plan_item_id,
        unit_id: ctx.unit_id
    };
    startPracticeClock();
    const paramObj = {
        student_id: currentStudent && currentStudent.student_id,
        student_name: currentStudent && currentStudent.name,
        module_type: normalizedModuleId,
        module_name: moduleName,
        mode: finalMode,
        v: '20260827d'
    };
    if (ctx.plan_item_id != null) paramObj.plan_item_id = ctx.plan_item_id;
    if (ctx.unit_id) paramObj.unit_id = ctx.unit_id;
    if (ctx.content_version) paramObj.content_version = ctx.content_version;
    const finalUrl = appendModuleParams(url, paramObj);
    showScreen('genericScreen');
    document.getElementById('genericScreenTitle').textContent = moduleName + (finalMode === 'test' ? '测试' : '学习');
    const genericIframe = document.getElementById('genericIframe');
    // P4 跟读测试需要麦克风；学习页允许自动播放音频
    genericIframe.setAttribute('allow', 'microphone; autoplay');
    try { genericIframe.setAttribute('allowfullscreen', ''); } catch (e) {}
    genericIframe.src = finalUrl;
    bindIframePracticeClock(genericIframe);
}

async function saveCurrentModuleFallback() {
    const current = window._currentModule;
    if (!current) return;
    if (current.pendingStudySave) {
        try { await current.pendingStudySave; } catch (e) {}
    }
    if (current.reported) return;
    const duration = practiceElapsedSeconds(current.startedAt);
    if (duration < 3) return;
    const result = await saveStudySession({
        module_type: current.id,
        module_name: current.name,
        session_kind: current.mode === 'test' ? 'test' : 'study',
        duration_seconds: duration,
        started_at: new Date(current.startedAt).toISOString(),
        ended_at: new Date().toISOString()
    });
    if (!result.error) current.reported = true;
}

function finishGenericIframeClose() {
    stopPracticeClock();
    window._currentModule = null;
    try { document.getElementById('genericIframe').src = ''; } catch(e) {}
    const returnId = window._wrongBookReturn;
    window._wrongBookReturn = null;
    if (returnId) {
        openWrongBook(returnId);
        return;
    }
    showStudentHome();
}

function exitGenericIframe() {
    try {
        var iframe = document.getElementById('genericIframe');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.postMessage({ type: 'requestSave' }, '*');
        }
    } catch(e) {}
    setTimeout(async function() {
        try { await saveCurrentModuleFallback(); } catch(e) { console.error('保存模块兜底时长失败:', e); }
        finishGenericIframeClose();
    }, 700);
}

function exitPhrase() {
    try {
        var iframe = document.getElementById('phraseIframe');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.postMessage({ type: 'requestSave' }, '*');
        }
    } catch(e) {}
    setTimeout(function() {
        document.getElementById('phraseIframe').src = '';
        showScreen('studentHome');
        try { loadProgressTable(); } catch(e) {}
    }, 700);
}

// 新版听力学习 iframe；taskOpts 可选：{ group, task_id, plan_item_id, unit_id, content_version }
function openListeningIframe(moduleId, taskOpts) {
    const dictation = getBuiltinDictation(moduleId || 'dictation');
    currentDictationModuleId = dictation.id;
    window._currentModule = {
        id: dictation.id,
        name: dictation.name,
        mode: 'study',
        startedAt: Date.now(),
        reported: false,
        plan_item_id: taskOpts && taskOpts.plan_item_id,
        unit_id: taskOpts && taskOpts.unit_id
    };
    startPracticeClock();
    showScreen('listeningScreen');
    const listeningTitle = document.querySelector('#listeningScreen h2');
    if (listeningTitle) listeningTitle.textContent = dictation.name + '学习';
    const params = {
        student_id: currentStudent && currentStudent.student_id,
        module_type: dictation.id,
        module_name: dictation.name,
        mode: 'study',
        v: '20260828spell'
    };
    if (taskOpts && typeof taskOpts === 'object') {
        if (taskOpts.group != null && taskOpts.group !== '') params.group = taskOpts.group;
        if (taskOpts.task_id != null) params.task_id = taskOpts.task_id;
        if (taskOpts.plan_item_id != null) params.plan_item_id = taskOpts.plan_item_id;
        if (taskOpts.unit_id) params.unit_id = taskOpts.unit_id;
        if (taskOpts.content_version) params.content_version = taskOpts.content_version;
    }
    document.getElementById('listeningIframe').src = appendModuleParams(dictation.studyPage, params);
    bindIframePracticeClock(document.getElementById('listeningIframe'));
}

function exitListening() {
    try {
        var iframe = document.getElementById('listeningIframe');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.postMessage({ type: 'requestSave' }, '*');
        }
    } catch(e) {}
    setTimeout(async function() {
        try { await saveCurrentModuleFallback(); } catch(e) { console.error('保存听力学习兜底时长失败:', e); }
        stopPracticeClock();
        window._currentModule = null;
        document.getElementById('listeningIframe').src = '';
        showStudentHome();
    }, 700);
}

// 导出函数到全局
window.exitPhrase = exitPhrase;
window.openPhraseIframe = openPhraseIframe;
window.showPhraseScreen = openPhraseIframe;
window.openListeningIframe = openListeningIframe;
window.exitListening = exitListening;

function isTrustedModuleMessage(event, current) {
    if (!current || !current.id || !currentStudent) return false;
    if (event.origin !== window.location.origin) return false;
    const iframeId = isBuiltinDictationModule(current.id) && current.mode === 'study'
        ? 'listeningIframe'
        : 'genericIframe';
    const iframe = document.getElementById(iframeId);
    return !!(iframe && iframe.contentWindow && event.source === iframe.contentWindow);
}

window.addEventListener('message', async function(event) {
    const data = event.data;
    if (!data || !data.type) return;
    if (data.type === 'taskScopeProgress') {
        if (event.origin && event.origin !== window.location.origin) return;
        const ctx = window._currentTaskContext || {};
        const planItemId = data.plan_item_id || ctx.plan_item_id;
        if (!planItemId) return;
        const body = { plan_item_id: planItemId };
        if (data.scope_done != null) body.scope_done = data.scope_done;
        else if (data.delta != null) body.delta = data.delta;
        else return;
        apiFetch('/api/task/me/scope-progress', {
            method: 'POST',
            body: JSON.stringify(body)
        }).then(function(result) {
            if (result.error) {
                console.warn('scope progress failed', result.error);
            }
        });
        return;
    }
    if (data.type === 'taskUnitComplete') {
        // Same-origin iframe task completion (may fire before _currentModule checks)
        if (event.origin && event.origin !== window.location.origin) return;
        await completeCurrentTaskStudy(data);
        return;
    }
    const current = window._currentModule;
    if (!isTrustedModuleMessage(event, current)) return;

    try {
        if (data.type === 'genericStudyComplete' || data.type === 'phraseStudyComplete' || data.type === 'listeningStudyComplete' || data.type === 'listeningStudyTime') {
            const moduleType = current.id;
            // 口语学习/测试都会练题，两种模式都记学习会话；其他模块仍仅学习模式上报
            if (current.mode !== 'study' && moduleType !== 'speaking') return;
            const module = getModuleById(moduleType);
            const totalWords = data.totalWords || data.totalCount || data.wordsTested || 0;
            const totalCorrect = data.totalCorrect || data.rightCount || data.masteredCount || data.correctCount || 0;
            const endedAt = data.endedAt || data.ended_at || new Date().toISOString();
            const elapsedSeconds = practiceElapsedSeconds(current.startedAt);
            const reportedSeconds = Math.max(0, Math.round(Number(data.durationSeconds || data.duration_seconds || 0)));
            // 口语按录音时长上报；允许略大于打开时长的时钟误差
            const durationSeconds = moduleType === 'speaking'
                ? reportedSeconds
                : Math.min(reportedSeconds, elapsedSeconds + 5);
            const startedAt = data.startedAt || data.started_at || new Date(new Date(endedAt).getTime() - Math.max(durationSeconds, 1) * 1000).toISOString();
            const savePromise = saveStudySession({
                student_id: currentStudent.student_id,
                module_type: moduleType,
                module_name: current.name || (module ? module.name : moduleType),
                session_kind: 'study',
                totalWords: totalWords,
                totalCorrect: totalCorrect,
                wrongCount: data.wrongCount != null ? data.wrongCount : Math.max(0, totalWords - totalCorrect),
                completedGroups: data.completedGroups || 0,
                durationSeconds: durationSeconds,
                started_at: startedAt,
                ended_at: endedAt,
                details: data.details || []
            });
            current.pendingStudySave = savePromise;
            const result = await savePromise;
            if (current.pendingStudySave === savePromise) current.pendingStudySave = null;
            // 口语已主动上报（含 0 增量退出），跳过墙钟兜底，避免把停留时长记成练习时长
            if (!result.error || moduleType === 'speaking') current.reported = true;
            if (result.error) {
                console.error('保存学习记录失败:', result.error);
                showToast('保存学习时长失败', 'error');
            } else if (!result.skipped) {
                showToast(moduleType === 'speaking' ? '口语练习进度已保存' : '学习时长已保存');
                try { loadProgressTable(); } catch(e) {}
            }
            return;
        }

        if (data.type === 'genericTestComplete' || data.type === 'moduleTestComplete') {
            if (data.completed !== true) return;
            const moduleType = current.id;
            // 口语在学习/测试里都可能 AI 评分，两种模式都写入测试记录
            if (current.mode !== 'test' && moduleType !== 'speaking') return;
            const module = getModuleById(moduleType);
            const reportedSeconds = Math.max(0, Math.round(Number(data.durationSeconds || data.duration_seconds || 0)));
            const elapsedSeconds = practiceElapsedSeconds(current.startedAt);
            const durationSeconds = moduleType === 'speaking'
                ? reportedSeconds
                : (reportedSeconds > 0 ? Math.min(reportedSeconds, elapsedSeconds + 5) : elapsedSeconds);
            const endedAt = data.endedAt || data.ended_at || new Date().toISOString();
            const startedAt = data.startedAt || data.started_at || new Date(new Date(endedAt).getTime() - durationSeconds * 1000).toISOString();
            const result = await saveModuleTestRecord({
                student_id: currentStudent.student_id,
                module_type: moduleType,
                module_name: current.name || (module ? module.name : moduleType),
                test_type: data.testType || data.test_type || 'module_test',
                score_percent: data.scorePercent != null ? data.scorePercent : data.score,
                correct_count: data.correctCount || data.correct_count || data.rightCount || 0,
                total_count: data.totalCount || data.total_count || 0,
                duration_seconds: durationSeconds,
                started_at: startedAt,
                ended_at: endedAt,
                details: data.details || []
            });
            if (!result.error) current.reported = true;
            if (result.error) {
                console.error('保存测试记录失败:', result.error);
                showToast('保存测试记录失败', 'error');
            } else {
                if (!result.skipped) showToast('测试记录已保存');
                if (module && hasWrongBook(module)) {
                    const applyItems = extractWrongItemResults(moduleType, data.details || []);
                    if (applyItems.length > 0) {
                        const applyResult = await apiFetch('/api/student/wrong-items/apply', {
                            method: 'POST',
                            body: JSON.stringify({ module_type: moduleType, results: applyItems })
                        });
                        if (applyResult.error) {
                            console.error('同步错题失败:', applyResult.error);
                            showToast('测试已保存，但错题同步失败', 'error');
                        }
                    }
                }
                try { loadProgressTable(); } catch(e) {}
            }
        }
    } catch (e) {
        console.error('处理模块上报失败:', e);
    }
});

setTimeout(initEntryRoute, 0);
