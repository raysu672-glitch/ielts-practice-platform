/**
 * 词伙答案「多写法」支持（2026-09-20）。
 *
 * 题库里有 11 条用 `/` 表示两种说法都行（climb steadily/solidly、
 * curb crime / deter crime、the elderly / the senior population…）。
 * 数据没拆开，旧逻辑把整串当唯一答案，学生写 a 或 b 都判错 —— 这类题永远拿不到分。
 * 现在按 `/` 拆成多个可接受答案，任一命中即算对。
 *
 * 直接 require 真实上线的 sources/shared/phrase_answer.js（不复制逻辑），
 * 保证测的就是三个前端页面共用的那份代码。
 * 「11 条一个不落」这条用数据驱动：每条都断言两种写法都算对。
 */
const assert = require('node:assert/strict');

const {
  phraseAcceptList,
  phraseMatchesAny,
  phraseIsCorrect,
  phraseDisplayAnswer,
  phrasePrimaryAnswer,
  phraseAcceptedWordSets,
} = require('../sources/shared/phrase_answer.js');

// 线上题库里全部 11 条多写法，逐条断言两边都算对
const MULTI = [
  ['climb steadily/solidly', 'climb steadily', 'climb solidly'],
  ['continue to increase / soar', 'continue to increase', 'continue to soar'],
  ['a modest dip/drop over the last decade',
    'a modest dip over the last decade', 'a modest drop over the last decade'],
  ['remain stable/steady', 'remain stable', 'remain steady'],
  ['in the final phase/stage', 'in the final phase', 'in the final stage'],
  ['curb crime / deter crime', 'curb crime', 'deter crime'],
  ['be ethically wrong / theoretically wrong', 'be ethically wrong', 'be theoretically wrong'],
  ['consumer goods /products', 'consumer goods', 'consumer products'],
  ['digital/online dating', 'digital dating', 'online dating'],
  ['dip/drop to only 2.5%', 'dip to only 2.5%', 'drop to only 2.5%'],
  ['the elderly / the senior population', 'the elderly', 'the senior population'],
];

for (const [answer, formA, formB] of MULTI) {
  assert.equal(phraseIsCorrect(formA, answer), true, `「${formA}」应被「${answer}」接受`);
  assert.equal(phraseIsCorrect(formB, answer), true, `「${formB}」应被「${answer}」接受`);
  // 大小写/首尾空格/连字符都不应影响
  assert.equal(phraseIsCorrect('  ' + formB.toUpperCase() + '  ', answer), true, `大小写应忽略: ${answer}`);
  // 照题目原样打出来也算对（不惩罚老习惯）
  assert.equal(phraseIsCorrect(answer, answer), true, `原样应算对: ${answer}`);
  // 无关答案必须判错，不能因为放宽就把错答案放过
  assert.equal(phraseIsCorrect('completely unrelated phrase', answer), false, `无关答案应判错: ${answer}`);
  assert.equal(phraseIsCorrect('', answer), false);
  assert.equal(phraseIsCorrect('   ', answer), false);
  // 至少拆出两条不同的写法，否则不算生效
  assert.ok(phraseAcceptList(answer).length >= 2, `应拆出多条写法: ${answer}`);
  assert.equal(phraseMatchesAny(formA, answer), true, 'phraseMatchesAny 应与 phraseIsCorrect 一致');
}

// ── 不带 `/` 的普通答案必须原样生效（不能被放宽误伤） ──────
assert.equal(phraseIsCorrect('a barrage of problems', 'a barrage of problems'), true);
assert.equal(phraseIsCorrect('a barrage of problem', 'a barrage of problems'), false);
assert.equal(phraseIsCorrect('well known fact', 'a well-known fact'), false, '少冠词应判错');
assert.equal(phraseIsCorrect('a well known fact', 'a well-known fact'), true, '连字符按空格处理');
assert.equal(phraseIsCorrect('a long term plan', 'a long-term plan'), true, '连字符按空格处理');
assert.deepEqual(phraseAcceptList('a barrage of problems').length, 1, '无 `/` 时只有一条写法');
assert.equal(phraseMatchesAny('a barrage of problems', 'a barrage of problems'), true);

// ── 括号内的补充说明可省 ────────────────────────────────
assert.equal(
  phraseIsCorrect('be juxtaposed to the left of the gym',
    'be juxtaposed to the left of the gym (not touching)'),
  true, '括号内容可省略');

// ── 主答案 / 展示 / 词集合 ──────────────────────────────
assert.equal(phrasePrimaryAnswer('climb steadily/solidly'), 'climb steadily');
assert.equal(phrasePrimaryAnswer('a barrage of problems'), 'a barrage of problems');
assert.equal(phraseDisplayAnswer('climb steadily/solidly'), 'climb steadily 或 climb solidly');
assert.equal(phraseDisplayAnswer('a barrage of problems'), 'a barrage of problems');

const sets = phraseAcceptedWordSets('curb crime / deter crime');
assert.equal(sets.length, 2);
assert.deepEqual(sets[0], ['crime', 'curb']);
assert.deepEqual(sets[1], ['crime', 'deter']);

// 选词题的词块只按主答案出，不能出现 `/`
for (const [answer] of MULTI) {
  for (const w of phrasePrimaryAnswer(answer).split(/\s+/)) {
    assert.equal(w.includes('/'), false, `主答案拆出的词不应含 /：${answer} → ${w}`);
  }
}

console.log('test_phrase_multi_answer.js ok');
