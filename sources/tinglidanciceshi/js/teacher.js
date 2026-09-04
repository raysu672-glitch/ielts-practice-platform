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
        const toggleLabel = s.status === 'active' ? '禁用' : '启用';
        const toggleClass = s.status === 'active' ? 'btn-danger' : 'btn-success';
        html += '<tr><td>' + escapeHtml(s.student_id) + '</td><td>' + studentNameLinkHtml(s.student_id, s.name) + '</td><td>' + s.target_score + '分</td><td><span class="badge ' + statusBadge + '</span></td><td><div class="student-actions">';
        html += '<button class="btn btn-sm btn-secondary" onclick="showEditStudentModal(\'' + escapeJsString(s.student_id) + '\',\'' + escapeJsString(s.name) + '\',\'' + escapeJsString(String(s.target_score)) + '\')">修改</button>';
        html += '<button class="btn btn-sm btn-secondary" onclick="resetPassword(\'' + escapeJsString(s.student_id) + '\')">重置密码</button>';
        html += '<button class="btn btn-sm ' + toggleClass + '" onclick="toggleStatus(\'' + escapeJsString(s.student_id) + '\',\'' + escapeJsString(s.status) + '\')">' + toggleLabel + '</button>';
        html += '</div></td></tr>';
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
            html += '<span style="min-width:50px; text-align:right;">' + (moduleRecords.length > 0 ? formatTargetValue(bestScore, m.unit) : formatTargetValue(0, m.unit)) + '</span>';
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
    const byType = {};
    (result.data || []).forEach(function(s) {
        if (s && s.module_type) byType[s.module_type] = s;
    });
    const modules = MODULES.filter(isModuleAvailable);
    if (!modules.length) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:20px;">暂无模块配置</p>';
        return;
    }
    let html = '';
    for (let i = 0; i < modules.length; i++) {
        const m = modules[i];
        const s = byType[m.id] || {};
        const unit = m.unit || '%';
        const unitHint = unit === '个'
            ? '答对题数（个），不是百分比'
            : (unit === '%' ? '正确率（%）' : ('单位：' + unit));
        const step = unit === '分' ? '0.5' : '1';
        const score6 = s.score_6 != null ? s.score_6 : (m.targets ? m.targets[6] : '');
        const score65 = s.score_6_5 != null ? s.score_6_5 : (m.targets ? m.targets[6.5] : '');
        const score7 = s.score_7 != null ? s.score_7 : (m.targets ? m.targets[7] : '');
        html += '<div style="padding:20px;background:#f8f9fa;border-radius:10px;margin-bottom:15px;">';
        html += '<h4 style="margin-bottom:6px;">' + escapeHtml(m.name) + '</h4>';
        html += '<p style="color:#666;font-size:0.85rem;margin:0 0 12px;">' + escapeHtml(unitHint) + '</p>';
        html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;">';
        html += '<div class="input-group"><label>6分达标线（' + escapeHtml(unit) + '）</label>';
        html += '<input type="number" min="0" step="' + step + '" id="std6_' + m.id + '" value="' + score6 + '" onchange="updateStandard(\'' + m.id + '\', \'score_6\', this.value)"></div>';
        html += '<div class="input-group"><label>6.5分达标线（' + escapeHtml(unit) + '）</label>';
        html += '<input type="number" min="0" step="' + step + '" id="std65_' + m.id + '" value="' + score65 + '" onchange="updateStandard(\'' + m.id + '\', \'score_6_5\', this.value)"></div>';
        html += '<div class="input-group"><label>7分达标线（' + escapeHtml(unit) + '）</label>';
        html += '<input type="number" min="0" step="' + step + '" id="std7_' + m.id + '" value="' + score7 + '" onchange="updateStandard(\'' + m.id + '\', \'score_7\', this.value)"></div>';
        html += '</div></div>';
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
    var tabTasks = document.getElementById('tabTasks');
    if (tabTasks) tabTasks.style.display = tab === 'tasks' ? 'block' : 'none';
    var tabActive = document.getElementById('tabActive');
    if (tabActive) tabActive.style.display = tab === 'active' ? 'block' : 'none';
    document.getElementById('tabWriting').style.display = tab === 'writing' ? 'block' : 'none';
    var tabJianya = document.getElementById('tabJianya');
    if (tabJianya) tabJianya.style.display = tab === 'jianya' ? 'block' : 'none';
    document.getElementById('tabStandards').style.display = tab === 'standards' ? 'block' : 'none';
    var tabTeachers = document.getElementById('tabTeachers');
    if (tabTeachers) tabTeachers.style.display = (tab === 'teachers' && isAdminTeacher()) ? 'block' : 'none';
    document.body.classList.toggle('teacher-writing-wide', tab === 'writing' || tab === 'jianya');
    if (tab === 'tasks') {
        initTeacherTaskPlanTab();
    }
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
    if (tab === 'jianya') {
        var jianyaFrame = document.getElementById('jianyaTeacherIframe');
        if (jianyaFrame && jianyaFrame.getAttribute('data-src') !== '/jianyazhenti/teacher?embed=1') {
            jianyaFrame.src = '/jianyazhenti/teacher?embed=1';
            jianyaFrame.setAttribute('data-src', '/jianyazhenti/teacher?embed=1');
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

function showAddStudentModal() {
    window._editingStudentId = '';
    var title = document.getElementById('studentModalTitle');
    if (title) title.textContent = '添加学生';
    var idGroup = document.getElementById('editStudentIdGroup');
    if (idGroup) idGroup.style.display = 'none';
    var hint = document.getElementById('studentModalHint');
    if (hint) hint.textContent = '学号将自动生成，初始密码为 123456';
    var saveBtn = document.getElementById('studentModalSaveBtn');
    if (saveBtn) saveBtn.textContent = '添加';
    document.getElementById('newStudentName').value = '';
    document.getElementById('newStudentTarget').value = '6.5';
    showModal('addStudentModal');
}

function showEditStudentModal(studentId, name, targetScore) {
    window._editingStudentId = studentId || '';
    var title = document.getElementById('studentModalTitle');
    if (title) title.textContent = '修改学生';
    var idGroup = document.getElementById('editStudentIdGroup');
    if (idGroup) idGroup.style.display = '';
    var idInput = document.getElementById('editStudentId');
    if (idInput) idInput.value = studentId || '';
    var hint = document.getElementById('studentModalHint');
    if (hint) hint.textContent = '学号不可改。改姓名或目标分数后点保存。';
    var saveBtn = document.getElementById('studentModalSaveBtn');
    if (saveBtn) saveBtn.textContent = '保存';
    document.getElementById('newStudentName').value = name || '';
    var target = String(targetScore == null ? '6.5' : targetScore);
    if (target === '6.0') target = '6';
    document.getElementById('newStudentTarget').value = target;
    showModal('addStudentModal');
}

function showAddTeacherModal() {
    if (!isAdminTeacher()) {
        showToast('仅管理员可添加教师', 'error');
        return;
    }
    window._editingTeacherId = '';
    var title = document.getElementById('teacherModalTitle');
    if (title) title.textContent = '添加教师';
    var account = document.getElementById('newTeacherAccount');
    if (account) {
        account.value = '';
        account.disabled = false;
    }
    var hint = document.getElementById('teacherModalHint');
    if (hint) hint.textContent = '初始密码为 123456，教师可用账号密码登录教师后台';
    var saveBtn = document.getElementById('teacherModalSaveBtn');
    if (saveBtn) saveBtn.textContent = '添加';
    document.getElementById('newTeacherName').value = '';
    document.getElementById('newTeacherPosition').value = '';
    document.getElementById('newTeacherSubjects').value = '';
    showModal('addTeacherModal');
}

function showEditTeacherModal(teacherId, name, position, subjects) {
    if (!isAdminTeacher()) {
        showToast('仅管理员可修改教师', 'error');
        return;
    }
    window._editingTeacherId = teacherId || '';
    var title = document.getElementById('teacherModalTitle');
    if (title) title.textContent = '修改教师';
    var account = document.getElementById('newTeacherAccount');
    if (account) {
        account.value = teacherId || '';
        account.disabled = true;
    }
    var hint = document.getElementById('teacherModalHint');
    if (hint) hint.textContent = '登录账号不可改。可改姓名、职位、科目。';
    var saveBtn = document.getElementById('teacherModalSaveBtn');
    if (saveBtn) saveBtn.textContent = '保存';
    document.getElementById('newTeacherName').value = name || '';
    document.getElementById('newTeacherPosition').value = position || '';
    document.getElementById('newTeacherSubjects').value = subjects || '';
    showModal('addTeacherModal');
}

async function addStudent() {
    return saveStudent();
}

async function saveStudent() {
    if (window._savingStudent) return;
    const name = document.getElementById('newStudentName').value.trim();
    const targetScore = parseFloat(document.getElementById('newStudentTarget').value);
    if (!name) { showToast('请输入姓名', 'error'); return; }
    const editingId = window._editingStudentId || '';
    window._savingStudent = true;
    try {
        if (editingId) {
            const result = await teacherApiPost('/api/teacher/students/update', {
                student_id: editingId,
                name: name,
                target_score: targetScore
            });
            if (result.error) {
                showToast('保存失败：' + ((result.error && result.error.message) || '未知错误'), 'error');
                return;
            }
            window._editingStudentId = '';
            document.getElementById('newStudentName').value = '';
            closeModal('addStudentModal');
            showToast('学生信息已保存', 'success');
            loadStudents();
            return;
        }
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
    } finally {
        window._savingStudent = false;
    }
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
            actions += '<button class="btn btn-sm btn-secondary" onclick="showEditTeacherModal(\'' + escapeJsString(t.teacher_id) + '\',\'' + escapeJsString(t.name) + '\',\'' + escapeJsString(t.position || '') + '\',\'' + escapeJsString(t.subjects || '') + '\')">修改</button>';
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
    return saveTeacher();
}

async function saveTeacher() {
    if (!isAdminTeacher()) { showToast('仅管理员可操作教师账号', 'error'); return; }
    if (window._savingTeacher) return;
    const name = document.getElementById('newTeacherName').value.trim();
    const accountInput = document.getElementById('newTeacherAccount');
    const account = (window._editingTeacherId || (accountInput && accountInput.value) || '').trim().toLowerCase();
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
    const editingId = window._editingTeacherId || '';
    window._savingTeacher = true;
    try {
        if (editingId) {
            const result = await teacherApiPost('/api/teacher/teachers/update', {
                teacher_id: editingId,
                name: name,
                position: position,
                subjects: subjects
            });
            if (result.error) {
                showToast('保存失败：' + ((result.error && result.error.message) || '未知错误'), 'error');
                return;
            }
            window._editingTeacherId = '';
            if (accountInput) accountInput.disabled = false;
            document.getElementById('newTeacherName').value = '';
            document.getElementById('newTeacherPosition').value = '';
            document.getElementById('newTeacherSubjects').value = '';
            closeModal('addTeacherModal');
            showToast('教师信息已保存', 'success');
            loadTeachers();
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
    } finally {
        window._savingTeacher = false;
    }
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

// ── 任务计划（MVP）──────────────────────────────────────────────
var _taskDraftItems = [];
var _taskModuleQuotas = {};
var _taskLiveItems = [];
var _taskPlanPause = null;
var _taskHasDbDraft = false;
var _taskPendingEffectiveLabel = '';
var _taskUnitCatalog = [];
var _taskPendingPlanChange = false;
var _taskLibraryModule = '';
var _taskLibrarySearch = '';
var _stageTestModalModule = '';
var _taskPlanSubtab = 'overview';
var _taskOverviewData = null;
var _taskOverviewFilters = {
    incomplete: false,
    yesterdayIncomplete: false,
    backlog: false,
    refresh: false,
    testFail: false,
    attention: false,
    noPlan: false
};
/** true = 收起；undefined 也视为收起（默认全收） */
var _taskPlanCollapse = {};
var _taskLiveCollapse = {};
/** 有序清单当前展开操作菜单的行下标 */
var _taskPlanOpenMenuIdx = null;
/** 各科目是否展示已完成行；默认 false=收起已完成 */
var _taskPlanShowCompleted = {};
var _taskLiveShowCompleted = {};

/** 科目 Tab 顺序：阅读优先；未列出的新科目按中文名排在后面 */
var TASK_LIBRARY_MODULE_ORDER = [
    'reading_synonym',
    'dictation',
    'listening_basic',
    'listening_synonym',
    'sentence',
    'writing_phrase',
    'writing_translate',
    'listening_p4_speed',
    'speaking_complex',
    'speaking_p1',
    'speaking_p2_material',
    'speaking_p2_apply'
];

function taskLibraryModuleLabel(mt) {
    return taskModuleShortLabel(mt);
}

/** 清单里用的短科目名，避免「学 · 第2组」看不出科 */
function taskModuleShortLabel(mt) {
    var aliases = {
        reading_synonym: '阅读',
        dictation: '听力千词',
        listening_basic: '听力基础',
        listening_synonym: '听力同义',
        sentence: '长难句',
        writing_phrase: '写作词伙',
        writing_translate: '写作翻译',
        listening_p4_speed: '听力跟读',
        speaking_complex: '口语复合句',
        speaking_p1: '口语P1',
        speaking_p2_material: '口语P2素材',
        speaking_p2_apply: '口语P2套题'
    };
    if (mt && aliases[mt]) return aliases[mt];
    var mod = (typeof getModuleById === 'function') ? getModuleById(mt) : null;
    return (mod && mod.name) || mt || '未分科';
}

function normalizeTestUnitIds(raw) {
    if (Array.isArray(raw)) return raw.slice();
    if (typeof raw === 'string' && raw) {
        try {
            var parsed = JSON.parse(raw);
            if (Array.isArray(parsed)) return parsed.slice();
        } catch (e) { /* ignore */ }
    }
    return [];
}

function inferTaskItemModuleType(it, items) {
    if (it && it.module_type) return it.module_type;
    if (!it || it.item_type !== 'test') return '';
    var covers = normalizeTestUnitIds(it.test_unit_ids);
    var list = items || _taskDraftItems || [];
    for (var i = 0; i < covers.length; i++) {
        var row = list.find(function(x) {
            return x.item_type === 'study' && x.unit_id === covers[i];
        });
        if (row && row.module_type) return row.module_type;
    }
    return '';
}

function formatTaskPlanItemLabel(it, items) {
    var mt = inferTaskItemModuleType(it, items);
    var mod = taskModuleShortLabel(mt);
    var body = formatTaskPlanItemBody(it);
    return '<span style="display:inline-block;min-width:4.5em;color:#64748b;font-size:12px;">' +
        escapeTeacherAttr(mod) + '</span> ' + body;
}

function formatTaskPlanItemBody(it) {
    var body = it.item_type === 'test'
        ? ('测 · ' + (it.test_title || '阶段测'))
        : ('学 · ' + (it.unit_title || it.unit_id || ''));
    if (isTaskItemDone(it)) {
        body += ' <span style="color:#94a3b8;font-size:12px;">已完成</span>';
    }
    return body;
}

function isTaskItemDone(it) {
    if (!it) return false;
    if (it.item_type === 'test') return !!Number(it.test_passed);
    return !!Number(it.study_completed);
}

function toggleTaskPlanShowCompleted(mt) {
    _taskPlanShowCompleted[mt] = !_taskPlanShowCompleted[mt];
    renderTaskPlanList();
}

function toggleTaskLiveShowCompleted(mt) {
    _taskLiveShowCompleted[mt] = !_taskLiveShowCompleted[mt];
    renderTaskLivePlanList();
}

/** 段内展示顺序：未完成在前、已完成沉底（不改 sort_order） */
function orderSegmentIndicesForDisplay(items, indices, showCompleted) {
    var pending = [];
    var done = [];
    (indices || []).forEach(function(i) {
        if (isTaskItemDone(items[i])) done.push(i);
        else pending.push(i);
    });
    if (showCompleted) return pending.concat(done);
    return pending;
}

function groupTaskItemsByModuleSegments(items) {
    var segments = [];
    var cur = null;
    (items || []).forEach(function(it, idx) {
        var mt = inferTaskItemModuleType(it, items) || '_none';
        if (!cur || cur.moduleType !== mt) {
            cur = { moduleType: mt, indices: [] };
            segments.push(cur);
        }
        cur.indices.push(idx);
    });
    return segments;
}

function isTaskSectionCollapsed(mt, map) {
    // 默认展开：折叠时只看得到「待学 N」，容易误以为清单只有当天那几条
    if (!map) return false;
    if (map[mt] === undefined) return false;
    return !!map[mt];
}

function toggleTaskPlanSection(mt) {
    _taskPlanCollapse[mt] = !isTaskSectionCollapsed(mt, _taskPlanCollapse);
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
}

function toggleTaskLiveSection(mt) {
    _taskLiveCollapse[mt] = !isTaskSectionCollapsed(mt, _taskLiveCollapse);
    renderTaskLivePlanList();
}

function expandTaskPlanModule(mt) {
    if (!mt) return;
    _taskPlanCollapse[mt] = false;
}

function scrollTaskPlanSegmentIntoView(mt) {
    setTimeout(function() {
        var el = document.getElementById('taskPlanSeg_' + mt);
        if (el && el.scrollIntoView) {
            el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
    }, 40);
}

function toggleTaskRowMenu(idx) {
    _taskPlanOpenMenuIdx = _taskPlanOpenMenuIdx === idx ? null : idx;
    renderTaskPlanList();
}

function insertStageTestForModuleSegment(moduleType) {
    var lastStudy = -1;
    for (var i = 0; i < _taskDraftItems.length; i++) {
        var it = _taskDraftItems[i];
        if (it.item_type === 'study' && it.module_type === moduleType && it.unit_id) {
            lastStudy = i;
        }
    }
    if (lastStudy < 0) {
        showToast('该科目没有学习单元', 'error');
        return;
    }
    expandTaskPlanModule(moduleType);
    insertStageTestThrough(lastStudy);
}

function removeTaskDraftModuleSegment(moduleType) {
    var label = taskModuleShortLabel(moduleType);
    if (!window.confirm('确定移除「' + label + '」整段（该科目全部学/测）？')) return;
    var snapshot = _taskDraftItems.slice();
    _taskDraftItems = snapshot.filter(function(it) {
        return inferTaskItemModuleType(it, snapshot) !== moduleType;
    });
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    renderTaskUnitLibrary();
    schedulePackPreviewRefresh();
    showToast('已移除「' + label + '」整段（记得保存）', 'success');
}

function sortedTaskModuleTypes(catalog) {
    var set = {};
    (catalog || []).forEach(function(u) {
        if (u && u.module_type) set[u.module_type] = true;
    });
    var keys = Object.keys(set);
    keys.sort(function(a, b) {
        var ia = TASK_LIBRARY_MODULE_ORDER.indexOf(a);
        var ib = TASK_LIBRARY_MODULE_ORDER.indexOf(b);
        if (ia === -1 && ib === -1) {
            return taskLibraryModuleLabel(a).localeCompare(taskLibraryModuleLabel(b), 'zh');
        }
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
    });
    return keys;
}

function escapeTeacherAttr(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
}

function selectTaskLibraryModule(mt) {
    _taskLibraryModule = mt;
    _taskLibrarySearch = '';
    renderTaskUnitLibrary();
}

function onTaskUnitSearchInput(val) {
    _taskLibrarySearch = val || '';
    renderTaskUnitLibraryList();
}

function renderTaskUnitLibraryList() {
    var box = document.getElementById('taskUnitLibrary');
    if (!box) return;
    var planned = {};
    _taskDraftItems.forEach(function(it) {
        if (it.item_type === 'study' && it.unit_id && it.status !== 'removed') {
            planned[it.unit_id] = true;
        }
    });
    if (!_taskUnitCatalog.length) {
        box.innerHTML = '<p style="color:#666;margin:0;">暂无单元</p>';
        return;
    }
    var q = (_taskLibrarySearch || '').trim().toLowerCase();
    var units = _taskUnitCatalog.filter(function(u) {
        if (u.module_type !== _taskLibraryModule) return false;
        if (!q) return true;
        var title = (u.title || '').toLowerCase();
        var uid = (u.unit_id || '').toLowerCase();
        return title.indexOf(q) >= 0 || uid.indexOf(q) >= 0 || String(u.unit_no || '').indexOf(q) >= 0;
    }).sort(function(a, b) {
        return (a.unit_no || 0) - (b.unit_no || 0);
    });
    var html = '<div style="font-size:12px;color:#64748b;margin-bottom:6px;">' +
        taskLibraryModuleLabel(_taskLibraryModule) + ' · 显示 ' + units.length + ' 个' +
        (q ? '（已筛选）' : '') + '</div>';
    if (!units.length) {
        html += '<p style="color:#666;margin:0;">无匹配单元，请换关键词或切换科目</p>';
    } else {
        units.forEach(function(u) {
            var used = !!planned[u.unit_id];
            var noLabel = u.unit_no ? ('<span style="color:#94a3b8;font-size:12px;margin-right:6px;">#' + u.unit_no + '</span>') : '';
            html += '<div style="display:flex;justify-content:space-between;gap:8px;padding:4px 0;' +
                (used ? 'opacity:0.45;' : '') + '">';
            html += '<span>' + noLabel + (u.title || u.unit_id) + '</span>';
            html += used
                ? '<span style="color:#94a3b8;font-size:12px;">已排</span>'
                : '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:12px;" onclick="addUnitToTaskDraft(\'' +
                    u.unit_id + '\')">加入</button>';
            html += '</div>';
        });
    }
    box.innerHTML = html;
}

function renderTaskUnitLibrary() {
    var moduleTypes = sortedTaskModuleTypes(_taskUnitCatalog);
    renderTaskUnitLibraryToolbar(moduleTypes);
    renderTaskUnitLibraryList();
}

function batchAddTaskUnits() {
    var fromEl = document.getElementById('taskUnitBatchFrom');
    var toEl = document.getElementById('taskUnitBatchTo');
    var from = parseInt(fromEl && fromEl.value, 10);
    var to = parseInt(toEl && toEl.value, 10);
    if (isNaN(from) || isNaN(to)) {
        showToast('请输入有效序号', 'error');
        return;
    }
    if (from > to) {
        var swap = from;
        from = to;
        to = swap;
    }
    var units = _taskUnitCatalog.filter(function(u) {
        return u.module_type === _taskLibraryModule;
    }).sort(function(a, b) {
        return (a.unit_no || 0) - (b.unit_no || 0);
    });
    var added = 0;
    var skipped = 0;
    for (var n = from; n <= to; n++) {
        var u = units.find(function(x) { return x.unit_no === n; });
        if (!u) continue;
        if (_taskDraftItems.some(function(it) {
            return it.item_type === 'study' && it.unit_id === u.unit_id && it.status !== 'removed';
        })) {
            skipped++;
            continue;
        }
        var row = {
            item_type: 'study',
            unit_id: u.unit_id,
            module_type: u.module_type,
            unit_title: u.title,
            status: 'pending'
        };
        var at = findDraftInsertIndexForUnit(u);
        _taskDraftItems.splice(at, 0, row);
        added++;
    }
    if (!added) {
        showToast(skipped ? '所选单元已在计划中' : '未找到对应序号的单元', 'error');
        return;
    }
    expandTaskPlanModule(_taskLibraryModule);
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    renderTaskUnitLibrary();
    scrollTaskPlanSegmentIntoView(_taskLibraryModule);
    showToast(
        '已加入 ' + added + ' 个单元' + (skipped ? ('，跳过 ' + skipped + ' 个已排') : ''),
        'success'
    );
    schedulePackPreviewRefresh();
}

function renderTaskUnitLibraryToolbar(moduleTypes) {
    var bar = document.getElementById('taskUnitLibraryToolbar');
    if (!bar) return;
    if (!_taskLibraryModule && moduleTypes.length) {
        _taskLibraryModule = moduleTypes[0];
    }
    if (_taskLibraryModule && moduleTypes.indexOf(_taskLibraryModule) === -1) {
        _taskLibraryModule = moduleTypes[0] || '';
    }
    var moduleUnits = _taskUnitCatalog.filter(function(u) {
        return u.module_type === _taskLibraryModule;
    });
    var maxNo = moduleUnits.reduce(function(m, u) {
        return Math.max(m, u.unit_no || 0);
    }, 0);
    var html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;">';
    html += '<span style="font-size:12px;color:#64748b;align-self:center;width:100%;">科目 ' +
        moduleTypes.length + ' · 单元 ' + (_taskUnitCatalog || []).length + '</span>';
    moduleTypes.forEach(function(mt) {
        var active = mt === _taskLibraryModule;
        var count = _taskUnitCatalog.filter(function(u) { return u.module_type === mt; }).length;
        html += '<button type="button" class="btn ' + (active ? '' : 'btn-secondary') + '" ' +
            'style="padding:4px 10px;font-size:12px;" onclick="selectTaskLibraryModule(\'' + mt + '\')">' +
            taskLibraryModuleLabel(mt) + ' (' + count + ')</button>';
    });
    html += '</div>';
    html += '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px;">';
    html += '<input type="search" id="taskUnitSearchInput" placeholder="搜索单元…" value="' +
        escapeTeacherAttr(_taskLibrarySearch) + '" style="flex:1;min-width:140px;padding:6px 8px;border:1px solid #e5e7eb;border-radius:6px;" ' +
        'oninput="onTaskUnitSearchInput(this.value)">';
    if (maxNo > 1) {
        html += '<span style="font-size:12px;color:#64748b;white-space:nowrap;">序号</span>';
        html += '<input type="number" id="taskUnitBatchFrom" min="1" max="' + maxNo + '" style="width:52px;padding:4px;" value="1">';
        html += '<span style="font-size:12px;color:#64748b;">—</span>';
        html += '<input type="number" id="taskUnitBatchTo" min="1" max="' + maxNo + '" style="width:52px;padding:4px;" value="' + Math.min(6, maxNo) + '">';
        html += '<button type="button" class="btn btn-secondary" style="padding:4px 8px;font-size:12px;" onclick="batchAddTaskUnits()">批量加入</button>';
    }
    html += '</div>';
    bar.innerHTML = html;
}

function taskFormatLocalYmd(d) {
    d = d || new Date();
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
}

function taskDefaultEffectiveYmd() {
    var d = new Date();
    d.setDate(d.getDate() + 1);
    return taskFormatLocalYmd(d);
}

function taskEffectiveLabel(ymd) {
    if (!ymd) return '明天';
    var today = taskFormatLocalYmd(new Date());
    var tom = taskDefaultEffectiveYmd();
    if (ymd === today) return '今天';
    if (ymd === tom) return '明天';
    return ymd;
}

function readTaskEffectiveFromInput() {
    var el = document.getElementById('taskEffectiveFrom');
    if (!el || !el.value) return taskDefaultEffectiveYmd();
    return el.value;
}

function setTaskEffectiveFromInput(ymd) {
    var el = document.getElementById('taskEffectiveFrom');
    if (!el) return;
    el.min = taskFormatLocalYmd(new Date());
    el.value = ymd || taskDefaultEffectiveYmd();
}

function updateTaskPlanSectionTitles(data) {
    var hasDbDraft = !!(data && (data.draft_pending || (data.draft && data.draft.length)));
    var effLabel = taskEffectiveLabel(
        (data && (data.pending_effective_from || data.draft_effective_from)) ||
            readTaskEffectiveFromInput()
    );
    var draftListTitle = document.getElementById('taskDraftListTitle');
    if (draftListTitle) {
        draftListTitle.textContent = hasDbDraft
            ? ('有序清单（待生效草稿，' + effLabel + ' 起替换左侧）')
            : '有序清单（编辑区，与左侧同步；改完后选生效日期保存）';
    }
    var packDraftTitle = document.getElementById('taskPackPreviewDraftTitle');
    if (packDraftTitle) {
        packDraftTitle.textContent = hasDbDraft
            ? ('待生效草稿装箱预览（' + effLabel + '）')
            : '编辑装箱预览（按右侧清单试算，保存后才生效）';
    }
}

async function initTeacherTaskPlanTab() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel) return;
    if (!_teacherStudents || !_teacherStudents.length) {
        try {
            var r = await teacherApiGet('/api/teacher/students');
            _teacherStudents = (r && r.data) || [];
        } catch (e) {
            _teacherStudents = [];
        }
    }
    var students = (_teacherStudents || []).filter(function(s) {
        return !s.status || s.status === 'active';
    });
    var prev = sel.value;
    sel.innerHTML = students.map(function(s) {
        return '<option value="' + s.student_id + '">' + s.student_id + ' ' + (s.name || '') + '</option>';
    }).join('');
    if (prev && students.some(function(s) { return s.student_id === prev; })) {
        sel.value = prev;
    }
    var unitsRes = await teacherApiGet('/api/task/units');
    _taskUnitCatalog = (unitsRes && unitsRes.data) || [];
    renderTaskUnitLibrary();
    bindTaskDurationPreviewInputs();
    bindTaskScheduleModeInputs();
    renderTaskOverviewFilterChips();
    if (_taskPlanSubtab === 'plan') {
        switchTaskPlanSubtab('plan');
        await loadTeacherTaskPlan();
    } else {
        switchTaskPlanSubtab('overview');
        await loadTaskClassOverview();
    }
}

function switchTaskPlanSubtab(which) {
    _taskPlanSubtab = which === 'plan' ? 'plan' : 'overview';
    var ov = document.getElementById('taskClassOverviewPane');
    var pl = document.getElementById('taskStudentPlanPane');
    var bOv = document.getElementById('taskSubtabOverviewBtn');
    var bPl = document.getElementById('taskSubtabPlanBtn');
    if (ov) ov.style.display = _taskPlanSubtab === 'overview' ? 'block' : 'none';
    if (pl) pl.style.display = _taskPlanSubtab === 'plan' ? 'block' : 'none';
    if (bOv) bOv.classList.toggle('active', _taskPlanSubtab === 'overview');
    if (bPl) bPl.classList.toggle('active', _taskPlanSubtab === 'plan');
    if (_taskPlanSubtab === 'overview') {
        renderTaskOverviewFilterChips();
        if (!_taskOverviewData) loadTaskClassOverview();
        else renderTaskClassOverview();
    }
}

async function openStudentPlanFromOverview(studentId) {
    if (!studentId) return;
    var sel = document.getElementById('taskPlanStudentSelect');
    if (sel) sel.value = studentId;
    switchTaskPlanSubtab('plan');
    await loadTeacherTaskPlan();
}

function renderTaskOverviewFilterChips() {
    var box = document.getElementById('taskOverviewFilters');
    if (!box) return;
    var chips = [
        { key: null, label: '全部学生' },
        { key: 'paused', label: '计划暂停' },
        { key: 'yesterdayIncomplete', label: '昨日未完成' },
        { key: 'incomplete', label: '今日未完成' },
        { key: 'backlog', label: '有积压' },
        { key: 'attention', label: '需关注' },
        { key: 'noPlan', label: '无计划' }
    ];
    var anyFilter = Object.keys(_taskOverviewFilters).some(function(k) {
        return !!_taskOverviewFilters[k];
    });
    box.innerHTML = chips.map(function(c) {
        var on = c.key ? !!_taskOverviewFilters[c.key] : !anyFilter;
        return '<button type="button" class="btn btn-secondary" style="padding:3px 8px;font-size:12px;' +
            (on ? 'background:#e0f2fe;border-color:#7dd3fc;' : '') + '" ' +
            'onclick="toggleTaskOverviewFilter(' + (c.key ? ("'" + c.key + "'") : 'null') + ')">' +
            c.label + '</button>';
    }).join('');
}

function toggleTaskOverviewFilter(key) {
    if (!key) {
        Object.keys(_taskOverviewFilters).forEach(function(k) {
            _taskOverviewFilters[k] = false;
        });
    } else {
        _taskOverviewFilters[key] = !_taskOverviewFilters[key];
    }
    renderTaskOverviewFilterChips();
    renderTaskClassOverview();
}

async function loadTaskClassOverview() {
    var wrap = document.getElementById('taskOverviewTableWrap');
    var stats = document.getElementById('taskOverviewStats');
    if (wrap) wrap.innerHTML = '<div style="padding:12px;color:#94a3b8;">加载中…</div>';
    var res = await teacherApiGet('/api/task/class-overview');
    if (res.error) {
        if (wrap) {
            wrap.innerHTML = '<div style="padding:12px;color:#b45309;">加载失败：' +
                escapeTeacherAttr((res.error && res.error.message) || '接口不可用') +
                '。请重启本地服务后刷新。</div>';
        }
        return;
    }
    _taskOverviewData = res.data || {};
    renderTaskClassOverview();
    if (stats && _taskOverviewData.generated_at) {
        /* stats filled in render */
    }
}

function filterTaskOverviewRows(rows) {
    var q = ((document.getElementById('taskOverviewSearch') || {}).value || '').trim().toLowerCase();
    return (rows || []).filter(function(r) {
        if (q) {
            var blob = (r.student_id + ' ' + (r.name || '')).toLowerCase();
            if (blob.indexOf(q) < 0) return false;
        }
        if (_taskOverviewFilters.paused) {
            var pp = r.plan_pause || {};
            if (!(pp.active || pp.upcoming)) return false;
        }
        if (_taskOverviewFilters.incomplete) {
            if (!(r.today_total > 0 && r.today_done < r.today_total)) return false;
        }
        if (_taskOverviewFilters.yesterdayIncomplete) {
            if (!r.yesterday_incomplete) return false;
        }
        if (_taskOverviewFilters.backlog && !(r.backlog > 0)) return false;
        if (_taskOverviewFilters.attention && r.row_status !== 'red') return false;
        if (_taskOverviewFilters.noPlan && r.plan_status !== 'none') return false;
        return true;
    });
}

function taskOverviewStatusEmoji(st) {
    if (st === 'red') return '🔴';
    if (st === 'yellow') return '🟡';
    if (st === 'green') return '🟢';
    return '⚪';
}

function taskOverviewRowBg(st) {
    if (st === 'red') return 'background:#fff5f5;';
    if (st === 'yellow') return 'background:#fffbeb;';
    if (st === 'green') return '';
    return '';
}

/** Minutes → "15h 48m" / "45m" / "0m" (no Chinese). */
function formatMinutesHm(mins) {
    mins = Math.max(0, Math.floor(Number(mins) || 0));
    var h = Math.floor(mins / 60);
    var m = mins % 60;
    if (h > 0 && m > 0) return h + 'h ' + m + 'm';
    if (h > 0) return h + 'h';
    return m + 'm';
}

function renderTaskClassOverview() {
    var wrap = document.getElementById('taskOverviewTableWrap');
    var statsEl = document.getElementById('taskOverviewStats');
    if (!wrap) return;
    var data = _taskOverviewData || {};
    var all = data.students || [];
    var rows = filterTaskOverviewRows(all);
    rows.sort(function(a, b) {
        return String(b.student_id || '').localeCompare(String(a.student_id || ''), 'en');
    });
    var st = data.stats || {};
    if (statsEl) {
        statsEl.textContent = '共 ' + (st.total != null ? st.total : all.length) +
            ' 人 · 计划暂停 ' + (st.plan_paused || 0) +
            ' · 昨日未完成 ' + (st.yesterday_incomplete || 0) +
            ' · 今日已全完成 ' + (st.today_all_done || 0) +
            ' · 需关注 ' + (st.need_attention || 0) +
            ' · 无计划 ' + (st.no_plan || 0) +
            (data.generated_at ? (' · 更新 ' + data.generated_at) : '') +
            (rows.length !== all.length ? (' · 筛选后 ' + rows.length) : '');
    }
    if (!all.length) {
        wrap.innerHTML = '<div style="padding:16px;color:#64748b;">暂无在读学生</div>';
        return;
    }
    if (!rows.length) {
        wrap.innerHTML = '<div style="padding:16px;color:#64748b;">无匹配学生</div>';
        return;
    }
    var html = '<table style="width:100%;border-collapse:collapse;font-size:13px;min-width:720px;">' +
        '<thead><tr style="background:#f8fafc;text-align:left;">' +
        '<th style="padding:8px 6px;">状态</th>' +
        '<th style="padding:8px 6px;">学号</th>' +
        '<th style="padding:8px 6px;">姓名</th>' +
        '<th style="padding:8px 6px;">昨日任务</th>' +
        '<th style="padding:8px 6px;">昨日学习时长</th>' +
        '<th style="padding:8px 6px;">积压</th>' +
        '<th style="padding:8px 6px;">计划进度</th>' +
        '</tr></thead><tbody>';
    rows.forEach(function(r) {
        var sid = escapeTeacherAttr(r.student_id);
        var yCell;
        if (!(r.yesterday_total > 0)) {
            yCell = '<span style="color:#94a3b8;">— 无任务</span>';
        } else {
            var yPct = Math.round((r.yesterday_done / r.yesterday_total) * 100);
            var yDanger = r.yesterday_incomplete ? 'color:#dc2626;font-weight:600;' : '';
            yCell = '<span style="' + yDanger + '">' + r.yesterday_done + '/' + r.yesterday_total +
                ' · ' + yPct + '%</span>';
        }
        var brief = (r.plan_progress_brief || []).map(function(b) {
            return b.text || '';
        }).join(' · ');
        if (r.plan_status === 'none') brief = '未排计划';
        else if ((r.plan_pause || {}).active) {
            brief = '⏸ 暂停至 ' + (r.plan_pause.resume_on || '') +
                ' · ' + (r.plan_pause.reason || '');
        } else if ((r.plan_pause || {}).upcoming) {
            brief = '⏸ 将于 ' + (r.plan_pause.pause_from || '') + ' 暂停 · ' +
                (r.plan_pause.reason || '');
        } else if (r.plan_status === 'all_paused') brief = '计划已暂停';
        else if (!brief) brief = '—';
        var pendingTag = r.pending_plan_change
            ? (' <span style="color:#b45309;font-size:11px;">明生效</span>')
            : '';
        if ((r.plan_pause || {}).active || (r.plan_pause || {}).upcoming) {
            pendingTag += ' <span style="color:#b45309;font-size:11px;">暂停</span>';
        }
        var yMins = Number(r.yesterday_minutes) || 0;
        var tMins = Number(r.total_minutes) || 0;
        var timeCell = (yMins > 0 || tMins > 0)
            ? (formatMinutesHm(yMins) + ' / ' + formatMinutesHm(tMins))
            : '—';
        html += '<tr style="border-top:1px solid #f1f5f9;cursor:pointer;' +
            taskOverviewRowBg(r.row_status) + '" ' +
            'onclick="openStudentPlanFromOverview(\'' + sid.replace(/'/g, "\\'") + '\')">' +
            '<td style="padding:8px 6px;">' + taskOverviewStatusEmoji(r.row_status) + '</td>' +
            '<td style="padding:8px 6px;">' + sid + '</td>' +
            '<td style="padding:8px 6px;">' + escapeTeacherAttr(r.name || '') + pendingTag + '</td>' +
            '<td style="padding:8px 6px;">' + yCell + '</td>' +
            '<td style="padding:8px 6px;" title="昨日时长 / 累计总时长">' + timeCell + '</td>' +
            '<td style="padding:8px 6px;' + (r.backlog >= 3 ? 'color:#dc2626;font-weight:600;' : '') + '">' +
            (r.backlog > 0 ? r.backlog : '—') + '</td>' +
            '<td style="padding:8px 6px;">' + escapeTeacherAttr(brief) + '</td>' +
            '</tr>';
    });
    html += '</tbody></table>';
    wrap.innerHTML = html;
}

function renderTaskPlanList() {
    var box = document.getElementById('taskPlanList');
    if (!box) return;
    if (!_taskDraftItems.length) {
        box.innerHTML = '<p style="color:#666;margin:0;">从左侧加入单元</p>';
        if (readTaskPackMode() === 'units_per_day') renderTaskModuleQuotaTable();
        return;
    }
    var issues = _taskDraftOrderIssues(_taskDraftItems);
    var html = '';
    if (issues.length) {
        html += '<div style="background:#fef2f2;border:1px solid #fecaca;color:#b91c1c;padding:8px;border-radius:8px;margin-bottom:8px;font-size:13px;position:sticky;top:0;z-index:3;">';
        html += '<strong>顺序问题：</strong>' + issues.join('；') +
            '。可点「修正测验顺序」或保存清单时自动修正。</div>';
    }
    var segments = groupTaskItemsByModuleSegments(_taskDraftItems);
    segments.forEach(function(seg) {
        var mt = seg.moduleType;
        var pendingStudy = 0;
        var doneStudy = 0;
        var testN = 0;
        var testPassed = 0;
        seg.indices.forEach(function(i) {
            var it = _taskDraftItems[i];
            if (it.item_type === 'test') {
                testN++;
                if (isTaskItemDone(it)) testPassed++;
            } else if (isTaskItemDone(it)) {
                doneStudy++;
            } else {
                pendingStudy++;
            }
        });
        var collapsed = isTaskSectionCollapsed(mt, _taskPlanCollapse);
        var showDone = !!_taskPlanShowCompleted[mt];
        var arrow = collapsed ? '▶' : '▼';
        var safeMt = String(mt).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        var summary = escapeTeacherAttr(taskModuleShortLabel(mt)) +
            ' · 待学 ' + pendingStudy + ' · 已完成 ' + doneStudy +
            ' · 测 ' + testN + (testN ? ('（过关 ' + testPassed + '）') : '');
        html += '<div id="taskPlanSeg_' + escapeTeacherAttr(mt) +
            '" style="position:sticky;top:' + (issues.length ? '42px' : '0') +
            ';z-index:2;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;margin:6px 0 4px;padding:6px 8px;">';
        html += '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;">';
        html += '<button type="button" class="btn btn-secondary" style="padding:4px 10px;font-size:13px;font-weight:600;" ' +
            'onclick="toggleTaskPlanSection(\'' + safeMt + '\')">' + arrow + ' ' + summary + '</button>';
        html += '<span style="display:flex;gap:4px;flex-shrink:0;">';
        if (doneStudy + testPassed > 0) {
            html += '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:11px;" ' +
                'onclick="toggleTaskPlanShowCompleted(\'' + safeMt + '\')">' +
                (showDone ? '收起已完成' : ('展开已完成 ' + (doneStudy + testPassed))) + '</button>';
        }
        html += '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:11px;" ' +
            'onclick="insertStageTestForModuleSegment(\'' + safeMt + '\')" title="对本科目当前最后一段插入阶段测">本段测至末</button>';
        html += '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:11px;" ' +
            'onclick="removeTaskDraftModuleSegment(\'' + safeMt + '\')">移除本段</button>';
        html += '</span></div></div>';
        if (collapsed) return;
        var displayIdx = orderSegmentIndicesForDisplay(_taskDraftItems, seg.indices, showDone);
        displayIdx.forEach(function(idx) {
            var it = _taskDraftItems[idx];
            var done = isTaskItemDone(it);
            var bad = issues.some(function(msg) { return msg.indexOf('第' + (idx + 1) + '条') === 0; });
            var menuOpen = _taskPlanOpenMenuIdx === idx;
            var rowBg = bad ? 'background:#fff7ed;' : (done ? 'background:#f8fafc;' : '');
            var dim = done ? 'color:#94a3b8;' : '';
            html += '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;padding:5px 6px;border-bottom:1px solid #f1f5f9;' +
                rowBg + dim + '">';
            html += '<span style="font-size:13px;line-height:1.4;">' + (idx + 1) + '. ' +
                formatTaskPlanItemBody(it) + '</span>';
            html += '<span style="position:relative;flex-shrink:0;">';
            html += '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:12px;" ' +
                'onclick="toggleTaskRowMenu(' + idx + ')" title="操作">⋯</button>';
            if (menuOpen) {
                html += '<div style="position:absolute;right:0;top:100%;z-index:5;background:#fff;border:1px solid #e2e8f0;' +
                    'border-radius:8px;box-shadow:0 4px 12px rgba(15,23,42,0.12);padding:6px;min-width:110px;display:flex;flex-direction:column;gap:4px;color:#334155;">';
                if (it.item_type === 'study' && it.unit_id) {
                    html += '<button type="button" class="btn btn-secondary" style="padding:4px 8px;font-size:12px;text-align:left;" ' +
                        'onclick="insertStageTestThrough(' + idx + ')">测至此处</button>';
                }
                if (idx > 0) {
                    html += '<button type="button" class="btn btn-secondary" style="padding:4px 8px;font-size:12px;text-align:left;" ' +
                        'onclick="moveTaskDraft(' + idx + ',-1)">上移</button>';
                }
                if (idx < _taskDraftItems.length - 1) {
                    html += '<button type="button" class="btn btn-secondary" style="padding:4px 8px;font-size:12px;text-align:left;" ' +
                        'onclick="moveTaskDraft(' + idx + ',1)">下移</button>';
                }
                html += '<button type="button" class="btn btn-secondary" style="padding:4px 8px;font-size:12px;text-align:left;" ' +
                    'onclick="removeTaskDraft(' + idx + ')">移除</button>';
                html += '</div>';
            }
            html += '</span></div>';
        });
        if (!showDone && (doneStudy + testPassed) > 0) {
            html += '<div style="padding:4px 8px;font-size:12px;color:#94a3b8;">已收起 ' +
                (doneStudy + testPassed) + ' 条已完成 · 点上方「展开已完成」查看</div>';
        }
    });
    box.innerHTML = html;
    if (readTaskPackMode() === 'units_per_day') renderTaskModuleQuotaTable();
}

function _taskDraftOrderIssues(items) {
    var issues = [];
    var studySeen = {};
    (items || []).forEach(function(it, idx) {
        if (it.item_type === 'study' && it.unit_id) {
            studySeen[it.unit_id] = true;
        } else if (it.item_type === 'test') {
            var covers = normalizeTestUnitIds(it.test_unit_ids);
            var missing = covers.filter(function(uid) { return !studySeen[uid]; });
            if (missing.length) {
                var mod = taskModuleShortLabel(inferTaskItemModuleType(it, items));
                issues.push('第' + (idx + 1) + '条「' + mod + ' · ' + (it.test_title || '阶段测') +
                    '」排在部分学习单元之前');
            }
        }
    });
    return issues;
}

function normalizeStageTestOrderClient(items) {
    var out = items.filter(function(it) { return it.item_type !== 'test'; }).map(function(it) {
        return Object.assign({}, it, {
            test_unit_ids: normalizeTestUnitIds(it.test_unit_ids)
        });
    });
    var tests = items.filter(function(it) { return it.item_type === 'test'; });
    var seen = {};
    var uniqueTests = [];
    tests.forEach(function(test) {
        var coverIds = normalizeTestUnitIds(test.test_unit_ids);
        var covers = coverIds.slice().sort().join('\u0001');
        if (!covers || seen[covers]) return;
        seen[covers] = true;
        var mt = test.module_type || inferTaskItemModuleType(
            { item_type: 'test', test_unit_ids: coverIds }, out
        );
        uniqueTests.push(Object.assign({}, test, {
            test_unit_ids: coverIds,
            module_type: mt || test.module_type || ''
        }));
    });
    var keyed = uniqueTests.map(function(test) {
        var coverSet = {};
        (test.test_unit_ids || []).forEach(function(u) { coverSet[u] = true; });
        var indices = [];
        out.forEach(function(st, i) {
            if (st.item_type === 'study' && st.unit_id && coverSet[st.unit_id]) indices.push(i);
        });
        if (!indices.length) return { last: out.length, first: 0, n: 0, test: test };
        return {
            last: Math.max.apply(null, indices),
            first: Math.min.apply(null, indices),
            n: (test.test_unit_ids || []).length,
            test: test
        };
    });
    keyed.sort(function(a, b) {
        if (a.last !== b.last) return a.last - b.last;
        if (a.first !== b.first) return a.first - b.first;
        return a.n - b.n;
    });
    for (var ki = keyed.length - 1; ki >= 0; ki--) {
        out.splice(keyed[ki].last + 1, 0, keyed[ki].test);
    }
    return out;
}

function draftItemUnitNo(it) {
    if (!it || it.item_type !== 'study' || !it.unit_id) return null;
    var u = (_taskUnitCatalog || []).find(function(x) { return x.unit_id === it.unit_id; });
    if (u && u.unit_no != null && u.unit_no !== '') return Number(u.unit_no) || 0;
    var m = /_u(\d+)$/i.exec(String(it.unit_id));
    return m ? Number(m[1]) : 0;
}

function regroupDraftItemsByModule(items) {
    // 按科目首次出现顺序归拢；同科学生成按组号/单元号排序。装箱时再多科轮换。
    var order = [];
    var buckets = {};
    (items || []).forEach(function(it) {
        var mt = inferTaskItemModuleType(it, items) || '_none';
        if (!buckets[mt]) {
            buckets[mt] = [];
            order.push(mt);
        }
        buckets[mt].push(it);
    });
    var out = [];
    order.forEach(function(mt) {
        var bucket = buckets[mt];
        var studies = bucket.filter(function(it) { return it.item_type === 'study'; });
        var tests = bucket.filter(function(it) { return it.item_type !== 'study'; });
        studies.sort(function(a, b) {
            return (draftItemUnitNo(a) || 0) - (draftItemUnitNo(b) || 0);
        });
        out = out.concat(studies).concat(tests);
    });
    return out;
}

function fixStageTestOrderDraft() {
    if (!_taskDraftItems.length) return;
    _taskDraftItems = normalizeStageTestOrderClient(
        regroupDraftItemsByModule(_taskDraftItems)
    );
    // 修正后默认今天生效，避免只改了右侧、左侧「当前生效」一直不动
    setTaskEffectiveFromInput(taskFormatLocalYmd(new Date()));
    renderTaskPlanList();
    showToast('有序清单已重排；生效日已设为今天，请点「保存清单草稿」以更新左侧当前生效清单', 'success');
    schedulePackPreviewRefresh();
}

async function loadTaskPackPreviews(studentId) {
    if (!studentId) return;
    var packMode = readTaskPackMode();
    // 先记住表单配额，再刷新 UI，避免重绘把刚改的数字盖回旧值
    rememberTaskModuleQuotasFromForm();
    toggleTaskScheduleModeUI();

    var draftPayload = {
        pack_mode: packMode,
        items: (_taskDraftItems || []).map(function(it) {
            return {
                item_type: it.item_type,
                unit_id: it.unit_id || null,
                module_type: it.module_type,
                test_unit_ids: it.test_unit_ids || [],
                test_title: it.test_title || '',
                est_minutes: it.est_minutes,
                status: it.status || 'pending'
            };
        })
    };

    if (packMode === 'units_per_day') {
        var schedBox = document.getElementById('taskUnitsSchedule');
        var schedTitle = document.getElementById('taskUnitsScheduleTitle');
        if (!schedBox) return;
        schedBox.innerHTML = '<span style="color:#94a3b8;">加载中…</span>';
        draftPayload.module_quotas = collectTaskModuleQuotasPayload();
        if (!draftPayload.module_quotas.length) {
            draftPayload.module_quotas = Object.keys(_taskModuleQuotas || {}).map(function(mt) {
                return {
                    module_type: mt,
                    weekday_units: _taskModuleQuotas[mt].weekday_units,
                    weekend_units: _taskModuleQuotas[mt].weekend_units
                };
            });
        }
        var effInput = readTaskEffectiveFromInput();
        if (effInput) draftPayload.effective_from = effInput;
        var unitsRes = await teacherApiPost(
            '/api/task/students/' + encodeURIComponent(studentId) + '/pack-preview',
            draftPayload
        );
        if (unitsRes.error) {
            schedBox.innerHTML = '<span style="color:#b45309;">排程预览失败：' +
                escapeTeacherAttr((unitsRes.error && unitsRes.error.message) || '接口不可用') +
                '。请重启本地服务后刷新。</span>';
            return;
        }
        if (schedTitle) {
            schedTitle.textContent = _taskHasDbDraft
                ? ('每日任务排程（与学生对齐；待生效草稿试算，' + (_taskPendingEffectiveLabel || '') + '）')
                : '每日任务排程（与学生端对齐；周末条数按生效日配额，未到生效日仍用旧配额）';
        }
        schedBox.innerHTML = renderUnitsScheduleHtml(unitsRes.data);
        return;
    }

    var liveBox = document.getElementById('taskPackPreviewLive');
    var draftBox = document.getElementById('taskPackPreviewDraft');
    if (!liveBox || !draftBox) return;
    liveBox.innerHTML = '<span style="color:#94a3b8;">加载中…</span>';
    draftBox.innerHTML = '<span style="color:#94a3b8;">加载中…</span>';

    var liveRes = await teacherApiGet(
        '/api/task/students/' + encodeURIComponent(studentId) + '/pack-preview?source=live'
    );
    if (liveRes.error) {
        liveBox.innerHTML = '<span style="color:#b45309;">今日预览加载失败：' +
            escapeTeacherAttr((liveRes.error && liveRes.error.message) || '接口不可用') +
            '。若刚更新代码，请<strong>重启本地服务</strong>后刷新。</span>';
    } else {
        liveBox.innerHTML = renderPackPreviewHtml(liveRes.data, '今日');
    }

    var formWd = Number(document.getElementById('taskWeekdayMinutes') && document.getElementById('taskWeekdayMinutes').value);
    var formWe = Number(document.getElementById('taskWeekendMinutes') && document.getElementById('taskWeekendMinutes').value);
    if (!isNaN(formWd) && formWd > 0) draftPayload.weekday_minutes = formWd;
    if (!isNaN(formWe) && formWe > 0) draftPayload.weekend_minutes = formWe;
    var draftRes = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(studentId) + '/pack-preview',
        draftPayload
    );
    if (draftRes.error) {
        draftBox.innerHTML = '<span style="color:#b45309;">编辑预览失败：' +
            escapeTeacherAttr((draftRes.error && draftRes.error.message) || '接口不可用') +
            '。请重启本地服务后刷新。</span>';
        return;
    }
    var draftLabel = _taskHasDbDraft
        ? _taskPendingEffectiveLabel
        : ('保存·' + taskEffectiveLabel(readTaskEffectiveFromInput()));
    var draftHtml = renderPackPreviewHtml(draftRes.data, draftLabel);
    if (draftRes.data && draftRes.data.source === 'draft_items') {
        draftHtml = '<div style="color:#64748b;font-size:12px;margin-bottom:6px;">' +
            (_taskHasDbDraft
                ? '按待生效草稿 + 上方时长输入试算'
                : '按右侧清单与上方时长输入实时试算（改分钟后无需先保存）') +
            '</div>' + draftHtml;
    }
    var liveBudget = liveRes && liveRes.data ? Number(liveRes.data.budget_minutes) : NaN;
    if (!isNaN(formWd) && !isNaN(liveBudget) && formWd !== liveBudget) {
        draftHtml = '<div style="color:#b45309;font-size:12px;margin-bottom:6px;">' +
            '上方周中 ' + formWd + '′ 尚未成为「今日实际」预算（当前生效 ' + liveBudget +
            '′）。点「保存排程设置」且生效日为今天后，上方预览会同步。</div>' + draftHtml;
    }
    draftBox.innerHTML = draftHtml;
}

var _packPreviewTimer = null;
function schedulePackPreviewRefresh() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    if (_packPreviewTimer) clearTimeout(_packPreviewTimer);
    _packPreviewTimer = setTimeout(function() {
        loadTaskPackPreviews(sel.value);
    }, 350);
}

function readTaskPackMode() {
    return 'units_per_day';
}

function setTaskPackMode(mode) {
    toggleTaskScheduleModeUI();
}

function toggleTaskScheduleModeUI() {
    var quotaPanel = document.getElementById('taskModuleQuotaPanel');
    var timePack = document.getElementById('taskTimePackPreviewBlock');
    var unitsSched = document.getElementById('taskUnitsScheduleBlock');
    if (quotaPanel) quotaPanel.style.display = 'block';
    if (timePack) timePack.style.display = 'none';
    if (unitsSched) unitsSched.style.display = 'block';
    rememberTaskModuleQuotasFromForm();
    renderTaskModuleQuotaTable();
}

function rememberTaskModuleQuotasFromForm() {
    collectTaskModuleQuotasPayload().forEach(function(q) {
        if (!_taskModuleQuotas) _taskModuleQuotas = {};
        _taskModuleQuotas[q.module_type] = {
            weekday_units: q.weekday_units,
            weekend_units: q.weekend_units
        };
    });
}

function collectModulesInDraft() {
    var order = [];
    var seen = {};
    (_taskDraftItems || []).forEach(function(it) {
        var mt = inferTaskItemModuleType(it, _taskDraftItems) || it.module_type;
        if (!mt || seen[mt]) return;
        seen[mt] = true;
        order.push(mt);
    });
    return order;
}

function syncTaskModuleQuotasFromProfile(tp) {
    _taskModuleQuotas = {};
    (tp && tp.module_quotas || []).forEach(function(q) {
        if (!q.module_type) return;
        _taskModuleQuotas[q.module_type] = {
            weekday_units: q.pending_weekday_units != null ? q.pending_weekday_units :
                (q.weekday_units != null ? q.weekday_units : 1),
            weekend_units: q.pending_weekend_units != null ? q.pending_weekend_units :
                (q.weekend_units != null ? q.weekend_units : 1)
        };
    });
}

function renderTaskModuleQuotaTable() {
    var panel = document.getElementById('taskModuleQuotaPanel');
    if (!panel) return;
    var modules = collectModulesInDraft();
    if (!modules.length) {
        panel.innerHTML = '<span style="color:#64748b;font-size:13px;">请先在右侧清单加入科目单元</span>';
        return;
    }
    rememberTaskModuleQuotasFromForm();
    var quotas = _taskModuleQuotas || {};
    var html = '<table style="width:100%;max-width:520px;border-collapse:collapse;font-size:13px;">' +
        '<thead><tr><th style="text-align:left;padding:4px 8px;">科目</th>' +
        '<th style="padding:4px 8px;">周中每天</th><th style="padding:4px 8px;">周末每天</th></tr></thead><tbody>';
    modules.forEach(function(mt) {
        var q = quotas[mt] || {};
        var mod = (typeof getModuleById === 'function') ? getModuleById(mt) : null;
        var name = (mod && mod.name) || mt;
        html += '<tr><td style="padding:4px 8px;">' + escapeTeacherAttr(name) + '</td>' +
            '<td style="padding:4px 8px;text-align:center;"><input type="number" class="taskQuotaWd" data-module="' +
            escapeTeacherAttr(mt) + '" min="0" max="20" style="width:52px;" value="' +
            (q.weekday_units != null ? q.weekday_units : 1) + '"></td>' +
            '<td style="padding:4px 8px;text-align:center;"><input type="number" class="taskQuotaWe" data-module="' +
            escapeTeacherAttr(mt) + '" min="0" max="20" style="width:52px;" value="' +
            (q.weekend_units != null ? q.weekend_units : 1) + '"></td></tr>';
    });
    html += '</tbody></table>';
    panel.innerHTML = html;
    panel.querySelectorAll('.taskQuotaWd, .taskQuotaWe').forEach(function(el) {
        el.addEventListener('change', function() {
            rememberTaskModuleQuotasFromForm();
            schedulePackPreviewRefresh();
        });
        el.addEventListener('input', function() {
            rememberTaskModuleQuotasFromForm();
            schedulePackPreviewRefresh();
        });
    });
}

function collectTaskModuleQuotasPayload() {
    var out = [];
    document.querySelectorAll('.taskQuotaWd').forEach(function(wdEl) {
        var mt = wdEl.getAttribute('data-module');
        if (!mt) return;
        var weEl = document.querySelector('.taskQuotaWe[data-module="' + mt + '"]');
        out.push({
            module_type: mt,
            weekday_units: Number(wdEl.value) || 0,
            weekend_units: Number((weEl && weEl.value) || 0) || 0
        });
    });
    return out;
}

function bindTaskScheduleModeInputs() {
    /* 仅保留单元排程模式，无需绑定切换控件 */
}

function bindTaskDurationPreviewInputs() {
    ['taskWeekdayMinutes', 'taskWeekendMinutes', 'taskEffectiveFrom'].forEach(function(id) {
        var el = document.getElementById(id);
        if (!el || el._packBound) return;
        el._packBound = true;
        el.addEventListener('change', schedulePackPreviewRefresh);
        el.addEventListener('input', schedulePackPreviewRefresh);
    });
}

function weekdayLabelZh(ymd) {
    if (!ymd) return '';
    var parts = String(ymd).split('-');
    if (parts.length < 3) return '';
    var d = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    if (isNaN(d.getTime())) return '';
    return ['日', '一', '二', '三', '四', '五', '六'][d.getDay()];
}

function renderUnitsDayTasksHtml(items) {
    if (!items || !items.length) {
        return '<div style="color:#94a3b8;padding:2px 0 2px 8px;">无任务</div>';
    }
    var html = '';
    items.forEach(function(it, i) {
        var mod = (typeof getModuleById === 'function') ? getModuleById(it.module_type) : null;
        var modName = (mod && mod.name) || it.module_type || '';
        var prefix = it.item_type === 'test' ? '测' : '学';
        html += '<div style="padding:2px 0 2px 8px;">' + (i + 1) + '. <span style="color:#64748b;">' +
            escapeTeacherAttr(modName) + '</span> ' + prefix + ' · ' +
            escapeTeacherAttr(it.title || '') + '</div>';
    });
    return html;
}

function renderUnitsScheduleHtml(data) {
    var schedule = (data && data.schedule) || [];
    if (!schedule.length && data && data.items && data.items.length) {
        schedule = [{
            task_date: data.task_date || '',
            items: data.items,
            units_total: data.units_total || data.items.length
        }];
    }
    if (!schedule.length) {
        return '<span style="color:#64748b;">暂无排程（请先在下方清单加入单元，并设置每科每天几个）</span>';
    }
    var today = taskFormatLocalYmd(new Date());
    var html = '';
    var shown = 0;
    schedule.forEach(function(day) {
        if (!day || !day.items || !day.items.length) return;
        shown += 1;
        if (shown > 14) return;
        var ymd = day.task_date || '';
        var isToday = ymd === today;
        var wd = weekdayLabelZh(ymd);
        html += '<div style="margin:0 0 10px;padding:8px;border:1px solid ' +
            (isToday ? '#93c5fd' : '#e2e8f0') + ';border-radius:8px;background:' +
            (isToday ? '#eff6ff' : '#f8fafc') + ';">';
        html += '<div style="font-weight:600;margin-bottom:4px;color:#0f172a;">' +
            escapeTeacherAttr(ymd) +
            (wd ? '（周' + wd + '）' : '') +
            (isToday ? ' · 今天' : '') +
            (day.source === 'actual' ? ' · 学生实际' : '') +
            ' <span style="font-weight:400;color:#64748b;">· ' +
            (day.units_total || day.items.length) + ' 条</span></div>';
        html += renderUnitsDayTasksHtml(day.items);
        html += '</div>';
    });
    if (!shown) {
        return '<span style="color:#64748b;">暂无排程（请先在下方清单加入单元，并设置每科每天几个）</span>';
    }
    return html;
}

function renderPackPreviewHtml(data, label) {
    if (!data || !data.items || !data.items.length) {
        return '<span style="color:#64748b;">' + label + '暂无装箱任务（或清单为空）</span>';
    }
    var rot = data.rotated
        ? '<span style="color:#16a34a;margin-left:6px;">多科轮换</span>'
        : '<span style="color:#64748b;margin-left:6px;">单科顺序</span>';
    var locked = data.source === 'live_locked'
        ? '<span style="color:#64748b;margin-left:6px;">（今日已锁定）</span>' : '';
    var html = '<div style="margin-bottom:6px;color:#64748b;">预算 ' + (data.budget_minutes || 0) +
        '′ · 预计放出 ' + (data.est_total_minutes || 0) + '′' + rot + locked + '</div>';
    data.items.forEach(function(it, i) {
        var mod = (typeof getModuleById === 'function') ? getModuleById(it.module_type) : null;
        var modName = (mod && mod.name) || it.module_type || '';
        var prefix = it.item_type === 'test' ? '测' : '学';
        html += '<div style="padding:2px 0;">' + (i + 1) + '. <span style="color:#94a3b8;">' +
            modName + '</span> ' + prefix + ' · ' + (it.title || '') +
            ' <span style="color:#94a3b8;">(' + (it.est_minutes || 0) + '′)</span></div>';
    });
    return html;
}

function getStageTestModuleUnits(moduleType) {
    return _taskDraftItems.filter(function(it) {
        return it.item_type === 'study' && it.unit_id && it.module_type === moduleType;
    });
}

function buildStageTestTitle(unitIds) {
    var titles = unitIds.map(function(uid) {
        var x = _taskDraftItems.find(function(it) { return it.unit_id === uid; });
        return (x && x.unit_title) || uid;
    });
    if (!titles.length) return '阶段测';
    if (titles.length === 1) return titles[0] + ' 阶段测';
    return titles[0] + '–' + titles[titles.length - 1] + ' 阶段测';
}

function insertStageTestForUnits(unitIds) {
    if (!unitIds || !unitIds.length) {
        showToast('请至少选择一个单元', 'error');
        return false;
    }
    var moduleType = null;
    var i;
    for (i = 0; i < unitIds.length; i++) {
        var row = _taskDraftItems.find(function(it) {
            return it.item_type === 'study' && it.unit_id === unitIds[i];
        });
        if (!row) {
            showToast('单元不在清单中', 'error');
            return false;
        }
        if (!moduleType) moduleType = row.module_type;
        else if (row.module_type !== moduleType) {
            showToast('阶段测只能覆盖同一科目', 'error');
            return false;
        }
    }
    var unitSet = {};
    unitIds.forEach(function(uid) { unitSet[uid] = true; });
    for (i = 0; i < _taskDraftItems.length; i++) {
        var testItem = _taskDraftItems[i];
        if (testItem.item_type !== 'test') continue;
        var covers = normalizeTestUnitIds(testItem.test_unit_ids);
        if (covers.length === unitIds.length &&
            covers.every(function(uid) { return unitSet[uid]; })) {
            showToast('已有相同范围的阶段测', 'error');
            return false;
        }
    }
    var lastIdx = -1;
    for (i = 0; i < _taskDraftItems.length; i++) {
        if (_taskDraftItems[i].item_type === 'study' && unitSet[_taskDraftItems[i].unit_id]) {
            lastIdx = i;
        }
    }
    if (lastIdx < 0) {
        showToast('未找到对应学习单元', 'error');
        return false;
    }
    var testTitle = buildStageTestTitle(unitIds);
    _taskDraftItems.splice(lastIdx + 1, 0, {
        item_type: 'test',
        unit_id: null,
        module_type: moduleType,
        test_unit_ids: unitIds.slice(),
        test_title: testTitle,
        est_minutes: 20,
        status: 'pending'
    });
    _taskDraftItems = normalizeStageTestOrderClient(_taskDraftItems);
    expandTaskPlanModule(moduleType);
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    scrollTaskPlanSegmentIntoView(moduleType);
    schedulePackPreviewRefresh();
    return true;
}

function insertStageTestThrough(draftIdx) {
    var anchor = _taskDraftItems[draftIdx];
    if (!anchor || anchor.item_type !== 'study' || !anchor.unit_id) return;
    var moduleType = anchor.module_type;
    // 只覆盖「当前段」：上一同科目阶段测之后（或上一其他科目之后）到本单元。
    // 这样最后加的第二组也能单独插测，并被「修正测验顺序」正确归位。
    var startIdx = 0;
    var i;
    for (i = draftIdx - 1; i >= 0; i--) {
        var prev = _taskDraftItems[i];
        if (prev.item_type === 'test' &&
            (prev.module_type === moduleType ||
                inferTaskItemModuleType(prev, _taskDraftItems) === moduleType)) {
            startIdx = i + 1;
            break;
        }
        if (prev.item_type === 'study' && prev.module_type && prev.module_type !== moduleType) {
            startIdx = i + 1;
            break;
        }
    }
    var unitIds = [];
    for (i = startIdx; i <= draftIdx; i++) {
        var it = _taskDraftItems[i];
        if (it.item_type === 'study' && it.module_type === moduleType && it.unit_id) {
            unitIds.push(it.unit_id);
        }
    }
    if (insertStageTestForUnits(unitIds)) {
        showToast('已插入阶段测（本段 ' + unitIds.length + ' 个单元，至第 ' + (draftIdx + 1) + ' 项）', 'success');
    }
}

function openStageTestModal() {
    var studies = _taskDraftItems.filter(function(it) {
        return it.item_type === 'study' && it.unit_id;
    });
    if (!studies.length) {
        showToast('请先加入学习单元', 'error');
        return;
    }
    var modules = [];
    var seen = {};
    studies.forEach(function(it) {
        var mt = it.module_type || 'other';
        if (!seen[mt]) {
            seen[mt] = true;
            modules.push(mt);
        }
    });
    modules.sort(function(a, b) {
        var ia = TASK_LIBRARY_MODULE_ORDER.indexOf(a);
        var ib = TASK_LIBRARY_MODULE_ORDER.indexOf(b);
        if (ia === -1 && ib === -1) return taskLibraryModuleLabel(a).localeCompare(taskLibraryModuleLabel(b), 'zh');
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
    });
    var tabs = document.getElementById('taskStageTestModuleTabs');
    if (!tabs) return;
    _stageTestModalModule = modules[0] || '';
    tabs.innerHTML = modules.map(function(mt) {
        var active = mt === _stageTestModalModule;
        return '<button type="button" data-mt="' + escapeTeacherAttr(mt) + '" class="btn ' +
            (active ? '' : 'btn-secondary') + '" style="padding:4px 10px;font-size:12px;" ' +
            'onclick="selectStageTestModule(this.getAttribute(\'data-mt\'))">' +
            taskLibraryModuleLabel(mt) + '</button>';
    }).join('');
    renderStageTestRangeUI();
    showModal('taskStageTestModal');
}

function selectStageTestModule(moduleType) {
    _stageTestModalModule = moduleType;
    var tabs = document.getElementById('taskStageTestModuleTabs');
    if (tabs) {
        tabs.querySelectorAll('button[data-mt]').forEach(function(btn) {
            var active = btn.getAttribute('data-mt') === moduleType;
            btn.className = 'btn ' + (active ? '' : 'btn-secondary');
        });
    }
    renderStageTestRangeUI();
}

function renderStageTestRangeUI() {
    var fromSel = document.getElementById('taskStageTestFrom');
    var toSel = document.getElementById('taskStageTestTo');
    if (!fromSel || !toSel) return;
    var units = getStageTestModuleUnits(_stageTestModalModule);
    if (!units.length) {
        fromSel.innerHTML = '';
        toSel.innerHTML = '';
        updateStageTestPreview();
        return;
    }
    var opts = units.map(function(it, idx) {
        var label = (idx + 1) + '. ' + (it.unit_title || it.unit_id);
        return '<option value="' + escapeTeacherAttr(it.unit_id) + '">' + escapeTeacherAttr(label) + '</option>';
    }).join('');
    fromSel.innerHTML = opts;
    toSel.innerHTML = opts;
    var defaultFrom = Math.max(0, units.length - 3);
    fromSel.selectedIndex = defaultFrom;
    toSel.selectedIndex = units.length - 1;
    onStageTestRangeChange();
}

function onStageTestRangeChange() {
    var fromSel = document.getElementById('taskStageTestFrom');
    var toSel = document.getElementById('taskStageTestTo');
    if (!fromSel || !toSel || fromSel.selectedIndex < 0 || toSel.selectedIndex < 0) {
        updateStageTestPreview();
        return;
    }
    if (fromSel.selectedIndex > toSel.selectedIndex) {
        toSel.selectedIndex = fromSel.selectedIndex;
    }
    updateStageTestPreview();
}

function applyStageTestQuickRange(count) {
    var units = getStageTestModuleUnits(_stageTestModalModule);
    var fromSel = document.getElementById('taskStageTestFrom');
    var toSel = document.getElementById('taskStageTestTo');
    if (!units.length || !fromSel || !toSel) return;
    toSel.selectedIndex = units.length - 1;
    if (!count) {
        fromSel.selectedIndex = 0;
    } else {
        fromSel.selectedIndex = Math.max(0, units.length - count);
    }
    updateStageTestPreview();
}

function collectStageTestRangeUnitIds() {
    var fromSel = document.getElementById('taskStageTestFrom');
    var toSel = document.getElementById('taskStageTestTo');
    if (!fromSel || !toSel) return [];
    var units = getStageTestModuleUnits(_stageTestModalModule);
    if (!units.length) return [];
    var fromIdx = fromSel.selectedIndex;
    var toIdx = toSel.selectedIndex;
    if (fromIdx < 0 || toIdx < 0) return [];
    if (fromIdx > toIdx) {
        var tmp = fromIdx;
        fromIdx = toIdx;
        toIdx = tmp;
    }
    var slice = units.slice(fromIdx, toIdx + 1);
    return slice.map(function(it) { return it.unit_id; });
}

function updateStageTestPreview() {
    var box = document.getElementById('taskStageTestPreview');
    if (!box) return;
    var unitIds = collectStageTestRangeUnitIds();
    if (!unitIds.length) {
        box.textContent = '请先在清单中加入该科目的学习单元';
        return;
    }
    box.textContent = '将插入：' + buildStageTestTitle(unitIds) + '（覆盖 ' + unitIds.length + ' 个单元）';
}

function confirmInsertStageTest() {
    var unitIds = collectStageTestRangeUnitIds();
    if (!unitIds.length) {
        showToast('请选择覆盖范围', 'error');
        return;
    }
    if (!insertStageTestForUnits(unitIds)) return;
    closeModal('taskStageTestModal');
    showToast('已插入阶段测（记得保存清单）', 'success');
}

function renderTaskLivePlanList() {
    var box = document.getElementById('taskLivePlanList');
    if (!box) return;
    var title = document.getElementById('taskLivePlanTitle');
    if (!_taskLiveItems.length) {
        if (title) title.textContent = '当前生效清单';
        box.innerHTML = '<p style="color:#666;margin:0;">暂无生效清单</p>';
        return;
    }
    var studyN = _taskLiveItems.filter(function(it) { return it.item_type === 'study'; }).length;
    var testN = _taskLiveItems.filter(function(it) { return it.item_type === 'test'; }).length;
    if (title) {
        title.textContent = '当前生效清单（共 ' + _taskLiveItems.length + ' 项）';
    }
    var html = '';
    var isUnits = readTaskPackMode() === 'units_per_day';
    html += '<p style="color:#64748b;font-size:12px;margin:0 0 8px;">这是<strong>完整学习队列</strong>（学 ' +
        studyN + ' / 测 ' + testN + '），不是学生今天要做的全部。' +
        (isUnits
            ? '系统按各科每日配额从中逐日释放，请看下方「每日任务排程」。'
            : '系统按每日预算从中逐日装箱，请看下方「装箱预览」。') +
        '</p>';
    if (_taskPendingPlanChange) {
        html += '<p style="color:#b45309;margin:0 0 8px;">有待生效草稿/排程变更；到达生效日后将替换本列表。</p>';
    }
    var segments = groupTaskItemsByModuleSegments(_taskLiveItems);
    segments.forEach(function(seg) {
        var mt = seg.moduleType;
        var pendingStudy = 0;
        var doneStudy = 0;
        var tN = 0;
        var tPass = 0;
        seg.indices.forEach(function(i) {
            var it = _taskLiveItems[i];
            if (it.item_type === 'test') {
                tN++;
                if (isTaskItemDone(it)) tPass++;
            } else if (isTaskItemDone(it)) {
                doneStudy++;
            } else {
                pendingStudy++;
            }
        });
        var collapsed = isTaskSectionCollapsed(mt, _taskLiveCollapse);
        var showDone = !!_taskLiveShowCompleted[mt];
        var arrow = collapsed ? '▶' : '▼';
        var safeMt = String(mt).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        var summary = escapeTeacherAttr(taskModuleShortLabel(mt)) +
            ' · 待学 ' + pendingStudy + ' · 已完成 ' + doneStudy +
            ' · 测 ' + tN + (tN ? ('（过关 ' + tPass + '）') : '');
        html += '<div style="position:sticky;top:0;z-index:1;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;margin:4px 0;padding:4px 6px;">';
        html += '<div style="display:flex;flex-wrap:wrap;gap:4px;align-items:center;">';
        html += '<button type="button" class="btn btn-secondary" style="padding:3px 8px;font-size:12px;font-weight:600;" ' +
            'onclick="toggleTaskLiveSection(\'' + safeMt + '\')">' + arrow + ' ' + summary + '</button>';
        if (doneStudy + tPass > 0) {
            html += '<button type="button" class="btn btn-secondary" style="padding:2px 6px;font-size:11px;" ' +
                'onclick="toggleTaskLiveShowCompleted(\'' + safeMt + '\')">' +
                (showDone ? '收起已完成' : ('展开已完成 ' + (doneStudy + tPass))) + '</button>';
        }
        html += '</div></div>';
        if (collapsed) return;
        var displayIdx = orderSegmentIndicesForDisplay(_taskLiveItems, seg.indices, showDone);
        displayIdx.forEach(function(idx) {
            var it = _taskLiveItems[idx];
            var done = isTaskItemDone(it);
            html += '<div style="padding:2px 6px;font-size:13px;' +
                (done ? 'color:#94a3b8;' : 'color:#334155;') + '">' +
                (idx + 1) + '. ' + formatTaskPlanItemBody(it) + '</div>';
        });
        if (!showDone && (doneStudy + tPass) > 0) {
            html += '<div style="padding:2px 8px;font-size:12px;color:#94a3b8;">已收起 ' +
                (doneStudy + tPass) + ' 条已完成</div>';
        }
    });
    box.innerHTML = html;
}

function findDraftInsertIndexForUnit(unit) {
    var moduleType = unit && unit.module_type;
    if (!moduleType) return _taskDraftItems.length;
    var newNo = Number(unit.unit_no);
    if (isNaN(newNo)) {
        var m = /_u(\d+)$/i.exec(String(unit.unit_id || ''));
        newNo = m ? Number(m[1]) : 0;
    }
    var firstSame = -1;
    var insertAfterStudy = -1;
    for (var i = 0; i < _taskDraftItems.length; i++) {
        var it = _taskDraftItems[i];
        var mt = inferTaskItemModuleType(it, _taskDraftItems);
        if (mt !== moduleType) continue;
        if (firstSame < 0) firstSame = i;
        if (it.item_type !== 'study') continue;
        var no = draftItemUnitNo(it);
        if (no != null && no < newNo) insertAfterStudy = i;
    }
    if (firstSame < 0) return _taskDraftItems.length;
    // 第2组插到第1组正下方（同科按组号），而不是甩到该科末尾
    if (insertAfterStudy >= 0) return insertAfterStudy + 1;
    return firstSame;
}

function addUnitToTaskDraft(unitId) {
    if (_taskDraftItems.some(function(it) {
        return it.item_type === 'study' && it.unit_id === unitId && it.status !== 'removed';
    })) {
        showToast('该单元已在计划中', 'error');
        return;
    }
    var u = _taskUnitCatalog.find(function(x) { return x.unit_id === unitId; });
    if (!u) return;
    var row = {
        item_type: 'study',
        unit_id: unitId,
        module_type: u.module_type,
        unit_title: u.title,
        status: 'pending'
    };
    var at = findDraftInsertIndexForUnit(u);
    _taskDraftItems.splice(at, 0, row);
    expandTaskPlanModule(u.module_type);
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    renderTaskUnitLibrary();
    scrollTaskPlanSegmentIntoView(u.module_type);
    schedulePackPreviewRefresh();
}

function moveTaskDraft(idx, delta) {
    var j = idx + delta;
    if (j < 0 || j >= _taskDraftItems.length) return;
    var tmp = _taskDraftItems[idx];
    _taskDraftItems[idx] = _taskDraftItems[j];
    _taskDraftItems[j] = tmp;
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    schedulePackPreviewRefresh();
}

function removeTaskDraft(idx) {
    _taskDraftItems.splice(idx, 1);
    _taskPlanOpenMenuIdx = null;
    renderTaskPlanList();
    renderTaskUnitLibrary();
    schedulePackPreviewRefresh();
}

async function loadTeacherTaskPlan() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    var sid = sel.value;
    var planRes = await teacherApiGet('/api/task/students/' + encodeURIComponent(sid) + '/plan');
    if (planRes.error) {
        if (planRes._httpStatus === 401) {
            showToast('教师登录已失效，请重新登录', 'error');
            currentTeacher = null;
            showScreen('teacherLoginScreen');
            return;
        }
        showToast((planRes.error && planRes.error.message) || '加载计划失败', 'error');
        return;
    }
    var data = planRes.data || {};
    await applyTeacherTaskPlanData(data);
}

async function saveTeacherTaskPlan() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    _taskDraftItems = normalizeStageTestOrderClient(
        regroupDraftItemsByModule(_taskDraftItems)
    );
    var items = _taskDraftItems.map(function(it) {
        return {
            item_type: it.item_type,
            unit_id: it.unit_id || null,
            module_type: it.module_type,
            test_unit_ids: it.test_unit_ids || [],
            test_title: it.test_title || '',
            est_minutes: it.est_minutes,
            status: it.status || 'pending'
        };
    });
    var effYmd = readTaskEffectiveFromInput();
    var result = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(sel.value) + '/plan',
        { items: items, effective_from: effYmd }
    );
    if (result.error) {
        showToast((result.error && result.error.message) || '保存失败', 'error');
        return;
    }
    var data = result.data || {};
    var appliedNow = !(data.draft_pending || (data.draft && data.draft.length));
    if (appliedNow) {
        showToast('清单已保存，当前生效清单已更新', 'success');
    } else {
        showToast(
            '草稿已保存，' + taskEffectiveLabel(data.draft_effective_from || effYmd) +
            ' 起才替换左侧「当前生效」；若要马上改，请把生效日期改成今天再保存',
            'info'
        );
    }
    if (result.data) {
        await applyTeacherTaskPlanData(result.data);
    } else {
        await loadTeacherTaskPlan();
    }
}

