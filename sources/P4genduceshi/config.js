// P4 跟读测试 API 配置
// 默认走主站同源 Python 服务（scripts/local_server.py）的 /api/p4/*
// 主站会把请求转发到真实 ASR 服务（默认 https://p4.oyenglish.com.cn）
window.API_CONFIG = {
    // 留空表示使用当前页面同源地址
    API_BASE: '',
    TRANSCRIBE_PATH: '/api/p4/transcribe'
};
