// 跟读 ASR：默认走主站同源 /api/p4，由 local_server.py 转发到 p4.oyenglish.com.cn
// （浏览器直连外网 ASR 会因 CORS 报 Failed to fetch）
window.API_CONFIG = {
    API_BASE: '/api/p4'
};
