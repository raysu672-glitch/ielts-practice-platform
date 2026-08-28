// 应用壳：数据库、通用 UI、入口路由
// Supabase 为备用数据源；生产默认使用同域 SQLite API。
var SUPABASE_URL = window.IELTS_SUPABASE_URL || '';
var SUPABASE_KEY = window.IELTS_SUPABASE_KEY || '';
var db = null;
try {
    if (window.createLocalDbClient && location.protocol !== 'file:') {
        db = window.createLocalDbClient('/api/db');
        console.log('已连接本地 SQLite 数据库');
    } else if (SUPABASE_URL && SUPABASE_KEY && window.supabase && typeof window.supabase.createClient === 'function') {
        db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    } else {
        console.warn('本地数据库和 Supabase 均不可用，网络功能不可用');
    }
} catch (e) {
    console.error('数据库初始化失败:', e);
}

// 全局状态
var currentStudent = null;
var STUDENT_SESSION_KEY = 'ouye_student_session_v1';
var STUDENT_SESSION_DAYS = 7;

async function apiFetch(url, options) {
    options = options || {};
    var headers = Object.assign({}, options.headers || {});
    if (options.method && options.method.toUpperCase() !== 'GET' && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }
    var resp = await fetch(url, Object.assign({}, options, {
        credentials: 'include',
        headers: headers
    }));
    var result = null;
    try {
        result = await resp.json();
    } catch (e) {
        result = { data: null, error: { message: '响应解析失败' } };
    }
    if (!resp.ok && result && !result.error) {
        result.error = { message: '请求失败：' + resp.status };
    }
    result._httpStatus = resp.status;
    return result;
}

async function authLogout(role) {
    try {
        var q = role ? ('?role=' + encodeURIComponent(role)) : '';
        await apiFetch('/api/auth/logout' + q, { method: 'POST', body: '{}' });
    } catch (e) {
        console.warn('退出登录请求失败:', e);
    }
}

async function authMe(role) {
    var q = role ? ('?role=' + encodeURIComponent(role)) : '';
    return apiFetch('/api/auth/me' + q, { method: 'GET' });
}

// 工具函数
var AUTH_SCREENS = ['studentLoginScreen', 'teacherLoginScreen', 'writingTeacherLoginScreen'];
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
    document.body.classList.toggle('auth-view', AUTH_SCREENS.indexOf(screenId) !== -1);
}

function showToast(message, type) {
    type = type || 'info';
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show ' + type;
    setTimeout(function() { toast.classList.remove('show'); }, 3000);
}

function showModal(modalId) { document.getElementById(modalId).classList.add('active'); }
function closeModal(modalId) { document.getElementById(modalId).classList.remove('active'); }

function escapeHtml(value) {
    return String(value === undefined || value === null ? '' : value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function escapeJsString(value) {
    return String(value === undefined || value === null ? '' : value)
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '');
}


function initEntryRoute() {
    const params = new URLSearchParams(window.location.search || '');
    const role = (params.get('role') || params.get('entry') || window.location.hash.replace('#', '') || '').toLowerCase();
    if (role === 'writing' || role === 'writing-teacher' || role === 'writing_teacher') {
        showScreen('writingTeacherLoginScreen');
        return;
    }
    if (role === 'teacher') {
        showScreen('teacherLoginScreen');
        if (typeof restoreTeacherSession === 'function') {
            restoreTeacherSession();
        }
        return;
    }
    if (role === 'student') {
        showScreen('studentLoginScreen');
    }
    restoreStudentSession();
}
