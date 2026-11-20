/**
 * 作文批改训练判分：多词短语 / 少虚词 / 坏 AI 检查点过滤。
 */
const assert = require('node:assert/strict');
const score = require('../sources/xiezuopigai/practice_score.js');

function cp(partial) {
  return Object.assign({
    highlight: '',
    answer: '',
    rawCorrected: '',
    originalSentence: '',
    baseText: ''
  }, partial);
}

// ── 应改成局部短语：学生只交关键子短语应通过 ──────────────
{
  const checkpoint = cp({
    highlight: 'the main reason of',
    originalSentence: 'The main reason of this change is clear.',
    baseText: 'The main reason of this change is clear.',
    rawCorrected: 'The main reason for this change is clear.',
    answer: 'The main reason for this change is clear.'
  });
  assert.equal(score.getExpectedLocalFix(checkpoint).toLowerCase(), 'the main reason for');
  assert.equal(score.isAnswerCorrect('reason for', checkpoint), true, 'reason for 应判对');
  assert.equal(score.isAnswerCorrect('the main reason for', checkpoint), true);
  assert.equal(score.isAnswerCorrect('of', checkpoint), false, '只交原错词应判错');
}

{
  const checkpoint = cp({
    highlight: 'in low prices',
    originalSentence: 'Goods are available in low prices.',
    baseText: 'Goods are available in low prices.',
    rawCorrected: 'Goods are available at low prices.',
    answer: 'Goods are available at low prices.'
  });
  assert.equal(score.isAnswerCorrect('at low prices', checkpoint), true);
  assert.equal(score.isAnswerCorrect('at low', checkpoint), true, 'at low 子短语应判对');
  assert.equal(score.isAnswerCorrect('at', checkpoint), true, '只改关键介词 at 应判对');
  assert.equal(score.isAnswerCorrect('in', checkpoint), false);
}

{
  const checkpoint = cp({
    highlight: 'experience it',
    originalSentence: 'Students should experience it themselves.',
    baseText: 'Students should experience it themselves.',
    rawCorrected: 'Students should experience it in person themselves.',
    answer: 'Students should experience it in person themselves.'
  });
  // 局部修正可能是 "experience it in person"
  const local = score.getExpectedLocalFix(checkpoint).toLowerCase();
  assert.ok(local.includes('in person') || local.includes('experience'), '应抽出含 in person 的局部修正: ' + local);
  assert.equal(score.isAnswerCorrect('experience in person', checkpoint), true, '少写虚词 it 应判对');
  assert.equal(score.isAnswerCorrect('in person', checkpoint), true, '只交新增短语应判对');
}

{
  const checkpoint = cp({
    highlight: "growth of foods' costs",
    originalSentence: "There is growth of foods' costs.",
    baseText: "There is growth of foods' costs.",
    rawCorrected: 'There is a growth in food costs.',
    answer: 'There is a growth in food costs.'
  });
  assert.equal(score.isAnswerCorrect('a growth in food costs', checkpoint), true);
  assert.equal(score.isAnswerCorrect('growth in food costs', checkpoint), true, '少冠词 a 应判对');
}

{
  const checkpoint = cp({
    highlight: 'except for',
    originalSentence: 'All students except for John passed.',
    baseText: 'All students except for John passed.',
    rawCorrected: 'All students except John passed.',
    answer: 'All students except John passed.'
  });
  assert.equal(score.isAnswerCorrect('except', checkpoint), true);
  assert.equal(score.isAnswerCorrect('except for', checkpoint), false);
}

// 经典单字改动仍可用
{
  const checkpoint = cp({
    highlight: 'have always been',
    originalSentence: 'This have always been true.',
    baseText: 'This have always been true.',
    rawCorrected: 'This has always been true.',
    answer: 'This has always been true.'
  });
  assert.equal(score.isAnswerCorrect('has', checkpoint), true);
  assert.equal(score.isAnswerCorrect('has always been', checkpoint), true);
  assert.equal(score.isAnswerCorrect('have', checkpoint), false);
}

// 仅加逗号（Sheldon 第五句卡点）：so they → , so they
{
  const checkpoint = cp({
    highlight: 'so they dare not',
    originalSentence:
      'Based on this situation, students lack of relevant theoretical knowledge so they dare not try managing their money.',
    baseText:
      'Based on this situation, students lack relevant theoretical knowledge so they dare not try managing their money.',
    rawCorrected:
      'Based on this situation, students lack of relevant theoretical knowledge, so they dare not try managing their money.',
    answer:
      'Based on this situation, students lack of relevant theoretical knowledge, so they dare not try managing their money.'
  });
  assert.equal(
    score.getExpectedLocalFix(checkpoint).replace(/\s+/g, ' ').trim(),
    ', so they dare not'
  );
  assert.equal(score.isAnswerCorrect(', so they dare not', checkpoint), true);
  assert.equal(score.isAnswerCorrect(', so they dare not ', checkpoint), true);
  const progressive = score.applyFixToBase(checkpoint.baseText, checkpoint);
  assert.equal(
    progressive.includes('lack relevant'),
    true,
    '递进叠标点时不得回退 lack→lack of'
  );
  assert.equal(progressive.includes(', so they dare not'), true);
  assert.equal(progressive.includes('knowledge ,'), false, '逗号前不应残留空格');
  assert.equal(progressive.includes('knowledge, so'), true);
}

// ── 坏 AI 检查点应过滤 ──────────────────────────────────
assert.equal(score.isUsableCheckpoint({ highlight: ',', answer: 'x', originalSentence: 'Hi,' }), false);
assert.equal(score.isUsableCheckpoint({ highlight: '...', answer: 'x' }), false);
assert.equal(score.isUsableCheckpoint({ highlight: '', answer: 'ok' }), false);
assert.equal(score.isUsableCheckpoint({
  highlight: 'one of the appropriate',
  answer: 'One of the appropriates ways is clear.',
  originalSentence: 'One of the appropriate ways is clear.',
  rawCorrected: 'One of the appropriates ways is clear.'
}), true, '含字母的 AI 点仍保留（由判分处理）');
assert.equal(score.isUsableCheckpoint({
  highlight: 'good idea',
  answer: 'This is a good idea.',
  originalSentence: 'This is a good idea.',
  rawCorrected: 'This is a good idea.'
}), false, '修正与原文相同应丢弃');

console.log('test_writing_practice_score.js OK');