async function applyTeacherTaskPlanData(data) {
    _taskPendingPlanChange = !!data.pending_plan_change;
    _taskHasDbDraft = !!(data.draft_pending || (data.draft && data.draft.length));
    _taskPendingEffectiveLabel = taskEffectiveLabel(
        data.pending_effective_from || data.draft_effective_from || readTaskEffectiveFromInput()
    );
    _taskPlanOpenMenuIdx = null;
    var liveRows = (data.live || []).filter(function(it) {
        return it.status !== 'removed';
    });
    var liveByUnit = {};
    var liveTests = [];
    liveRows.forEach(function(it) {
        if (it.item_type === 'study' && it.unit_id) {
            liveByUnit[it.unit_id] = it;
        } else if (it.item_type === 'test') {
            liveTests.push(it);
        }
    });
    function matchLiveTest(draftIt) {
        var covers = normalizeTestUnitIds(draftIt.test_unit_ids).slice().sort().join('\u0001');
        if (!covers) return null;
        for (var i = 0; i < liveTests.length; i++) {
            var c = normalizeTestUnitIds(liveTests[i].test_unit_ids).slice().sort().join('\u0001');
            if (c === covers) return liveTests[i];
        }
        return null;
    }
    _taskLiveItems = liveRows.map(function(it) {
        return {
            item_type: it.item_type,
            unit_id: it.unit_id,
            module_type: it.module_type,
            unit_title: it.unit_title,
            test_title: it.test_title,
            test_unit_ids: it.test_unit_ids || [],
            status: it.status || 'pending',
            study_completed: Number(it.study_completed) || 0,
            test_passed: Number(it.test_passed) || 0
        };
    });
    var source = (data.draft && data.draft.length) ? data.draft : liveRows;
    _taskDraftItems = source.map(function(it) {
        var studyDone = Number(it.study_completed) || 0;
        var testPass = Number(it.test_passed) || 0;
        if (it.item_type === 'study' && it.unit_id && liveByUnit[it.unit_id]) {
            studyDone = Number(liveByUnit[it.unit_id].study_completed) || 0;
        } else if (it.item_type === 'test') {
            var liveT = matchLiveTest(it);
            if (liveT) testPass = Number(liveT.test_passed) || 0;
        }
        return {
            item_type: it.item_type,
            unit_id: it.unit_id,
            module_type: it.module_type,
            unit_title: it.unit_title,
            test_title: it.test_title,
            test_unit_ids: it.test_unit_ids || [],
            est_minutes: it.est_minutes,
            status: it.status || 'pending',
            study_completed: studyDone,
            test_passed: testPass
        };
    });
    _taskDraftItems = normalizeStageTestOrderClient(_taskDraftItems);
    var tp = data.time_profile || {};
    syncTaskModuleQuotasFromProfile(tp);
    var pendingMode = tp.pending_pack_mode != null ? tp.pending_pack_mode : (tp.pack_mode || 'time_budget');
    if (pendingMode !== 'units_per_day') {
        pendingMode = 'units_per_day';
    }
    setTaskPackMode(pendingMode);
    bindTaskScheduleModeInputs();
    var wd = document.getElementById('taskWeekdayMinutes');
    var we = document.getElementById('taskWeekendMinutes');
    if (wd) wd.value = tp.pending_weekday_minutes != null ? tp.pending_weekday_minutes : (tp.weekday_minutes || 40);
    if (we) we.value = tp.pending_weekend_minutes != null ? tp.pending_weekend_minutes : (tp.weekend_minutes || 90);
    // 无待生效时不要重置成「明天」，否则下次保存又进草稿、当前生效不更新
    var effFrom = data.draft_effective_from || data.pending_profile_effective_from ||
        readTaskEffectiveFromInput() || taskFormatLocalYmd(new Date());
    setTaskEffectiveFromInput(effFrom);
    var hint = document.getElementById('taskPlanHint');
    if (hint) {
        var base = '各科按清单顺序逐日释放；周中/周末配额独立；多科同日合并展示。';
        var effLabel = taskEffectiveLabel(data.pending_effective_from || effFrom);
        hint.textContent = data.pending_plan_change
            ? base + ' 有待生效变更（' + effLabel + ' 起生效）；上面「当前生效」才是学生今日所见。'
            : base + ' 可选择生效日期；选「今天」保存后立即更新清单并重排今日任务。';
    }
    toggleTaskScheduleModeUI();
    updateTaskPlanSectionTitles(data);
    renderTaskPlanPauseBanner(data.plan_pause || null);
    renderTaskLivePlanList();
    renderTaskPlanList();
    renderTaskUnitLibrary();
    var sel = document.getElementById('taskPlanStudentSelect');
    if (sel && sel.value) await loadTaskPackPreviews(sel.value);
}

