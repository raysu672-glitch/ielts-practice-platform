/**
 * 词伙「选词题」判分对称性回归测试。
 *
 * 背景（线上真实故障）：学生把正确词块全点对了，却被判错。
 * 原因是判分两侧用了两套归一化：
 *   - 学生侧 game.js 的本地 normalize：连字符**直接删除** → `selffulfillment`
 *   - 标准答案侧 phraseAcceptedWordSets → phraseNormalize：连字符**变空格** → `self fulfillment`
 * 两者永不相等，导致任何带连字符/撇号的词伙都「永远答不对」。
 *
 * 本测试锁两件事：
 *   1) 行为：按真实判分表达式，点全正确词块必须判对；点错必须判错。
 *   2) 接线：两个判分调用点必须都走共享的 phraseNormalize，防止再次各写一套。
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.join(__dirname, '..');
const PA = require(path.join(ROOT, 'sources', 'shared', 'phrase_answer.js'));
const phraseNormalize = PA.phraseNormalize;

/* ── 1) 接线检查：两个调用点必须用共享的 phraseNormalize ── */
const callSites = [
  ['sources/xiezuocihuo/game.js', 'var userSorted = selectedWords.map'],
  ['sources/tinglidanciceshi/js/student.js', 'const userSorted = phraseState.selectedWords.map'],
];
const extracted = [];
for (const [rel, marker] of callSites) {
  const src = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const line = src.split(/\r?\n/).find((l) => l.includes(marker) && l.includes('.map(function'));
  assert.ok(line, `${rel} 找不到判分行（marker=${marker}）`);
  assert.ok(
    /return\s+phraseNormalize\s*\(\s*\w+\.word\s*\)/.test(line),
    `${rel} 的判分必须用 phraseNormalize(...word) 归一化，实际是：${line.trim()}`,
  );
  assert.ok(
    !/return\s+\w+\.word\.toLowerCase\(\)/.test(line) && !/return\s+normalize\(/.test(line),
    `${rel} 又出现了本地归一化（会造成两侧不一致）：${line.trim()}`,
  );
  const m = line.match(/\.map\(function\s*\(\s*(\w+)\s*\)\s*\{\s*return\s+(.+?);\s*\}\)/);
  assert.ok(m, `${rel} 判分表达式解析失败`);
  extracted.push({ rel, argName: m[1], expr: m[2] });
}

// 用抽取出的真实表达式判分
function judge(site, words) {
  const fn = new Function('phraseNormalize', site.argName, `return (${site.expr});`);
  return words
    .map((w) => fn(phraseNormalize, { word: w }))
    .sort()
    .join(' ');
}

/* ── 2) 行为检查：全题库「点全正确词块」必须判对 ── */
const banks = [
  'sources/xiezuocihuo/game.js',
  'sources/xiezuocihuoceshi/index.html',
  'sources/tinglidanciceshi/js/modules.js',
];
const items = [];
const pairRe = /\{\s*zh:\s*"(?:[^"\\]|\\.)*"\s*,\s*en:\s*"((?:[^"\\]|\\.)*)"\s*\}/g;
for (const rel of banks) {
  const f = path.join(ROOT, rel);
  if (!fs.existsSync(f)) continue;
  const src = fs.readFileSync(f, 'utf8');
  let m;
  while ((m = pairRe.exec(src))) items.push({ en: m[1], src: rel });
}
assert.ok(items.length >= 50, `词伙题库解析数量异常：${items.length}`);

const chipsOf = (en) => PA.phrasePrimaryAnswer(en).split(/\s+/).filter(Boolean);
const acceptedOf = (en) => PA.phraseAcceptedWordSets(en).map((ws) => ws.join(' '));

let checked = 0;
for (const site of extracted) {
  for (const it of items) {
    const hit = acceptedOf(it.en).some((s) => s === judge(site, chipsOf(it.en)));
    assert.ok(hit, `点全正确词块却被判错：${it.en}  [${site.rel}, 来自 ${it.src}]`);
    checked++;
  }
}
assert.ok(checked > 0);

/* ── 3) 必须真的带连字符/撇号才覆盖得到这个 bug ── */
const tricky = items.filter((it) => /[-']/.test(it.en));
assert.ok(
  tricky.some((it) => it.en.includes('self-fulfillment')),
  '题库里应包含 a sense of self-fulfillment（线上报障题）',
);
assert.ok(tricky.length >= 2, `带连字符/撇号的词伙应有 >=2 条，实际 ${tricky.length}`);

/* ── 4) 错答必须仍判错（防止用「放水」掩盖） ── */
const site0 = extracted[0];
assert.equal(acceptedOf('a sense of self-fulfillment').some((s) => s === judge(site0, ['a', 'sense', 'self-fulfillment'])), false, '漏选 of 应判错');
assert.equal(acceptedOf('a sense of self-fulfillment').some((s) => s === judge(site0, ['a', 'sense', 'of', 'self-fulfillment'])), true, '全选应判对');
assert.equal(acceptedOf('a well-known fact').some((s) => s === judge(site0, ['a', 'well-known', 'fact'])), true, '全选应判对');
assert.equal(acceptedOf('a well-known fact').some((s) => s === judge(site0, ['a', 'well-known', 'fact', 'of'])), false, '多选应判错');

/* ── 5) phraseNormalize 语义 ── */
assert.equal(phraseNormalize('self-fulfillment'), 'self fulfillment');
assert.equal(phraseNormalize("one's"), 'ones');
assert.equal(phraseNormalize('  Climb  steadily/solidly '), 'climb steadily solidly');

console.log(`phrase answer tests passed（${items.length} 条题库 × ${extracted.length} 个判分点 = ${checked} 次比对）`);
