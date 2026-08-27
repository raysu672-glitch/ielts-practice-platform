const assert = require('node:assert/strict');
const match = require('../sources/juzifanyixinceshi/match.js');

assert.equal(match.isChineseMatch(
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。',
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。'
), true);

assert.equal(match.isChineseMatch(
  '互联网最大的优势在于它极大地简化了人与人之间的沟通',
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。'
), true);

assert.equal(match.isChineseMatch(
  '互联网最大的优势，在于它极大地简化了人与人之间的沟通！',
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。'
), true);

assert.equal(match.isChineseMatch(
  '互联网 最大的优势在于它极大地简化了人与人之间的沟通。',
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。'
), true);

assert.equal(match.isChineseMatch(
  '互联网最大优势在于它极大地简化了人与人之间的沟通。',
  '互联网最大的优势在于它极大地简化了人与人之间的沟通。'
), false);

assert.equal(match.isChineseMatch('', '互联网最大的优势在于它极大地简化了人与人之间的沟通。'), false);
assert.equal(match.isChineseMatch('   ', '互联网最大的优势在于它极大地简化了人与人之间的沟通。'), false);

console.log('test_writing_translate_match.js ok');
