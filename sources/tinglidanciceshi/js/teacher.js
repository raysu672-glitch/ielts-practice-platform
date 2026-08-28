// 教师端：登录与后台管理
var currentTeacher = null;

async function teacherApiGet(url) {
    return apiFetch(url);
}

async function teacherApiPost(url, body) {
    return apiFetch(url, {
        method: 'POST',
        body: JSON.stringify(body || {})
    });
}

var WRITING_TEACHER_PASSWORD = 'xiezuo8805';

async function restoreTeacherSession() {
    try {
        const me = await authMe('teacher');
        if (!me.data || me.data.role !== 'teacher' || !me.data.teacher) {
            return;
        }
        currentTeacher = me.data.teacher;
        showScreen('teacherDashboard');
        updateTeacherMgmtVisibility();
        loadTeacherData();
    } catch (e) {
        console.error('恢复教师登录态失败:', e);
    }
}

// 教师登录验证（账号+密码，服务端签发 HttpOnly Cookie）
async function verifyTeacherPassword() {
    const teacherId = document.getElementById('teacherId').value.trim();
    const password = document.getElementById('teacherPassword').value;
    if (!teacherId || !password) {
        showToast('请输入账号和密码', 'error');
        return;
    }
    try {
        const result = await apiFetch('/api/auth/teacher/login', {
            method: 'POST',
            body: JSON.stringify({ teacher_id: teacherId, password: password })
        });
        if (result.error || !result.data || !result.data.teacher) {
            showToast((result.error && result.error.message) || '账号或密码错误', 'error');
            return;
        }
        currentTeacher = result.data.teacher;
        showScreen('teacherDashboard');
        updateTeacherMgmtVisibility();
        loadTeacherData();
    } catch (e) {
        console.error('教师登录失败:', e);
        showToast('登录失败：' + (e.message || '请稍后再试'), 'error');
    }
}

function verifyWritingTeacherPassword() {
    const password = (document.getElementById('writingTeacherPassword') || {}).value || '';
    if (password === WRITING_TEACHER_PASSWORD) {
        openWritingTeacherDashboard();
    } else {
        showToast('密码错误', 'error');
    }
}

function openWritingTeacherDashboard() {
    document.body.classList.add('teacher-writing-wide');
    showScreen('writingTeacherDashboard');
    var frame = document.getElementById('writingOnlyIframe');
    if (frame) {
        frame.src = '../xiezuopigai/ielts-writing-backend/teacher.html?v=13&entry=writing-teacher&_=' + Date.now();
    }
}

function writingTeacherLogout() {
    document.body.classList.remove('teacher-writing-wide');
    var frame = document.getElementById('writingOnlyIframe');
    if (frame) frame.src = '';
    var pwd = document.getElementById('writingTeacherPassword');
    if (pwd) pwd.value = '';
    showScreen('writingTeacherLoginScreen');
}

function teacherLogout() {
    document.body.classList.remove('teacher-writing-wide');
    currentTeacher = null;
    updateTeacherMgmtVisibility();
    authLogout('teacher').finally(function() {
        showScreen('teacherLoginScreen');
        var teacherIdInput = document.getElementById('teacherId');
        if (teacherIdInput) teacherIdInput.value = '';
        document.getElementById('teacherPassword').value = '';
    });
}

function isAdminTeacher() {
    return !!(currentTeacher && (currentTeacher.teacher_id === 'admin' || currentTeacher.is_admin));
}

function updateTeacherMgmtVisibility() {
    var tab = document.getElementById('tabTeachersBtn');
    if (tab) tab.style.display = isAdminTeacher() ? '' : 'none';
    var panel = document.getElementById('tabTeachers');
    if (panel && !isAdminTeacher()) panel.style.display = 'none';
}

async function loadTeacherData() {
    try {
        var tasks = [loadStudents(), loadRecords(), loadStandards()];
        if (isAdminTeacher()) tasks.push(loadTeachers());
        await Promise.all(tasks);
    } catch (e) {
        console.error('加载教师数据失败:', e);
    }
    // 同时把学生列表加载到搜索缓存（供学习进度页面搜索）
    try {
        const studentsResult = await teacherApiGet('/api/teacher/students');
        _teacherStudents = studentsResult.data || [];
    } catch (e) {
        console.error('加载学生列表失败:', e);
        _teacherStudents = [];
    }
}

function studentNameLinkHtml(studentId, studentName) {
    const name = studentName || studentId || '-';
    if (!studentId) return escapeHtml(name);
    return '<a class="student-name-link" href="javascript:void(0)" onclick="event.stopPropagation();openStudentLearningProgress(\'' +
        escapeJsString(studentId) + '\', \'' + escapeJsString(name) + '\')">' + escapeHtml(name) + '</a>';
}

function openStudentLearningProgress(studentId, studentName) {
    if (!studentId) return;
    switchTeacherTab('progress', null, { skipLoad: true });
    const container = document.getElementById('teacherStudentProgress');
    if (container) container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">加载中...</p>';
    showStudentDetailProgress(studentId, studentName || studentId);
}

async function loadStudents() {
    const result = await teacherApiGet('/api/teacher/students');
    const container = document.getElementById('studentsList');
    const students = result.data;
    if (!students || students.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:20px;">暂无学生</p>';
        return;
    }
    let html = '<table><thead><tr><th>学号</th><th>姓名</th><th>目标</th><th>状态</th><th>操作</th></tr></thead><tbody>';
    for (let i = 0; i < students.length; i++) {
        const s = students[i];
        const statusBadge = s.status === 'active' ? 'badge-success">正常' : 'badge-danger">禁用';
        const toggleBtn = s.status === 'active' ? 'btn-danger">禁用' : 'btn-success">启用';
        html += '<tr><td>' + escapeHtml(s.student_id) + '</td><td>' + studentNameLinkHtml(s.student_id, s.name) + '</td><td>' + s.target_score + '分</td><td><span class="badge ' + statusBadge + '</span></td><td><div class="student-actions"><button class="btn btn-sm btn-secondary" onclick="resetPassword(\'' + escapeJsString(s.student_id) + '\')">重置密码</button><button class="btn btn-sm ' + toggleBtn + '</button></div></td></tr>';
    }
    html += '</tbody></table>';
    container.innerHTML = html;

}

// getCheckedValues 保留兼容（已无 checkbox 但 loadRecords 用到）
function getCheckedValues(className) {
    return Array.prototype.map.call(
        document.querySelectorAll('.' + className + ':checked'),
        function(el) { return el.value; }
    );
}

var _recordColumnFilters = {
    studentId: '',
    studentIds: [],
    module: '',
    testType: '',
    dateRange: '',
    durationRange: '',
    scoreRange: '',
    passed: ''
};
var _cachedRecordRows = [];

function buildSelectOptions(options, selectedValue) {
    return options.map(function(opt) {
        const selected = String(selectedValue || '') === String(opt.value) ? ' selected' : '';
        return '<option value="' + escapeHtml(opt.value) + '"' + selected + '>' + escapeHtml(opt.label) + '</option>';
    }).join('');
}

function toggleFilterMenu(id, event) {
    if (event) event.stopPropagation();
    const target = document.getElementById(id);
    if (!target) return;
    const shouldOpen = !target.classList.contains('open');
    document.querySelectorAll('.multi-filter.open').forEach(function(el) {
        if (el.id !== id) el.classList.remove('open');
    });
    document.querySelectorAll('.filter-cell-open').forEach(function(el) {
        el.classList.remove('filter-cell-open');
    });
    target.classList.toggle('open', shouldOpen);
    const cell = target.closest('th');
    if (shouldOpen && cell) cell.classList.add('filter-cell-open');
}

function reopenFilterMenu(id) {
    setTimeout(function() {
        const target = document.getElementById(id);
        if (target) {
            target.classList.add('open');
            const cell = target.closest('th');
            if (cell) cell.classList.add('filter-cell-open');
        }
    }, 0);
}

