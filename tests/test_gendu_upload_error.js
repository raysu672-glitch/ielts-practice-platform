const assert = require('node:assert/strict');
const { uploadFailureMessage } = require('../sources/P4genduceshi/upload-error.js');

const nginx413 = '<html><head><title>413 Request Entity Too Large</title></head><body><center><h1>413 Request Entity Too Large</h1></center><hr><center>nginx</center></body></html>';

const tooLarge = uploadFailureMessage(413, nginx413, 4 * 1024 * 1024);
assert.match(tooLarge, /录音约 4096 KB/);
assert.match(tooLarge, /超过网站上传大小限制/);
assert.equal(tooLarge.includes('<html>'), false);
assert.equal(tooLarge.includes('nginx'), false);

assert.equal(
    uploadFailureMessage(413, nginx413, 0),
    '录音约 1 KB，超过网站上传大小限制，音频没有送到识别服务'
);

const other = uploadFailureMessage(502, '<html><body>bad gateway</body></html>  ' + 'x'.repeat(400), 1000);
assert.match(other, /^后端返回错误 502：/);
assert.equal(other.includes('<'), false);
assert.ok(other.length < 220);