async function saveTeacherScheduleProfile() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    rememberTaskModuleQuotasFromForm();
    // 配额改完默认今天生效，避免改了数字却因「明天」看起来无效
    var eff = readTaskEffectiveFromInput() || taskFormatLocalYmd(new Date());
    setTaskEffectiveFromInput(eff);
    // 保存排程只写配额，勿整页重载计划（会把未保存的右侧清单清掉）
    var preservedDraft = (_taskDraftItems || []).map(function(it) {
        return {
            item_type: it.item_type,
            unit_id: it.unit_id,
            module_type: it.module_type,
            unit_title: it.unit_title,
            test_title: it.test_title,
            test_unit_ids: (it.test_unit_ids || []).slice(),
            est_minutes: it.est_minutes,
            status: it.status || 'pending',
            study_completed: Number(it.study_completed) || 0,
            test_passed: Number(it.test_passed) || 0
        };
    });
    var payload = {
        pack_mode: 'units_per_day',
        module_quotas: collectTaskModuleQuotasPayload(),
        effective_from: eff
    };
    if (!payload.module_quotas.length && _taskModuleQuotas) {
        payload.module_quotas = Object.keys(_taskModuleQuotas).map(function(mt) {
            return {
                module_type: mt,
                weekday_units: _taskModuleQuotas[mt].weekday_units,
                weekend_units: _taskModuleQuotas[mt].weekend_units
            };
        });
    }
    var result = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(sel.value) + '/time-profile',
        payload
    );
    if (result.error) {
        showToast((result.error && result.error.message) || '保存失败', 'error');
        return;
    }
    var toastMsg = '排程设置已保存（' + taskEffectiveLabel(readTaskEffectiveFromInput()) + ' 起生效）';
    if (preservedDraft.length && !_taskHasDbDraft) {
        toastMsg += '；右侧清单仍在编辑中，请点「保存清单草稿」';
    }
    showToast(toastMsg, preservedDraft.length && !_taskHasDbDraft ? 'info' : 'success');
    if (result.data) {
        var tp = result.data;
        syncTaskModuleQuotasFromProfile(tp);
        var effFrom = tp.pending_effective_from || readTaskEffectiveFromInput() || eff;
        setTaskEffectiveFromInput(effFrom);
        _taskPendingEffectiveLabel = taskEffectiveLabel(effFrom);
        if (preservedDraft.length && !_taskHasDbDraft) {
            _taskDraftItems = preservedDraft;
        }
        var hint = document.getElementById('taskPlanHint');
        if (hint) {
            var base = '各科按清单顺序逐日释放；周中/周末配额独立；多科同日合并展示。';
            var effLabel = taskEffectiveLabel(effFrom);
            var profilePending = tp.pending_effective_from != null;
            hint.textContent = (_taskHasDbDraft || profilePending)
                ? base + ' 有待生效变更（' + effLabel + ' 起生效）；上面「当前生效」才是学生今日所见。'
                : base + ' 可选择生效日期；选「今天」保存后立即更新清单并重排今日任务。';
        }
        updateTaskPlanSectionTitles({
            draft_pending: _taskHasDbDraft,
            draft: _taskHasDbDraft ? preservedDraft : [],
            pending_effective_from: tp.pending_effective_from,
            draft_effective_from: effFrom
        });
        toggleTaskScheduleModeUI();
        renderTaskPlanList();
        await loadTaskPackPreviews(sel.value);
    }
}