function buildStudentMultiFilter(id, options, selectedIds, toggleFn, clearFn) {
    const selectedSet = new Set(selectedIds || []);
    const label = selectedSet.size > 0 ? selectedSet.size + '人' : '全部学生';
    let html = '<div class="multi-filter" id="' + id + '">';
    html += '<button type="button" class="multi-filter-toggle" onclick="toggleFilterMenu(\'' + id + '\',event)"><span>' + label + '</span><span>展开</span></button>';
    html += '<div class="multi-filter-menu" onclick="event.stopPropagation()">';
    if (!options || options.length === 0) {
        html += '<div class="multi-filter-empty">暂无学生</div>';
    } else {
        for (let i = 0; i < options.length; i++) {
            const item = options[i];
            const checked = selectedSet.has(item.id) ? ' checked' : '';
            html += '<label class="multi-filter-option">';
            html += '<input type="checkbox"' + checked + ' onchange="' + toggleFn + '(\'' + escapeJsString(item.id) + '\')">';
            html += '<span>' + escapeHtml(item.name) + '</span><small>' + escapeHtml(item.id) + '</small>';
            html += '</label>';
        }
        html += '<button type="button" class="multi-filter-clear" onclick="' + clearFn + '()">清除选择</button>';
    }
    html += '</div></div>';
    return html;
}

function getStudentOptionsFromRecords(records) {
    const map = new Map();
    (records || []).forEach(function(record) {
        const id = record.student_id || '';
        if (!id || map.has(id)) return;
        map.set(id, { id: id, name: getRecordStudentName(record) });
    });
    return Array.from(map.values()).sort(function(a, b) {
        return a.name.localeCompare(b.name, 'zh-CN') || a.id.localeCompare(b.id);
    });
}

function numericRangeMatches(value, range) {
    if (!range) return true;
    const n = Number(value) || 0;
    if (range.endsWith('+')) return n >= Number(range.slice(0, -1));
    const parts = range.split('-').map(Number);
    if (parts.length !== 2 || parts.some(function(v) { return Number.isNaN(v); })) return true;
    return n >= parts[0] && n <= parts[1];
}

function dateRangeMatches(value, range) {
    if (!range) return true;
    const d = value ? new Date(value) : null;
    if (!d || Number.isNaN(d.getTime())) return false;
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const tomorrow = new Date(today.getTime() + 86400000);
    if (range === 'today') return d >= today && d < tomorrow;
    if (range === 'yesterday') {
        const yesterday = new Date(today.getTime() - 86400000);
        return d >= yesterday && d < today;
    }
    if (range === '7d') return d >= new Date(today.getTime() - 6 * 86400000) && d < tomorrow;
    if (range === '30d') return d >= new Date(today.getTime() - 29 * 86400000) && d < tomorrow;
    if (range === 'month') return d >= new Date(today.getFullYear(), today.getMonth(), 1) && d < tomorrow;
    return true;
}

function getRecordStudentName(record) {
    return record.students && record.students.name ? record.students.name : '-';
}

function getRecordModuleName(record) {
    const module = getModuleById(record.module_type || 'dictation');
    return record.module_name || (module ? module.name : '听力1000词');
}

function getRecordTypeText(record) {
    if (record.test_type === 'random') return '随机';
    if (record.test_type === 'wrong_words') return '错题';
    return '模块测试';
}

function getRecordDateText(record) {
    return record.created_at ? new Date(record.created_at).toLocaleString('zh-CN') : '-';
}

function getRecordPassText(record) {
    return record.is_passed ? '达标' : '未达标';
}

function setRecordColumnFilter(key, value) {
    _recordColumnFilters[key] = value || '';
    renderRecordsTable(_cachedRecordRows);
}

function toggleRecordStudentFilter(studentId) {
    const selected = new Set(_recordColumnFilters.studentIds || []);
    if (selected.has(studentId)) selected.delete(studentId);
    else selected.add(studentId);
    _recordColumnFilters.studentIds = Array.from(selected);
    renderRecordsTable(_cachedRecordRows);
    reopenFilterMenu('recordStudentFilter');
}

function clearRecordStudentFilter() {
    _recordColumnFilters.studentIds = [];
    renderRecordsTable(_cachedRecordRows);
    reopenFilterMenu('recordStudentFilter');
}

function recordTextIncludes(value, keyword) {
    return String(value || '').toLowerCase().indexOf(String(keyword || '').toLowerCase()) !== -1;
}

function recordMatchesFilters(record) {
    const f = _recordColumnFilters;
    const moduleId = normalizeModuleType(record.module_type || 'dictation');
    if (f.studentId && !recordTextIncludes(record.student_id, f.studentId)) return false;
    if (f.studentIds && f.studentIds.length > 0 && f.studentIds.indexOf(record.student_id) < 0) return false;
    if (f.module && moduleId !== f.module) return false;
    if (f.testType && getRecordTypeText(record) !== f.testType) return false;
    if (!dateRangeMatches(record.created_at, f.dateRange)) return false;
    if (!numericRangeMatches(record.duration_seconds, f.durationRange)) return false;
    if (!numericRangeMatches(record.score, f.scoreRange)) return false;
    if (f.passed && getRecordPassText(record) !== f.passed) return false;
    return true;
}

function renderRecordsTable(records) {
    const container = document.getElementById('recordsList');
    const filteredRecords = (records || []).filter(recordMatchesFilters);

    let moduleOptions = '<option value="">全部</option>';
    MODULES.filter(isModuleAvailable).forEach(function(m) {
        const selected = _recordColumnFilters.module === m.id ? ' selected' : '';
        moduleOptions += '<option value="' + escapeHtml(m.id) + '"' + selected + '>' + escapeHtml(m.name) + '</option>';
    });
    const studentOptions = getStudentOptionsFromRecords(records || []);
    const timeOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: 'today', label: '今天' },
        { value: 'yesterday', label: '昨天' },
        { value: '7d', label: '近7天' },
        { value: '30d', label: '近30天' },
        { value: 'month', label: '本月' }
    ], _recordColumnFilters.dateRange);
    const durationOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-59', label: '1分钟内' },
        { value: '60-179', label: '1-3分钟' },
        { value: '180-299', label: '3-5分钟' },
        { value: '300-599', label: '5-10分钟' },
        { value: '600+', label: '10分钟以上' }
    ], _recordColumnFilters.durationRange);
    const scoreOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-59', label: '0-59%' },
        { value: '60-69', label: '60-69%' },
        { value: '70-79', label: '70-79%' },
        { value: '80-89', label: '80-89%' },
        { value: '90-100', label: '90-100%' }
    ], _recordColumnFilters.scoreRange);

    let html = '<div class="records-table-wrap"><table class="records-table"><thead>';
    html += '<tr class="records-filter-row">';
    html += '<th><input class="records-filter-control" value="' + escapeHtml(_recordColumnFilters.studentId) + '" oninput="setRecordColumnFilter(\'studentId\',this.value)"></th>';
    html += '<th>' + buildStudentMultiFilter('recordStudentFilter', studentOptions, _recordColumnFilters.studentIds, 'toggleRecordStudentFilter', 'clearRecordStudentFilter') + '</th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'module\',this.value)">' + moduleOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'testType\',this.value)"><option value="">全部</option><option value="随机"' + (_recordColumnFilters.testType === '随机' ? ' selected' : '') + '>随机</option><option value="错题"' + (_recordColumnFilters.testType === '错题' ? ' selected' : '') + '>错题</option><option value="模块测试"' + (_recordColumnFilters.testType === '模块测试' ? ' selected' : '') + '>模块测试</option></select></th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'dateRange\',this.value)">' + timeOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'durationRange\',this.value)">' + durationOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'scoreRange\',this.value)">' + scoreOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setRecordColumnFilter(\'passed\',this.value)"><option value="">全部</option><option value="达标"' + (_recordColumnFilters.passed === '达标' ? ' selected' : '') + '>达标</option><option value="未达标"' + (_recordColumnFilters.passed === '未达标' ? ' selected' : '') + '>未达标</option></select></th>';
    html += '</tr>';
    html += '<tr class="records-header-row"><th>学号</th><th>姓名</th><th>模块</th><th>类型</th><th>时间</th><th>用时</th><th>正确率</th><th>达标</th></tr></thead><tbody>';
    for (let i = 0; i < filteredRecords.length; i++) {
        const r = filteredRecords[i];
        const moduleName = getRecordModuleName(r);
        const typeText = getRecordTypeText(r);
        const dateStr = getRecordDateText(r);
        const badgeClass = r.is_passed ? 'badge-success' : 'badge-danger';
        const name = getRecordStudentName(r);
        html += '<tr><td>' + escapeHtml(r.student_id) + '</td><td>' + studentNameLinkHtml(r.student_id, name) + '</td><td>' + escapeHtml(moduleName) + '</td><td>' + escapeHtml(typeText) + '</td><td>' + escapeHtml(dateStr) + '</td><td class="records-duration">' + escapeHtml(formatDuration(r.duration_seconds)) + '</td><td class="records-score">' + escapeHtml(r.score) + '%</td><td><span class="badge ' + badgeClass + '">' + getRecordPassText(r) + '</span></td></tr>';
    }
    if (filteredRecords.length === 0) {
        html += '<tr><td colspan="8" style="text-align:center;color:#666;padding:20px;">暂无测试记录</td></tr>';
    }
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

async function loadRecords() {
    const container = document.getElementById('recordsList');
    const result = await teacherApiGet('/api/teacher/test-records?limit=1000');
    if (result.error) console.error('加载测试记录失败:', result.error);
    _cachedRecordRows = result.data || [];
    renderRecordsTable(_cachedRecordRows);
}

var _teacherStudents = [];
var _progressColumnFilters = {
    studentId: '',
    studentIds: [],
    module: '',
    targetUnit: '',
    bestScoreRange: '',
    testCountRange: '',
    passCountRange: '',
    passRateRange: '',
    totalDurationRange: '',
    todayDurationRange: '',
    status: ''
};
var _cachedProgressRows = [];
var _teacherOverviewCache = null;
var _activeStudentState = {
    preset: 'today',
    day: '',
    start: '',
    end: '',
    sortDir: 'desc'
};
var _activeCalendarOpen = false;
var _activeCalendarPick = { viewYm: '', start: '', end: '' };

function padCal(n) {
    return n < 10 ? '0' + n : String(n);
}

function shiftCalendarYm(ym, delta) {
    var parts = String(ym || '').split('-');
    var y = Number(parts[0]);
    var m = Number(parts[1]) + Number(delta || 0);
    if (!y || !m && m !== 0) return ym;
    while (m < 1) { m += 12; y -= 1; }
    while (m > 12) { m -= 12; y += 1; }
    return y + '-' + padCal(m);
}

function formatChinaDateTime(iso) {
    if (!iso) return '-';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '-';
    return d.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false });
}

