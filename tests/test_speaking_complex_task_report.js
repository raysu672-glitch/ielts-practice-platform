/**
 * 口语复合句任务进度：三步完成句数 → scope_done / 满额打勾。
 * 与 complex-sentences.html 内 count/report 口径一致（纯逻辑抽测）。
 */
function comboProgress(map, key) {
  const c = map[key] || {};
  const a = !!c.a;
  const sh = !!c.sh;
  const sp = !!c.sp;
  return { a, sh, sp, done: a && sh && sp };
}

function countDone(map, pid, total) {
  let done = 0;
  for (let i = 0; i < total; i++) {
    if (comboProgress(map, pid + '_' + i).done) done++;
  }
  return done;
}

function shouldComplete(done, total) {
  return total > 0 && done >= total;
}

let failed = 0;
function assert(cond, msg) {
  if (!cond) {
    failed++;
    console.error('FAIL:', msg);
  }
}

const map = {
  p1_0: { a: true, sh: true, sp: true },
  p1_1: { a: true, sh: true, sp: true },
  p1_2: { a: true, sh: false, sp: false },
  p1_3: { a: true, sh: true, sp: true }
};
assert(countDone(map, 'p1', 10) === 3, 'three fully done sentences');
assert(!shouldComplete(3, 10), '3/10 not complete');
for (let i = 0; i < 10; i++) {
  map['p1_' + i] = { a: true, sh: true, sp: true };
}
assert(countDone(map, 'p1', 10) === 10, '10/10 done');
assert(shouldComplete(10, 10), '10/10 should complete');
assert(!shouldComplete(0, 0), 'empty total never completes');

if (failed) {
  console.error(failed + ' failed');
  process.exit(1);
}
console.log('test_speaking_complex_task_report.js ok');
