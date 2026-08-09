// 口语练习 ASR 配置（与 P4 跟读同一套接口）
// 默认走主站同源 /api/p4/transcribe，由 local_server.py 转发到 https://p4.oyenglish.com.cn
window.API_CONFIG = {
    TRANSCRIBE_PATH: '/api/p4/transcribe'
};