function activeRangeLabel(range) {
    if (!range || !range.startYmd) return '';
    if (range.startYmd === range.endYmd) return range.startYmd;
    return range.startYmd + ' ～ ' + range.endYmd;
}

function setActiveStudentRange(preset) {
    _activeStudentState.preset = preset || 'today';
    _activeStudentState.day = '';
    _activeStudentState.start = '';
    _activeStudentState.end = '';
    _activeCalendarOpen = false;
    renderActiveStudents();
}

function formatPickedDayLabel(ymd) {
    var parts = String(ymd || '').split('-');
    if (parts.length !== 3) return '';
    var y = Number(parts[0]);
    var m = Number(parts[1]);
    var d = Number(parts[2]);
    if (!y || !m || !d) return '';
    var thisYear = Number(String((window.TrackingUtils && window.TrackingUtils.getChinaYmd()) || '').slice(0, 4));
    if (thisYear && y === thisYear) return m + '月' + d + '日';
    return y + '年' + m + '月' + d + '日';
}

function formatCalendarButtonLabel(preset, range) {
    if (preset === 'week') return '本周';
    if (preset === 'month') return '本月';
    if (!range || !range.startYmd) return '日历';
    if (preset === 'range' || preset === 'day') {
        if (range.startYmd === range.endYmd) return formatPickedDayLabel(range.startYmd) || '日历';
        return (formatPickedDayLabel(range.startYmd) || range.startYmd) + ' ～ ' + (formatPickedDayLabel(range.endYmd) || range.endYmd);
    }
    return '日历';
}

function toggleActiveCalendar(ev) {
    if (ev) {
        ev.preventDefault();
        ev.stopPropagation();
    }
    _activeCalendarOpen = !_activeCalendarOpen;
    if (_activeCalendarOpen) {
        var today = window.TrackingUtils.getChinaYmd();
        var range = window.TrackingUtils.resolveActiveRange(
            _activeStudentState.preset,
            _activeStudentState.day,
            today,
            _activeStudentState.start,
            _activeStudentState.end
        );
        var anchor = range.endYmd && range.endYmd <= today ? range.endYmd : today;
        _activeCalendarPick.viewYm = String(anchor).slice(0, 7);
        _activeCalendarPick.start = range.startYmd || '';
        _activeCalendarPick.end = range.endYmd || '';
    }
    renderActiveStudents();
}

function shiftActiveCalendarMonth(delta) {
    var todayYm = window.TrackingUtils.getChinaYmd().slice(0, 7);
    var next = shiftCalendarYm(_activeCalendarPick.viewYm || todayYm, delta);
    if (next > todayYm) return;
    _activeCalendarPick.viewYm = next;
    _activeCalendarOpen = true;
    renderActiveStudents();
}

function pickActiveCalendarDay(ymd) {
    var today = window.TrackingUtils.getChinaYmd();
    if (!ymd || ymd > today) return;
    if (!_activeCalendarPick.start || _activeCalendarPick.end) {
        _activeCalendarPick.start = ymd;
        _activeCalendarPick.end = '';
        _activeCalendarOpen = true;
        renderActiveStudents();
        return;
    }
    var start = _activeCalendarPick.start;
    var end = ymd;
    if (start > end) {
        var swap = start;
        start = end;
        end = swap;
    }
    applyPickedActiveRange(start, end);
}

function applyPickedActiveRange(start, end) {
    if (!start && !end) {
        showToast('请先在日历上点开始和结束日期', 'error');
        return;
    }
    if (!start) start = end;
    if (!end) end = start;
    if (start > end) {
        var swap = start;
        start = end;
        end = swap;
    }
    _activeStudentState.preset = start === end ? 'day' : 'range';
    _activeStudentState.day = start === end ? start : '';
    _activeStudentState.start = start;
    _activeStudentState.end = end;
    _activeCalendarPick.start = start;
    _activeCalendarPick.end = end;
    _activeCalendarOpen = false;
    renderActiveStudents();
}

function applyActiveCalendarRange() {
    applyPickedActiveRange(_activeCalendarPick.start, _activeCalendarPick.end || _activeCalendarPick.start);
}

function buildActiveCalendarGridHtml(viewYm, start, end, today) {
    var parts = String(viewYm || today).split('-');
    var y = Number(parts[0]);
    var m = Number(parts[1]);
    if (!y || !m) return '';
    var todayYm = String(today).slice(0, 7);
    var firstWeekday = new Date(Date.UTC(y, m - 1, 1)).getUTCDay();
    var mondayPad = (firstWeekday + 6) % 7;
    var lastDate = new Date(Date.UTC(y, m, 0)).getUTCDate();
    var pending = start && !end;
    var html = '<div class="active-cal-nav">';
    html += '<button type="button" class="active-cal-nav-btn" onclick="shiftActiveCalendarMonth(-1)">‹</button>';
    html += '<strong>' + y + '年' + m + '月</strong>';
    html += '<button type="button" class="active-cal-nav-btn"' + (viewYm >= todayYm ? ' disabled' : '') + ' onclick="shiftActiveCalendarMonth(1)">›</button>';
    html += '</div>';
    html += '<div class="active-cal-weekdays"><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span><span>日</span></div>';
    html += '<div class="active-cal-grid">';
    var i;
    for (i = 0; i < mondayPad; i++) html += '<span class="active-cal-day is-empty"></span>';
    for (var d = 1; d <= lastDate; d++) {
        var ymd = y + '-' + padCal(m) + '-' + padCal(d);
        var cls = 'active-cal-day';
        var future = ymd > today;
        if (future) cls += ' is-future';
        if (ymd === today) cls += ' is-today';
        if (start && ymd === start) cls += ' is-bound';
        if (end && ymd === end) cls += ' is-bound';
        if (start && end && ymd > start && ymd < end) cls += ' is-in';
        if (pending && ymd === start) cls += ' is-pending';
        html += '<button type="button" class="' + cls + '"' + (future ? ' disabled' : '') + ' onclick="pickActiveCalendarDay(\'' + ymd + '\')">' + d + '</button>';
    }
    html += '</div>';
    html += '<div class="active-cal-hint">' + (pending ? '再点一个日期作为结束' : '先点开始日期，再点结束日期') + '</div>';
    return html;
}

function applyActiveCalendarPreset(preset) {
    var today = window.TrackingUtils.getChinaYmd();
    var range = window.TrackingUtils.resolveActiveRange(preset, '', today);
    _activeStudentState.preset = preset;
    _activeStudentState.day = '';
    _activeStudentState.start = range.startYmd;
    _activeStudentState.end = range.endYmd;
    _activeCalendarOpen = false;
    renderActiveStudents();
}