async function saveTeacherTimeProfile() {
    return saveTeacherScheduleProfile();
}

async function clearTeacherDailySchedule() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) {
        showToast('请先选择学生', 'error');
        return;
    }
    if (!confirm('清空该生的任务清单、草稿与已生成的每日任务？此操作不可撤销。')) return;
    var result = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(sel.value) + '/clear-daily-schedule',
        {}
    );
    if (result.error) {
        showToast((result.error && result.error.message) || '清除失败', 'error');
        return;
    }
    var d = result.data || {};
    showToast(
        '已清空：清单 ' + (d.cleared_plan_items || 0) +
        ' 项，每日任务 ' + (d.deleted || 0) + ' 条',
        'success'
    );
    _taskDraftItems = [];
    _taskLiveItems = [];
    _taskModuleQuotas = {};
    _taskPlanPause = null;
    await loadTeacherTaskPlan();
}

function renderTaskPlanPauseBanner(pause) {
    _taskPlanPause = pause || null;
    var box = document.getElementById('taskPlanPauseBanner');
    var resumeBtn = document.getElementById('taskPlanResumeBtn');
    if (resumeBtn) {
        resumeBtn.style.display = pause ? 'inline-block' : 'none';
    }
    if (!box) return;
    if (!pause) {
        box.style.display = 'none';
        box.innerHTML = '';
        return;
    }
    box.style.display = 'block';
    if (pause.active) {
        box.innerHTML = '<strong>计划已暂停</strong>：' +
            escapeTeacherAttr(pause.pause_from) + ' 起，至 ' +
            escapeTeacherAttr(pause.resume_on) + ' 恢复。原因：' +
            escapeTeacherAttr(pause.reason || '') +
            '。暂停期内不新发每日任务。';
    } else {
        box.innerHTML = '<strong>计划将暂停</strong>：' +
            escapeTeacherAttr(pause.pause_from) + ' 起暂停，' +
            escapeTeacherAttr(pause.resume_on) + ' 恢复。原因：' +
            escapeTeacherAttr(pause.reason || '') + '。';
    }
}

