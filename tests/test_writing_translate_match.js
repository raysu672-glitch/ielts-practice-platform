/**
 * 写作句子翻译判分（2026-09-20 重写为「规则四径」）。
 *
 * 旧口径是逐字全等，线上 11 次提交全部 0.0 分 —— 学生必须把参考译文一字不差默写
 * 才算对。这里锁住新口径的行为：
 *   - 逐字正确 / 只差标点空白           → 对
 *   - 增删虚词（的/了）、答案略长（加补充说明）→ 对
 *   - 语序颠倒（词都对）                → 错
 *   - 只写半句（漏译）                  → 错
 *   - 漏掉逻辑关系词                    → 错
 *   - 漏掉关键信息（数字/英文专名）      → 错
 */
const assert = require('node:assert/strict');
const match = require('../sources/juzifanyixinceshi/match.js');

const REF = '互联网最大的优势在于它极大地简化了人与人之间的沟通。';

// ── 应该判对 ──────────────────────────────────────────────
// 1. 逐字正确
assert.equal(match.gradeChinese(REF, REF).ok, true, '逐字正确应通过');
// 2. 只差标点与空白
assert.equal(match.gradeChinese('互联网最大的优势，在于它极大地简化了人与人之间的沟通！', REF).ok, true);
assert.equal(match.gradeChinese('互联网 最大的优势在于它极大地简化了人与人之间的沟通。', REF).ok, true);
// 3. 去掉虚词「的」「了」（中文里常见的合法简写）
assert.equal(
  match.gradeChinese('互联网最大优势在于它极大地简化人与人之间沟通', REF).ok,
  true,
  '去掉虚词的合法简写应通过'
);
// 4. 答案略长（补了一句自己的话）—— 不应因为「多写了」而判错
assert.equal(
  match.gradeChinese('我认为互联网最大的优势在于它极大地简化了人与人之间的沟通，这一点很重要。', REF).ok,
  true
);

// ── 应该判错 ──────────────────────────────────────────────
// 5. 语序颠倒：词全对，但顺序乱了
const shuffled = match.gradeChinese('极大地简化了人与人之间的沟通互联网最大的优势在于它', REF);
assert.equal(shuffled.ok, false, '语序颠倒应判错');
assert.ok(shuffled.order < match.MIN_ORDER, '语序一致率应低于门槛');

// 6. 只写后半句（漏译）
const half = match.gradeChinese('极大地简化了人与人之间的沟通', REF);
assert.equal(half.ok, false, '只写半句应判错');

// 7. 幅度较大的同义改写：规则法的已知代价，这里锁住「会判错」以免误以为已放宽
assert.equal(
  match.gradeChinese('互联网最大的好处是大大方便了人们的交流。', REF).ok,
  false,
  '规则法放不过同义改写（产品已确认接受）'
);

// 8. 空答案
assert.equal(match.gradeChinese('', REF).ok, false);
assert.equal(match.gradeChinese('   ', REF).ok, false);
assert.equal(match.gradeChinese('', REF).reasons.length > 0, true);

// ── 逻辑关系词 ────────────────────────────────────────────
const REF_CAUSE = '因为学生可以随时提问，所以他们的学习效率更高。';
assert.equal(match.gradeChinese('由于学生可以随时提问，因此他们的学习效率更高。', REF_CAUSE).ok, true,
  '同义逻辑词（因为→由于、所以→因此）应通过');
const noLogic = match.gradeChinese('学生可以随时提问，他们的学习效率更高。', REF_CAUSE);
assert.equal(noLogic.ok, false, '丢掉因果连接词应判错');
assert.ok(noLogic.missingLogic.length > 0, '应报出缺失的逻辑关系词');

// ── 关键信息点：数字 / 百分比 / 英文专名 ──────────────────
const REF_NUM = '过去十年里，网络使用率从 38% 稳定增长到 61%。';
assert.equal(match.gradeChinese('过去十年里网络使用率从38%稳定增长到61%', REF_NUM).ok, true);
const noPct = match.gradeChinese('过去十年里网络使用率稳定增长', REF_NUM);
assert.equal(noPct.ok, false, '漏掉数字应判错');
assert.ok(noPct.missingHard.length > 0, '应报出漏掉的关键信息');

const REF_EN = '例如，学生可以用 FaceTime 与家人保持日常联系。';
assert.equal(match.gradeChinese('例如学生可以用facetime与家人保持日常联系', REF_EN).ok, true,
  '英文专名大小写不应影响判定');
assert.equal(match.gradeChinese('例如学生可以与家人保持日常联系', REF_EN).ok, false, '漏掉 FaceTime 应判错');

// ── 旧接口保留（错题本等仍用严格比对） ────────────────────
assert.equal(match.isChineseMatch(REF, REF), true);
assert.equal(match.isChineseMatch('互联网最大优势在于它极大地简化了人与人之间的沟通。', REF), false);

console.log('test_writing_translate_match.js ok');