function toggleActiveStudentSort() {
    _activeStudentState.sortDir = _activeStudentState.sortDir === 'desc' ? 'asc' : 'desc';
    renderActiveStudents();
}

async function loadActiveStudents() {
    const container = document.getElementById('activeStudentsList');
    if (!container) return;
    container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">加载中...</p>';
    try {
        const overviewResult = await teacherApiGet('/api/teacher/overview');
        if (overviewResult.error) throw new Error((overviewResult.error && overviewResult.error.message) || '加载失败');
        _teacherOverviewCache = {
            students: (overviewResult.data && overviewResult.data.students) || [],
            test_records: (overviewResult.data && overviewResult.data.test_records) || [],
            study_sessions: (overviewResult.data && overviewResult.data.study_sessions) || []
        };
        _teacherStudents = _teacherOverviewCache.students;
        renderActiveStudents();
    } catch (e) {
        console.error('加载活跃学生失败:', e);
        container.innerHTML = '<p style="text-align:center;color:#c0392b;padding:40px;">加载失败，请稍后重试</p>';
        showToast('加载活跃学生失败', 'error');
    }
}

function renderActiveStudents() {
    const container = document.getElementById('activeStudentsList');
    if (!container) return;
    const cache = _teacherOverviewCache || { students: [], test_records: [], study_sessions: [] };
    const utils = window.TrackingUtils;
    const today = utils.getChinaYmd();
    const range = utils.resolveActiveRange(
        _activeStudentState.preset,
        _activeStudentState.day,
        today,
        _activeStudentState.start,
        _activeStudentState.end
    );
    const rows = utils.buildActiveStudentRows(cache.students, cache.study_sessions, cache.test_records, {
        startYmd: range.startYmd,
        endYmd: range.endYmd,
        sortDir: _activeStudentState.sortDir
    });
    const totalSeconds = rows.reduce(function(sum, row) { return sum + row.seconds; }, 0);
    const practicedCount = rows.filter(function(row) { return row.seconds > 0; }).length;
    const preset = _activeStudentState.preset;

    function chip(id, label) {
        const on = preset === id ? ' is-on' : '';
        return '<button type="button" class="active-range-btn' + on + '" onclick="setActiveStudentRange(\'' + id + '\')">' + label + '</button>';
    }

    let html = '<div class="active-range-bar">';
    html += chip('today', '今天');
    html += chip('yesterday', '昨天');
    var calOn = (preset === 'week' || preset === 'month' || preset === 'range' || preset === 'day') ? ' is-on' : '';
    var calOpen = _activeCalendarOpen ? ' is-open' : '';
    html += '<span class="active-calendar-wrap' + calOpen + '" id="activeCalendarWrap">';
    html += '<button type="button" class="active-range-btn active-calendar-btn' + calOn + '" onclick="toggleActiveCalendar(event)">';
    html += '<svg class="active-calendar-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M8 3v4M16 3v4M3 10h18"></path></svg>';
    html += escapeHtml(formatCalendarButtonLabel(preset, range)) + '</button>';
    html += '<div class="active-calendar-panel" onclick="event.stopPropagation()">';
    html += '<div class="active-calendar-presets">';
    html += '<button type="button" class="active-range-btn' + (preset === 'week' ? ' is-on' : '') + '" onclick="applyActiveCalendarPreset(\'week\')">本周</button>';
    html += '<button type="button" class="active-range-btn' + (preset === 'month' ? ' is-on' : '') + '" onclick="applyActiveCalendarPreset(\'month\')">本月</button>';
    html += '</div>';
    html += buildActiveCalendarGridHtml(
        _activeCalendarPick.viewYm || String(range.endYmd || today).slice(0, 7),
        _activeCalendarPick.start || range.startYmd,
        _activeCalendarPick.end,
        today
    );
    html += '<button type="button" class="btn btn-sm active-calendar-apply" onclick="applyActiveCalendarRange()">查看这段时间</button>';
    html += '</div></span>';
    html += '<button type="button" class="btn btn-sm btn-secondary" onclick="loadActiveStudents()">刷新</button>';
    html += '</div>';
    html += '<div class="active-range-summary">所选时段 <strong>' + escapeHtml(activeRangeLabel(range)) + '</strong>：共 <strong>' + rows.length + '</strong> 名学生，其中 <strong>' + practicedCount + '</strong> 人有练习，合计 <strong>' + escapeHtml(formatDuration(totalSeconds)) + '</strong></div>';

    if (rows.length === 0) {
        html += '<p style="text-align:center;color:#666;padding:28px;background:#f8f9fa;border-radius:10px;">暂无学生</p>';
        container.innerHTML = html;
        return;
    }

    const sortMark = _activeStudentState.sortDir === 'desc' ? '▼' : '▲';
    html += '<div class="records-table-wrap"><table class="records-table"><thead>';
    html += '<tr class="records-header-row">';
    html += '<th>学号</th><th>姓名</th>';
    html += '<th class="active-sort-th" onclick="toggleActiveStudentSort()">练习时长 ' + sortMark + '</th>';
    html += '<th>练习次数</th><th>最后练习</th>';
    html += '</tr></thead><tbody>';
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        html += '<tr' + (row.seconds > 0 ? '' : ' class="active-zero-row"') + '>';
        html += '<td>' + escapeHtml(row.student_id) + '</td>';
        html += '<td>' + studentNameLinkHtml(row.student_id, row.student_name) + '</td>';
        html += '<td class="numeric-cell">' + escapeHtml(row.seconds > 0 ? formatDuration(row.seconds) : '0秒') + '</td>';
        html += '<td class="numeric-cell">' + row.count + '</td>';
        html += '<td>' + escapeHtml(formatChinaDateTime(row.latest)) + '</td>';
        html += '</tr>';
    }
    html += '</tbody></table></div>';
    html += '<p style="margin-top:10px;color:#888;font-size:0.85rem;">点击「练习时长」可切换从长到短 / 从短到长。时长口径与学习进度一致（含学习与测试）。</p>';
    container.innerHTML = html;
}

async function loadTeacherProgressData() {
    const container = document.getElementById('teacherStudentProgress');
    try {
        const overviewResult = await teacherApiGet('/api/teacher/overview');
        if (overviewResult.error) throw new Error((overviewResult.error && overviewResult.error.message) || '加载失败');
        _teacherStudents = (overviewResult.data && overviewResult.data.students) || [];
        _cachedProgressRows = buildProgressRows(
            _teacherStudents,
            (overviewResult.data && overviewResult.data.test_records) || [],
            (overviewResult.data && overviewResult.data.study_sessions) || []
        );
        renderTeacherProgressSummary();
    } catch (e) {
        console.error('加载进度数据失败:', e);
        showToast('加载进度数据失败', 'error');
    }
}

function buildProgressRows(students, allRecords, allStudySessions) {
    const rows = [];
    const modules = MODULES.filter(isModuleAvailable);
    const todayKey = getChinaDateKey();
    for (let i = 0; i < students.length; i++) {
        const s = students[i];
        const studentRecordsAll = (allRecords || []).filter(function(r) { return r.student_id === s.student_id; });
        const studentSessionsRaw = (allStudySessions || []).filter(function(r) { return r.student_id === s.student_id; });
        const studentSessionsAll = getStudySessions(studentSessionsRaw);
        for (let j = 0; j < modules.length; j++) {
            const module = modules[j];
            const studentRecords = getModuleRecords(studentRecordsAll, module.id);
            const studentSessions = getModuleStudySessions(studentSessionsAll, module.id);
            const target = getModuleTargetForScore(module, getStudentTargetScoreValue(s));
            const bestScore = getBestScore(studentRecords);
            const passCount = getPassCount(studentRecords);
            const passRate = studentRecords.length > 0 ? Math.round(passCount / studentRecords.length * 100) : 0;
            const totalSeconds = window.TrackingUtils.sumPracticeSeconds(studentSessionsRaw, studentRecordsAll, { moduleId: module.id });
            const todaySeconds = window.TrackingUtils.sumPracticeSeconds(studentSessionsRaw, studentRecordsAll, {
                moduleId: module.id,
                createdAt: function(iso) { return getChinaDateKey(iso) === todayKey; }
            });
            const practicedCount = module.id === 'speaking' ? getSpeakingPracticedCount(studentSessions) : 0;
            const speakingTotalQ = module.id === 'speaking' ? getSpeakingTotalQuestions(studentSessions) : 0;
            const studyOnly = isStudyOnlyModule(module);
            let status = 'not_started';
            let statusText = '未开始';
            let statusClass = 'badge-info';
            if (!studyOnly && bestScore >= target && bestScore > 0) {
                status = 'passed';
                statusText = '已达标';
                statusClass = 'badge-success';
            } else if ((!studyOnly && studentRecords.length > 0) || totalSeconds > 0 || practicedCount > 0) {
                status = 'in_progress';
                statusText = '进行中';
                statusClass = 'badge-warning';
            }
            rows.push({
                student_id: s.student_id,
                student_name: s.name,
                module_id: module.id,
                module_name: module.name,
                studyOnly: studyOnly,
                target: target,
                unit: module.unit || '%',
                bestScore: bestScore,
                testCount: studentRecords.length,
                passCount: passCount,
                passRate: passRate,
                practicedCount: practicedCount,
                speakingTotalQ: speakingTotalQ,
                totalSeconds: totalSeconds,
                todaySeconds: todaySeconds,
                status: status,
                statusText: statusText,
                statusClass: statusClass
            });
        }
    }
    return rows;
}