function openPlanPauseModal() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) {
        showToast('请先选择学生', 'error');
        return;
    }
    if (!_taskLiveItems || !_taskLiveItems.length) {
        showToast('该生尚无生效清单，无法暂停', 'error');
        return;
    }
    var today = taskFormatLocalYmd(new Date());
    var fromEl = document.getElementById('taskPauseFrom');
    var toEl = document.getElementById('taskPauseResumeOn');
    var reasonEl = document.getElementById('taskPauseReason');
    if (fromEl) {
        fromEl.value = (_taskPlanPause && _taskPlanPause.pause_from) || today;
        fromEl.min = today;
    }
    if (toEl) {
        var defResume = (_taskPlanPause && _taskPlanPause.resume_on) || '';
        if (!defResume) {
            var d = new Date();
            d.setDate(d.getDate() + 3);
            defResume = taskFormatLocalYmd(d);
        }
        toEl.value = defResume;
        toEl.min = today;
    }
    if (reasonEl) reasonEl.value = (_taskPlanPause && _taskPlanPause.reason) || '';
    showModal('taskPlanPauseModal');
}

async function confirmTeacherPlanPause() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    var fromEl = document.getElementById('taskPauseFrom');
    var toEl = document.getElementById('taskPauseResumeOn');
    var reasonEl = document.getElementById('taskPauseReason');
    var pauseFrom = fromEl && fromEl.value;
    var resumeOn = toEl && toEl.value;
    var reason = reasonEl ? String(reasonEl.value || '').trim() : '';
    if (!pauseFrom || !resumeOn) {
        showToast('请填写暂停起始日与恢复日期', 'error');
        return;
    }
    if (!reason) {
        showToast('请填写暂停原因', 'error');
        return;
    }
    var result = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(sel.value) + '/plan-pause',
        { pause_from: pauseFrom, resume_on: resumeOn, reason: reason }
    );
    if (result.error) {
        showToast((result.error && result.error.message) || '暂停失败', 'error');
        return;
    }
    closeModal('taskPlanPauseModal');
    showToast('计划已设为暂停', 'success');
    await loadTeacherTaskPlan();
}

async function clearTeacherPlanPause() {
    var sel = document.getElementById('taskPlanStudentSelect');
    if (!sel || !sel.value) return;
    if (!confirm('确定提前恢复该生计划？恢复后将按清单继续排每日任务。')) return;
    var result = await teacherApiPost(
        '/api/task/students/' + encodeURIComponent(sel.value) + '/plan-pause/clear',
        {}
    );
    if (result.error) {
        showToast((result.error && result.error.message) || '恢复失败', 'error');
        return;
    }
    showToast('已提前恢复计划', 'success');
    await loadTeacherTaskPlan();
}
