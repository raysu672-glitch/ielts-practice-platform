// 跟读上传失败时给页面的短说明。413 是 nginx 拒绝了请求体，识别服务没收到音频。
function uploadFailureMessage(status, errText, size) {
    if (status === 413) {
        const kb = Math.max(1, Math.round((size || 0) / 1024));
        return '录音约 ' + kb + ' KB，超过网站上传大小限制，音频没有送到识别服务';
    }
    const brief = String(errText || '')
        .replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .slice(0, 160);
    return '后端返回错误 ' + status + (brief ? '：' + brief : '');
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { uploadFailureMessage: uploadFailureMessage };
}