function setProgressColumnFilter(key, value) {
    _progressColumnFilters[key] = value || '';
    renderTeacherProgressSummary();
}

function toggleProgressStudentFilter(studentId) {
    const selected = new Set(_progressColumnFilters.studentIds || []);
    if (selected.has(studentId)) selected.delete(studentId);
    else selected.add(studentId);
    _progressColumnFilters.studentIds = Array.from(selected);
    renderTeacherProgressSummary();
    reopenFilterMenu('progressStudentFilter');
}

function clearProgressStudentFilter() {
    _progressColumnFilters.studentIds = [];
    renderTeacherProgressSummary();
    reopenFilterMenu('progressStudentFilter');
}

function progressMatchesFilters(row) {
    const f = _progressColumnFilters;
    if (f.studentId && !recordTextIncludes(row.student_id, f.studentId)) return false;
    if (f.studentIds && f.studentIds.length > 0 && f.studentIds.indexOf(row.student_id) < 0) return false;
    if (f.module && row.module_id !== f.module) return false;
    if (f.targetUnit && row.unit !== f.targetUnit) return false;
    if (!numericRangeMatches(row.bestScore, f.bestScoreRange)) return false;
    if (!numericRangeMatches(row.testCount, f.testCountRange)) return false;
    if (!numericRangeMatches(row.passCount, f.passCountRange)) return false;
    if (!numericRangeMatches(row.passRate, f.passRateRange)) return false;
    if (!numericRangeMatches(row.totalSeconds, f.totalDurationRange)) return false;
    if (!numericRangeMatches(row.todaySeconds, f.todayDurationRange)) return false;
    if (f.status && row.status !== f.status) return false;
    return true;
}

function renderTeacherProgressSummary() {
    const container = document.getElementById('teacherStudentProgress');
    const filteredRows = (_cachedProgressRows || []).filter(progressMatchesFilters);
    const studentOptions = (_teacherStudents || []).map(function(s) {
        return { id: s.student_id, name: s.name };
    }).sort(function(a, b) {
        return a.name.localeCompare(b.name, 'zh-CN') || a.id.localeCompare(b.id);
    });
    let moduleOptions = '<option value="">全部</option>';
    MODULES.filter(isModuleAvailable).forEach(function(m) {
        const selected = _progressColumnFilters.module === m.id ? ' selected' : '';
        moduleOptions += '<option value="' + escapeHtml(m.id) + '"' + selected + '>' + escapeHtml(m.name) + '</option>';
    });
    const unitOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '%', label: '百分比' },
        { value: '个', label: '个数' },
        { value: '分', label: '分数' },
        { value: '倍', label: '倍速' }
    ], _progressColumnFilters.targetUnit);
    const scoreOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-59', label: '0-59%' },
        { value: '60-69', label: '60-69%' },
        { value: '70-79', label: '70-79%' },
        { value: '80-89', label: '80-89%' },
        { value: '90-100', label: '90-100%' }
    ], _progressColumnFilters.bestScoreRange);
    const countOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-0', label: '0次' },
        { value: '1-1', label: '1次' },
        { value: '2-3', label: '2-3次' },
        { value: '4-5', label: '4-5次' },
        { value: '6+', label: '6次以上' }
    ], '');
    const totalDurationOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-0', label: '无' },
        { value: '1-599', label: '10分钟内' },
        { value: '600-1799', label: '10-30分钟' },
        { value: '1800-3599', label: '30-60分钟' },
        { value: '3600+', label: '1小时以上' }
    ], _progressColumnFilters.totalDurationRange);
    const todayDurationOptions = buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-0', label: '无' },
        { value: '1-599', label: '10分钟内' },
        { value: '600-1799', label: '10-30分钟' },
        { value: '1800-3599', label: '30-60分钟' },
        { value: '3600+', label: '1小时以上' }
    ], _progressColumnFilters.todayDurationRange);

    let html = '<div class="records-table-wrap"><table class="records-table progress-table"><thead>';
    html += '<tr class="records-filter-row">';
    html += '<th><input class="records-filter-control" value="' + escapeHtml(_progressColumnFilters.studentId) + '" oninput="setProgressColumnFilter(\'studentId\',this.value)"></th>';
    html += '<th>' + buildStudentMultiFilter('progressStudentFilter', studentOptions, _progressColumnFilters.studentIds, 'toggleProgressStudentFilter', 'clearProgressStudentFilter') + '</th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'module\',this.value)">' + moduleOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'targetUnit\',this.value)">' + unitOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'bestScoreRange\',this.value)">' + scoreOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'testCountRange\',this.value)">' + buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-0', label: '0次' },
        { value: '1-1', label: '1次' },
        { value: '2-3', label: '2-3次' },
        { value: '4-5', label: '4-5次' },
        { value: '6+', label: '6次以上' }
    ], _progressColumnFilters.testCountRange) + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'passCountRange\',this.value)">' + buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-0', label: '0次' },
        { value: '1-1', label: '1次' },
        { value: '2-3', label: '2-3次' },
        { value: '4-5', label: '4-5次' },
        { value: '6+', label: '6次以上' }
    ], _progressColumnFilters.passCountRange) + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'passRateRange\',this.value)">' + buildSelectOptions([
        { value: '', label: '全部' },
        { value: '0-59', label: '0-59%' },
        { value: '60-69', label: '60-69%' },
        { value: '70-79', label: '70-79%' },
        { value: '80-89', label: '80-89%' },
        { value: '90-100', label: '90-100%' }
    ], _progressColumnFilters.passRateRange) + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'totalDurationRange\',this.value)">' + totalDurationOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'todayDurationRange\',this.value)">' + todayDurationOptions + '</select></th>';
    html += '<th><select class="records-filter-control" onchange="setProgressColumnFilter(\'status\',this.value)"><option value="">全部</option><option value="passed"' + (_progressColumnFilters.status === 'passed' ? ' selected' : '') + '>已达标</option><option value="in_progress"' + (_progressColumnFilters.status === 'in_progress' ? ' selected' : '') + '>进行中</option><option value="not_started"' + (_progressColumnFilters.status === 'not_started' ? ' selected' : '') + '>未开始</option></select></th>';
    html += '</tr>';
    html += '<tr class="records-header-row"><th>学号</th><th>姓名</th><th>模块</th><th>达标线</th><th>最高分</th><th>测试次数</th><th>达标次数</th><th>达标率</th><th>模块练习时长</th><th>今日练习时长</th><th>状态</th></tr></thead><tbody>';

    for (let i = 0; i < filteredRows.length; i++) {
        const row = filteredRows[i];
        html += '<tr style="cursor:pointer;" onclick="showStudentDetailProgress(\'' + escapeJsString(row.student_id) + '\', \'' + escapeJsString(row.student_name) + '\', \'' + escapeJsString(row.module_id) + '\')">';
        html += '<td>' + escapeHtml(row.student_id) + '</td>';
        html += '<td><strong style="color:#667eea; text-decoration:underline;">' + escapeHtml(row.student_name) + '</strong></td>';
        if (row.module_id === 'speaking' && row.practicedCount > 0) {
            html += '<td>' + escapeHtml(row.module_name) + '<div style="color:#666;font-size:0.75rem;margin-top:2px;">已练 ' + row.practicedCount + (row.speakingTotalQ > 0 ? (' / ' + row.speakingTotalQ) : '') + ' 题</div></td>';
        } else {
            html += '<td>' + escapeHtml(row.module_name) + '</td>';
        }
        html += '<td class="numeric-cell">' + (row.studyOnly ? '—' : escapeHtml(formatTargetValue(row.target, row.unit))) + '</td>';
        html += '<td class="numeric-cell">' + (row.studyOnly ? '—' : (row.testCount > 0 ? escapeHtml(formatTargetValue(row.bestScore, row.unit)) : '-')) + '</td>';
        html += '<td class="numeric-cell">' + (row.studyOnly ? '—' : row.testCount) + '</td>';
        html += '<td class="numeric-cell">' + (row.studyOnly ? '—' : row.passCount) + '</td>';
        html += '<td class="numeric-cell">' + (row.studyOnly ? '—' : (row.testCount > 0 ? row.passRate + '%' : '-')) + '</td>';
        html += '<td class="numeric-cell">' + escapeHtml(formatDuration(row.totalSeconds)) + '</td>';
        html += '<td class="numeric-cell">' + escapeHtml(formatDuration(row.todaySeconds)) + '</td>';
        html += '<td><span class="badge ' + row.statusClass + '">' + row.statusText + '</span></td>';
        html += '</tr>';
    }
    if (filteredRows.length === 0) {
        html += '<tr><td colspan="11" style="text-align:center;color:#666;padding:20px;">暂无学习进度</td></tr>';
    }
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

