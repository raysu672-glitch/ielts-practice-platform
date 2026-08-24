const assert = require('node:assert/strict');
const utils = require('../sources/tinglidanciceshi/tracking_utils.js');

const sessions = [
    { session_kind: 'study', duration_seconds: 120 },
    { session_kind: 'test', duration_seconds: 300 },
    { duration_seconds: 30 },
];

assert.deepEqual(utils.filterStudySessions(sessions), [sessions[0], sessions[2]]);
assert.equal(utils.sumDuration(utils.filterStudySessions(sessions)), 150);
assert.equal(utils.getTestTypeLabel('module_test'), '模块测试');
assert.equal(utils.getTestTypeLabel('wrong_words'), '错题测试');
assert.deepEqual(utils.parseDetails('[{"word":"apple","isCorrect":false}]'), [
    { word: 'apple', isCorrect: false },
]);
assert.deepEqual(utils.getWrongWordDetails([
    { word: 'apple', isCorrect: false },
    { original: 'sentence', isCorrect: false },
    { word: 'pear', isCorrect: true },
]), [{ word: 'apple', isCorrect: false }]);

const practiceSessions = [
    { session_kind: 'study', module_type: 'dictation', duration_seconds: 100, created_at: '2026-08-21T02:00:00.000Z' },
    { session_kind: 'test', module_type: 'dictation', duration_seconds: 50, created_at: '2026-08-21T03:00:00.000Z' },
    { session_kind: 'study', module_type: 'speaking', duration_seconds: 80, created_at: '2026-08-22T02:00:00.000Z' },
];
const practiceRecords = [
    { module_type: 'dictation', duration_seconds: 200, created_at: '2026-08-21T04:00:00.000Z' },
    { module_type: 'speaking', duration_seconds: 999, created_at: '2026-08-22T04:00:00.000Z' },
];
assert.equal(utils.sumPracticeSeconds(practiceSessions, practiceRecords), 430);
assert.equal(utils.sumPracticeSeconds(practiceSessions, practiceRecords, { moduleId: 'dictation' }), 350);
assert.equal(utils.sumPracticeSeconds(practiceSessions, practiceRecords, { moduleId: 'speaking' }), 80);

let fakeNow = 0;
const clock = utils.createIdleClock(5 * 60 * 1000, function() { return fakeNow; });
clock.touch();
fakeNow = 60 * 1000;
assert.equal(clock.elapsedSeconds(), 60);
fakeNow = 6 * 60 * 1000;
assert.equal(clock.elapsedSeconds(), 5 * 60);
fakeNow = 10 * 60 * 1000;
assert.equal(clock.elapsedSeconds(), 5 * 60);
clock.touch();
fakeNow = 10 * 60 * 1000 + 30 * 1000;
assert.equal(clock.elapsedSeconds(), 5 * 60 + 30);

const daily = utils.buildDailyPracticeRows(practiceSessions, practiceRecords, {
    dateKey: function(iso) { return String(iso).slice(0, 10); }
});
assert.equal(daily.length, 2);
assert.equal(daily[0].date, '2026-08-22');
assert.equal(daily[0].totalSeconds, 80);
assert.equal(daily[1].date, '2026-08-21');
assert.equal(daily[1].totalSeconds, 350);

assert.equal(utils.getChinaYmd('2026-08-21T15:59:59.000Z'), '2026-08-21');
assert.equal(utils.getChinaYmd('2026-08-21T16:00:00.000Z'), '2026-08-22');
assert.equal(utils.shiftYmd('2026-08-22', -1), '2026-08-21');
assert.deepEqual(utils.chinaWeekBounds('2026-08-22'), { startYmd: '2026-08-17', endYmd: '2026-08-23' });
assert.deepEqual(utils.chinaWeekBounds('2026-08-23'), { startYmd: '2026-08-17', endYmd: '2026-08-23' });
assert.deepEqual(utils.chinaMonthBounds('2026-08-22'), { startYmd: '2026-08-01', endYmd: '2026-08-31' });
assert.deepEqual(utils.chinaMonthBounds('2026-02-10'), { startYmd: '2026-02-01', endYmd: '2026-02-28' });
assert.deepEqual(utils.resolveActiveRange('yesterday', '', '2026-08-22'), { startYmd: '2026-08-21', endYmd: '2026-08-21' });
assert.deepEqual(utils.resolveActiveRange('week', '', '2026-08-22'), { startYmd: '2026-08-17', endYmd: '2026-08-23' });
assert.deepEqual(utils.resolveActiveRange('month', '', '2026-08-22'), { startYmd: '2026-08-01', endYmd: '2026-08-31' });
assert.deepEqual(utils.resolveActiveRange('day', '2026-08-10', '2026-08-22'), { startYmd: '2026-08-10', endYmd: '2026-08-10' });
assert.deepEqual(utils.resolveActiveRange('range', '', '2026-08-22', '2026-08-10', '2026-08-12'), { startYmd: '2026-08-10', endYmd: '2026-08-12' });
assert.deepEqual(utils.resolveActiveRange('range', '', '2026-08-22', '2026-08-12', '2026-08-10'), { startYmd: '2026-08-10', endYmd: '2026-08-12' });

const activeStudents = [
    { student_id: '2025001', name: '甲' },
    { student_id: '2025002', name: '乙' },
    { student_id: '2025003', name: '丙' },
];
const activeSessions = [
    { student_id: '2025001', session_kind: 'study', module_type: 'dictation', duration_seconds: 100, created_at: '2026-08-21T02:00:00.000Z' },
    { student_id: '2025002', session_kind: 'study', module_type: 'dictation', duration_seconds: 40, created_at: '2026-08-22T02:00:00.000Z' },
    { student_id: '2025002', session_kind: 'test', module_type: 'dictation', duration_seconds: 20, created_at: '2026-08-22T03:00:00.000Z' },
];
const activeRecords = [
    { student_id: '2025001', module_type: 'dictation', duration_seconds: 50, created_at: '2026-08-21T04:00:00.000Z' },
    { student_id: '2025002', module_type: 'speaking', duration_seconds: 999, created_at: '2026-08-22T04:00:00.000Z' },
];
const yesterdayActive = utils.buildActiveStudentRows(activeStudents, activeSessions, activeRecords, {
    startYmd: '2026-08-21',
    endYmd: '2026-08-21',
    sortDir: 'desc'
});
assert.equal(yesterdayActive.length, 3);
assert.equal(yesterdayActive[0].student_id, '2025001');
assert.equal(yesterdayActive[0].seconds, 150);
assert.equal(yesterdayActive[1].seconds, 0);
assert.equal(yesterdayActive[2].seconds, 0);

const todayActive = utils.buildActiveStudentRows(activeStudents, activeSessions, activeRecords, {
    startYmd: '2026-08-22',
    endYmd: '2026-08-22',
    sortDir: 'desc'
});
assert.equal(todayActive.length, 3);
assert.equal(todayActive[0].student_id, '2025002');
assert.equal(todayActive[0].seconds, 60);
assert.equal(todayActive[1].seconds, 0);

const weekActive = utils.buildActiveStudentRows(activeStudents, activeSessions, activeRecords, {
    startYmd: '2026-08-17',
    endYmd: '2026-08-23',
    sortDir: 'asc'
});
assert.equal(weekActive.length, 3);
assert.equal(weekActive[0].seconds, 0);
assert.equal(weekActive[1].student_id, '2025002');
assert.equal(weekActive[1].seconds, 60);
assert.equal(weekActive[2].student_id, '2025001');
assert.equal(weekActive[2].seconds, 150);

console.log('tracking utils tests passed');