async function showStudentDetailProgress(studentId, studentName, filterModuleId) {
    const container = document.getElementById('teacherStudentProgress');
    if (filterModuleId === undefined || filterModuleId === null) {
        filterModuleId = '';
    } else if (!filterModuleId) {
        filterModuleId = _progressColumnFilters.module || 'dictation';
    }
    const module = filterModuleId ? getModuleById(filterModuleId) : null;
    const moduleName = module ? module.name : '';

    const detailResult = await teacherApiGet('/api/teacher/student-detail?student_id=' + encodeURIComponent(studentId));
    if (detailResult.error) {
        showToast((detailResult.error && detailResult.error.message) || '加载学生详情失败', 'error');
        return;
    }
    const records = (detailResult.data && detailResult.data.test_records) || [];
    const wrongCount = ((detailResult.data && detailResult.data.wrong_words) || []).length;
    const rawSessions = (detailResult.data && detailResult.data.study_sessions) || [];
    const allSessions = getStudySessions(rawSessions);
    const selectedRecords = filterModuleId ? getModuleRecords(records, filterModuleId) : records;
    const selectedSessions = filterModuleId ? getModuleStudySessions(allSessions, filterModuleId) : allSessions;
    const selectedBestScore = getBestScore(selectedRecords);
    const selectedPassCount = getPassCount(selectedRecords);
    const selectedSeconds = window.TrackingUtils.sumPracticeSeconds(rawSessions, records, filterModuleId ? { moduleId: filterModuleId } : {});

    let html = '<div style="margin-bottom:20px;">';
    html += '<button class="btn btn-sm btn-secondary" onclick="loadTeacherProgressData()"> 返回汇总</button>';
    html += '<h3 style="display:inline-block; margin-left:20px;">' + escapeHtml(studentName) + (moduleName ? (' 的' + moduleName + '进度') : ' 的学习进度') + '</h3>';
    html += '</div>';

    const studentTargetScore = (detailResult.data && detailResult.data.student && detailResult.data.student.target_score != null)
        ? detailResult.data.student.target_score
        : 6.5;

    html += '<div style="margin-bottom:15px; padding:15px; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:10px; color:white;">';
    html += '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; text-align:center;">';
    const selectedPracticed = filterModuleId === 'speaking' ? getSpeakingPracticedCount(selectedSessions) : null;
    html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + formatDuration(selectedSeconds) + '</div><div style="font-size:0.85rem; opacity:0.9;">' + (filterModuleId ? '本模块练习时长' : '全部练习时长') + '</div></div>';
    if (selectedPracticed != null) {
        html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + selectedPracticed + '</div><div style="font-size:0.85rem; opacity:0.9;">已练题目</div></div>';
    } else {
        html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + selectedRecords.length + '</div><div style="font-size:0.85rem; opacity:0.9;">' + (filterModuleId ? '本模块测试次数' : '全部测试次数') + '</div></div>';
    }
    if (filterModuleId) {
        html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + (selectedRecords.length > 0 ? formatTargetValue(selectedBestScore, module && module.unit) : '-') + '</div><div style="font-size:0.85rem; opacity:0.9;">本模块最高分</div></div>';
    } else {
        html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + (selectedRecords.length > 0 ? Math.round(selectedPassCount / selectedRecords.length * 100) : 0) + '%</div><div style="font-size:0.85rem; opacity:0.9;">总达标率</div></div>';
    }
    html += '<div><div style="font-size:1.3rem; font-weight:bold;">' + wrongCount + '</div><div style="font-size:0.85rem; opacity:0.9;">听写未掌握错词</div></div>';
    html += '</div></div>';

    html += '<table style="width:100%; border-collapse: collapse;">';
    html += '<thead><tr style="background:#f8f9fa;">';
    html += '<th style="padding:12px; text-align:left; border-bottom:2px solid #dee2e6;">科目</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">目标</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">测试进度</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">测试次数</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">达标次数</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">状态</th>';
    html += '<th style="padding:12px; text-align:center; border-bottom:2px solid #dee2e6;">练习时长</th>';
    html += '</tr></thead><tbody>';

    // 教师详情与学生端一致：只展示已开放模块，其余先隐藏
    const availableModules = MODULES.filter(isModuleAvailable);
    for (let i = 0; i < availableModules.length; i++) {
        const m = availableModules[i];
        const moduleTarget = getModuleTargetForScore(m, studentTargetScore);
        const moduleRecords = getModuleRecords(records, m.id);
        const bestScore = getBestScore(moduleRecords);
        const passCount = getPassCount(moduleRecords);
        const moduleTotalSeconds = window.TrackingUtils.sumPracticeSeconds(rawSessions, records, { moduleId: m.id });
        const studyOnly = isStudyOnlyModule(m);
        const progressPercent = (!studyOnly && bestScore > 0) ? Math.min(100, Math.round((bestScore / moduleTarget) * 100)) : 0;
        let statusClass = 'badge-info';
        let statusText = '未开始';
        if (!studyOnly && bestScore >= moduleTarget && bestScore > 0) {
            statusClass = 'badge-success';
            statusText = '达标';
        } else if ((!studyOnly && moduleRecords.length > 0) || moduleTotalSeconds > 0) {
            statusClass = 'badge-warning';
            statusText = '进行中';
        }

        const progressColor = progressPercent >= 100 ? '#28a745' : '#667eea';

        html += '<tr style="border-bottom:1px solid #dee2e6;">';
        html += '<td style="padding:15px 12px;"><strong>' + m.name + '</strong></td>';
        html += '<td style="padding:15px 12px; text-align:center;">' + (studyOnly ? '—' : formatTargetValue(moduleTarget, m.unit)) + '</td>';
        html += '<td style="padding:15px 12px; min-width:150px;">';
        if (studyOnly) {
            html += '<span style="color:#888;">仅练习</span>';
        } else {
            html += '<div style="display:flex; align-items:center; gap:10px;">';
            html += '<div style="flex:1; background:#e9ecef; border-radius:10px; height:8px; overflow:hidden;">';
            html += '<div style="width:' + progressPercent + '%; background:' + progressColor + '; height:100%; transition:width 0.3s;"></div>';
            html += '</div>';
            html += '<span style="min-width:50px; text-align:right;">' + (moduleRecords.length > 0 ? bestScore + '%' : '0%') + '</span>';
            html += '</div>';
        }
        html += '</td>';
        html += '<td style="padding:15px 12px; text-align:center;">' + (studyOnly ? '—' : moduleRecords.length) + '</td>';
        html += '<td style="padding:15px 12px; text-align:center;">' + (studyOnly ? '—' : passCount) + '</td>';
        html += '<td style="padding:15px 12px; text-align:center;"><span class="badge ' + statusClass + '" style="font-size:0.75rem;">' + statusText + '</span></td>';
        html += '<td style="padding:15px 12px; text-align:center; color:#666; font-size:0.9rem;">' + formatDuration(moduleTotalSeconds) + '</td>';
        html += '</tr>';
    }

    html += '</tbody></table>';

    const dailyRows = buildDailyPracticeRows(rawSessions, records, filterModuleId).slice(0, 14);
    html += '<div style="margin-top:25px;"><h4 style="margin-bottom:12px;">每日练习时长</h4>';
    if (dailyRows.length === 0) {
        html += '<p style="color:#666; padding:12px; background:#f8f9fa; border-radius:8px;">暂无练习时长记录</p>';
    } else {
        html += '<table style="width:100%; border-collapse:collapse;"><thead><tr style="background:#f8f9fa;">';
        if (filterModuleId) {
            html += '<th style="padding:10px; text-align:left;">日期</th><th style="padding:10px; text-align:center;">' + moduleName + '</th><th style="padding:10px; text-align:center;">当天总时长</th><th style="padding:10px; text-align:center;">当天练习次数</th>';
        } else {
            html += '<th style="padding:10px; text-align:left;">日期</th><th style="padding:10px; text-align:center;">当天总时长</th><th style="padding:10px; text-align:center;">当天练习次数</th>';
        }
        html += '</tr></thead><tbody>';
        for (let j = 0; j < dailyRows.length; j++) {
            const row = dailyRows[j];
            html += '<tr style="border-bottom:1px solid #dee2e6;"><td style="padding:10px;">' + row.date + '</td>';
            if (filterModuleId) html += '<td style="padding:10px; text-align:center;">' + formatDuration(row.moduleSeconds) + '</td>';
            html += '<td style="padding:10px; text-align:center;">' + formatDuration(row.totalSeconds) + '</td><td style="padding:10px; text-align:center;">' + row.totalCount + '</td></tr>';
        }
        html += '</tbody></table>';
    }
    html += '</div>';

    html += '<div style="margin-top:30px; padding:20px; background:#f8f9fa; border-radius:10px;">';
    html += '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; text-align:center;">';
    html += '<div><div style="font-size:1.5rem; font-weight:bold; color:#667eea;">' + records.length + '</div><div style="color:#666; font-size:0.9rem;">全部测试次数</div></div>';
    html += '<div><div style="font-size:1.5rem; font-weight:bold; color:#28a745;">' + selectedPassCount + '</div><div style="color:#666; font-size:0.9rem;">' + (filterModuleId ? '本模块达标次数' : '达标次数') + '</div></div>';
    html += '<div><div style="font-size:1.5rem; font-weight:bold; color:#11998e;">' + (selectedRecords.length > 0 ? Math.round(selectedPassCount / selectedRecords.length * 100) : 0) + '%</div><div style="color:#666; font-size:0.9rem;">' + (filterModuleId ? '本模块达标率' : '总达标率') + '</div></div>';
    html += '<div><div style="font-size:1.5rem; font-weight:bold; color:#764ba2;">' + formatDuration(window.TrackingUtils.sumPracticeSeconds(rawSessions, records)) + '</div><div style="color:#666; font-size:0.9rem;">全部练习时长</div></div>';
    html += '</div></div>';

    container.innerHTML = html;
}

async function loadTeacherStudentProgress() {
    renderTeacherProgressSummary();
}

async function loadStandards() {
    const result = await teacherApiGet('/api/teacher/standards');
    const container = document.getElementById('standardsList');
    // 达标标准也只展示学生端已开放模块，其余先隐藏
    const availableIds = {};
    MODULES.filter(isModuleAvailable).forEach(function(m) { availableIds[m.id] = true; });
    const standards = (result.data || []).filter(function(s) { return availableIds[s.module_type]; });
    if (!standards || standards.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:20px;">暂无模块配置</p>';
        return;
    }
    let html = '';
    for (let i = 0; i < standards.length; i++) {
        const s = standards[i];
        html += '<div style="padding:20px;background:#f8f9fa;border-radius:10px;margin-bottom:15px;"><h4 style="margin-bottom:15px;">' + s.module_name + '</h4><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;"><div class="input-group"><label>6分达标线</label><input type="number" id="std6_' + s.module_type + '" value="' + s.score_6 + '" onchange="updateStandard(\'' + s.module_type + '\', \'score_6\', this.value)"></div><div class="input-group"><label>6.5分达标线</label><input type="number" id="std65_' + s.module_type + '" value="' + s.score_6_5 + '" onchange="updateStandard(\'' + s.module_type + '\', \'score_6_5\', this.value)"></div><div class="input-group"><label>7分达标线</label><input type="number" id="std7_' + s.module_type + '" value="' + s.score_7 + '" onchange="updateStandard(\'' + s.module_type + '\', \'score_7\', this.value)"></div></div></div>';
    }
    container.innerHTML = html;
}

async function updateStandard(moduleType, field, value) {
    const update = {};
    update[field] = parseFloat(value);
    update.updated_at = new Date().toISOString();
    update.module_type = moduleType;
    const result = await teacherApiPost('/api/teacher/standards/update', update);
    if (result.error) { showToast((result.error && result.error.message) || '更新失败', 'error'); return; }
    showToast('已更新', 'success');
}

function switchTeacherTab(tab, evt, options) {
    var tabs = document.querySelectorAll('#teacherDashboard .tab');
    tabs.forEach(function(t, i) {
        t.classList.remove('active');
        var id = t.getAttribute('onclick') || '';
        if (id.indexOf("'" + tab + "'") >= 0) {
            t.classList.add('active');
        }
    });
    document.getElementById('tabStudents').style.display = tab === 'students' ? 'block' : 'none';
    document.getElementById('tabRecords').style.display = tab === 'records' ? 'block' : 'none';
    document.getElementById('tabProgress').style.display = tab === 'progress' ? 'block' : 'none';
    var tabActive = document.getElementById('tabActive');
    if (tabActive) tabActive.style.display = tab === 'active' ? 'block' : 'none';
    document.getElementById('tabWriting').style.display = tab === 'writing' ? 'block' : 'none';
    document.getElementById('tabStandards').style.display = tab === 'standards' ? 'block' : 'none';
    var tabTeachers = document.getElementById('tabTeachers');
    if (tabTeachers) tabTeachers.style.display = (tab === 'teachers' && isAdminTeacher()) ? 'block' : 'none';
    document.body.classList.toggle('teacher-writing-wide', tab === 'writing');
    if (tab === 'records') {
        loadRecords();
    }
    if (tab === 'progress' && !(options && options.skipLoad)) {
        loadTeacherProgressData();
    }
    if (tab === 'active') {
        loadActiveStudents();
    }
    if (tab === 'writing') {
        var frame = document.getElementById('writingReportsIframe');
        if (frame) {
            frame.src = '../xiezuopigai/ielts-writing-backend/teacher.html?v=12&_=' + Date.now();
            frame.setAttribute('data-loaded', '1');
        }
    }
    if (tab === 'teachers') {
        if (!isAdminTeacher()) {
            showToast('仅管理员可管理教师账号', 'error');
            switchTeacherTab('students');
            return;
        }
        loadTeachers();
    }
}

function showAddStudentModal() { showModal('addStudentModal'); }

function showAddTeacherModal() {
    if (!isAdminTeacher()) {
        showToast('仅管理员可添加教师', 'error');
        return;
    }
    showModal('addTeacherModal');
}

async function addStudent() {
    const name = document.getElementById('newStudentName').value.trim();
    const targetScore = parseFloat(document.getElementById('newStudentTarget').value);
    if (!name) { showToast('请输入姓名', 'error'); return; }
    const insertResult = await teacherApiPost('/api/teacher/students', {
        name: name,
        target_score: targetScore
    });
    if (insertResult.error) {
        showToast('添加失败：' + ((insertResult.error && insertResult.error.message) || '未知错误'), 'error');
        return;
    }
    const newId = insertResult.data && insertResult.data.student_id;
    const initialPassword = insertResult.data && insertResult.data.password;
    closeModal('addStudentModal');
    document.getElementById('newStudentName').value = '';
    showToast('添加成功！学号：' + newId + '，初始密码：' + initialPassword, 'success');
    loadStudents();
}


async function loadTeachers() {
    if (!isAdminTeacher()) return;
    const result = await teacherApiGet('/api/teacher/teachers');
    const container = document.getElementById('teachersList');
    if (!container) return;
    const teachers = result.data || [];
    if (!teachers.length) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:20px;">暂无教师账号</p>';
        return;
    }
    let html = '<table><thead><tr><th>账号</th><th>姓名</th><th>职位</th><th>科目</th><th>状态</th><th>操作</th></tr></thead><tbody>';
    for (let i = 0; i < teachers.length; i++) {
        const t = teachers[i];
        const statusBadge = t.status === 'active' ? 'badge-success">正常' : 'badge-danger">禁用';
        const isAdminRow = t.teacher_id === 'admin';
        const toggleLabel = t.status === 'active' ? '禁用' : '启用';
        const toggleClass = t.status === 'active' ? 'btn-danger' : 'btn-success';
        let actions = '';
        if (!isAdminRow) {
            actions += '<button class="btn btn-sm btn-secondary" onclick="resetTeacherPassword(\'' + escapeJsString(t.teacher_id) + '\')">重置密码</button>';
            actions += '<button class="btn btn-sm ' + toggleClass + '" onclick="toggleTeacherStatus(\'' + escapeJsString(t.teacher_id) + '\', \'' + escapeJsString(t.status) + '\')">' + toggleLabel + '</button>';
        } else {
            actions = '<span style="color:#999;font-size:0.85rem;">系统管理员</span>';
        }
        html += '<tr><td>' + escapeHtml(t.teacher_id) + '</td><td>' + escapeHtml(t.name) + '</td><td>' + escapeHtml(t.position || '') + '</td><td>' + escapeHtml(t.subjects || '') + '</td><td><span class="badge ' + statusBadge + '</span></td><td><div class="student-actions">' + actions + '</div></td></tr>';
    }
    html += '</tbody></table>';
    container.innerHTML = html;
}

async function addTeacher() {
    if (!isAdminTeacher()) { showToast('仅管理员可添加教师', 'error'); return; }
    const name = document.getElementById('newTeacherName').value.trim();
    const account = document.getElementById('newTeacherAccount').value.trim().toLowerCase();
    const position = document.getElementById('newTeacherPosition').value.trim();
    const subjects = document.getElementById('newTeacherSubjects').value.trim();
    if (!name) { showToast('请输入姓名', 'error'); return; }
    if (!account) { showToast('请输入登录账号', 'error'); return; }
    if (!/^[a-z0-9_]+$/.test(account)) {
        showToast('账号仅支持小写字母、数字、下划线', 'error');
        return;
    }
    if (account === 'admin') {
        showToast('不能使用保留账号 admin', 'error');
        return;
    }
    const insertResult = await teacherApiPost('/api/teacher/teachers', {
        teacher_id: account,
        name: name,
        position: position,
        subjects: subjects
    });
    if (insertResult.error) {
        showToast('添加失败：' + ((insertResult.error && insertResult.error.message) || '未知错误'), 'error');
        return;
    }
    const initialPassword = (insertResult.data && insertResult.data.password) || '';
    closeModal('addTeacherModal');
    document.getElementById('newTeacherName').value = '';
    document.getElementById('newTeacherAccount').value = '';
    document.getElementById('newTeacherPosition').value = '';
    document.getElementById('newTeacherSubjects').value = '';
    showToast('添加成功！账号：' + account + '，初始密码：' + initialPassword, 'success');
    loadTeachers();
}

async function resetTeacherPassword(teacherId) {
    if (!isAdminTeacher()) { showToast('仅管理员可操作', 'error'); return; }
    if (teacherId === 'admin') { showToast('不能重置管理员密码', 'error'); return; }
    if (!confirm('确定将该教师密码重置为默认初始密码？')) return;
    const result = await teacherApiPost('/api/teacher/teachers/reset-password', { teacher_id: teacherId });
    if (result.error) {
        showToast((result.error && result.error.message) || '重置失败', 'error');
        return;
    }
    const resetPassword = (result.data && result.data.password) || '';
    showToast('密码已重置为 ' + resetPassword, 'success');
}

async function toggleTeacherStatus(teacherId, currentStatus) {
    if (!isAdminTeacher()) { showToast('仅管理员可操作', 'error'); return; }
    if (teacherId === 'admin') { showToast('不能禁用管理员', 'error'); return; }
    const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
    const result = await teacherApiPost('/api/teacher/teachers/toggle-status', { teacher_id: teacherId });
    if (result.error) {
        showToast((result.error && result.error.message) || '操作失败', 'error');
        return;
    }
    loadTeachers();
    showToast('教师已' + (newStatus === 'active' ? '启用' : '禁用'), 'success');
}

function showBatchImportModal() { showModal('batchImportModal'); }

async function batchImportStudents() {
    const text = document.getElementById('batchStudentList').value.trim();
    if (!text) { showToast('请输入学生列表', 'error'); return; }
    const lines = text.split('\n').filter(function(l) { return l.trim(); });
    const students = [];
    for (let i = 0; i < lines.length; i++) {
        const parts = lines[i].split(',');
        const name = parts[0].trim();
        const target = parts[1] ? parseFloat(parts[1].trim()) : 6.5;
        if (name) {
            students.push({
                name: name,
                target_score: target
            });
        }
    }
    if (students.length === 0) { showToast('没有有效的学生数据', 'error'); return; }
    const insertResult = await teacherApiPost('/api/teacher/students/batch', { students: students });
    if (insertResult.error) {
        showToast('导入失败：' + ((insertResult.error && insertResult.error.message) || '未知错误'), 'error');
        return;
    }
    closeModal('batchImportModal');
    document.getElementById('batchStudentList').value = '';
    const count = (insertResult.data && insertResult.data.count) || students.length;
    showToast('成功导入 ' + count + ' 名学生', 'success');
    loadStudents();
}


async function resetPassword(studentId) {
    if (!confirm('确定重置该学生密码为默认初始密码？')) return;
    const result = await teacherApiPost('/api/teacher/students/reset-password', { student_id: studentId });
    if (result.error) { showToast((result.error && result.error.message) || '重置失败', 'error'); return; }
    var pwd = (result.data && result.data.password) || '';
    showToast('密码已重置为 ' + pwd + '，请告知学生用此密码登录并修改密码', 'success');
}

async function toggleStatus(studentId, currentStatus) {
    const result = await teacherApiPost('/api/teacher/students/toggle-status', { student_id: studentId });
    if (result.error) { showToast((result.error && result.error.message) || '操作失败', 'error'); return; }
    const newStatus = (result.data && result.data.status) || (currentStatus === 'active' ? 'inactive' : 'active');
    loadStudents();
    showToast('学生已' + (newStatus === 'active' ? '启用' : '禁用'), 'success');
}

async function exportStudentsExcel() {
    const result = await teacherApiGet('/api/teacher/students');
    if (!result.data) return;
    const data = result.data.map(function(s) {
        return {
            '学号': s.student_id,
            '姓名': s.name,
            '目标分数': s.target_score,
            '状态': s.status === 'active' ? '正常' : '禁用',
            '创建时间': new Date(s.created_at).toLocaleString('zh-CN')
        };
    });
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '学生名单');
    XLSX.writeFile(wb, '学生名单_' + new Date().toISOString().slice(0,10) + '.xlsx');
    showToast('导出成功', 'success');
}

async function exportRecordsExcel() {
    const result = await teacherApiGet('/api/teacher/test-records?limit=5000');
    if (!result.data) return;
    const data = result.data.map(function(r) {
        return {
            '学号': r.student_id,
            '姓名': r.students ? r.students.name : '-',
            '测试类型': r.test_type === 'random' ? '随机测试' : '错题测试',
            '正确率': r.score + '%',
            '达标': r.is_passed ? '是' : '否',
            '达标线': r.pass_threshold + '%',
            '时间': new Date(r.created_at).toLocaleString('zh-CN')
        };
    });
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '测试记录');
    XLSX.writeFile(wb, '测试记录_' + new Date().toISOString().slice(0,10) + '.xlsx');
    showToast('导出成功', 'success');
}

// 音频上下文解锁标记
var audioUnlocked = false;

// 解锁音频上下文（必须在用户交互后调用）

// 点击搜索框外部区域时关闭下拉列表
document.addEventListener('click', function(e) {
    if (!e.target.closest || !e.target.closest('.multi-filter')) {
        document.querySelectorAll('.multi-filter.open').forEach(function(el) {
            el.classList.remove('open');
        });
        document.querySelectorAll('.filter-cell-open').forEach(function(el) {
            el.classList.remove('filter-cell-open');
        });
    }
});
