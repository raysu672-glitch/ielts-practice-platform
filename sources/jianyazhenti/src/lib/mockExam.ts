import { audioSrc, loadAnswerKey, loadCatalog, loadManifest, loadPart, saveAnswers } from './data'
import { gradePart, padItemsToPaper, recountGrade, type GradeItem, type GradeResult } from './grade'
import { PART_MODULE_NAMES, moduleTypeForPart } from './partModules'
import { attachQuestionTypes, buildTypeStats, type TypeStat } from './questionTypes'
import {
  loadAllDoneKeys,
  paperKey,
  type PaperRef,
} from './randomTest'
import { saveStoredResult } from './results'
import { isAuthError, loadStudentProgress, postStudentJson } from './studentApi'
import type { PartData, Subject } from '../types'

export const MOCK_BOOK_MIN = 7
export const MOCK_BOOK_MAX = 21
export const READING_LIMIT_SEC = 60 * 60
export const LISTENING_INTRO_SEC = 15
export const LISTENING_GAP_SEC = 30
export const LISTENING_END_SEC = 120

export type MockPaper = PaperRef & { reused: boolean }

export type MockDurations = {
  readingLimit: number
  intro: number
  gap: number
  end: number
}

export type ListeningPhase =
  | { kind: 'idle' }
  | { kind: 'intro'; remaining: number }
  | { kind: 'play'; part: number }
  | { kind: 'gap'; nextPart: number; remaining: number }
  | { kind: 'ending'; remaining: number }
  | { kind: 'done' }

export type LoadedMockPart = {
  paper: MockPaper
  part: PartData
  audioUrl: string | null
}

export type MockPartScore = {
  paper: MockPaper
  graded: GradeResult
  answers: Record<string, string>
  items: GradeItem[]
  pct: number
  durationSeconds: number
  typeStats: Record<string, TypeStat>
}

export type MockPartResult = {
  bookId: number
  subject: Subject
  sId: number
  sPart: number
  label: string
  correct: number
  total: number
  pct: number
  durationSeconds: number
  typeStats: Record<string, TypeStat>
  answers: Record<string, string>
  items: GradeItem[]
}

export type MockSetRecord = {
  id: string
  subject: Subject
  submittedAt: string
  durationSeconds: number
  correct: number
  total: number
  pct: number
  typeStats: Record<string, TypeStat>
  parts: MockPartResult[]
}

const MOCK_SET_KEY = 'mock-exam-sets:v1'

export function mockDurations(fast: boolean): MockDurations {
  if (fast) {
    return { readingLimit: 45, intro: 5, gap: 5, end: 8 }
  }
  return {
    readingLimit: READING_LIMIT_SEC,
    intro: LISTENING_INTRO_SEC,
    gap: LISTENING_GAP_SEC,
    end: LISTENING_END_SEC,
  }
}

export function formatClock(totalSeconds: number) {
  const s = Math.max(0, Math.floor(totalSeconds))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
  }
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}

export function listeningStatusText(phase: ListeningPhase) {
  if (phase.kind === 'idle') return '点击开始考试后计时播放'
  if (phase.kind === 'intro') return `开考空白 ${phase.remaining} 秒后播放 Part 1`
  if (phase.kind === 'play') return `正在播放 Part ${phase.part}`
  if (phase.kind === 'gap') return `${phase.remaining} 秒后播放 Part ${phase.nextPart}`
  if (phase.kind === 'ending') return `Part 4 已结束，${phase.remaining} 秒后自动交卷`
  return '已交卷'
}

export async function pickMockSet(subject: Subject): Promise<{
  papers: MockPaper[]
  reusedCount: number
}> {
  const partNums = subject === 'reading' ? [1, 2, 3] : [1, 2, 3, 4]
  const [done, books] = await Promise.all([loadAllDoneKeys(), loadCatalog()])
  const inRange = books.filter(
    (book) => book.bookId >= MOCK_BOOK_MIN && book.bookId <= MOCK_BOOK_MAX,
  )
  const pools = new Map<number, PaperRef[]>()
  for (const sPart of partNums) pools.set(sPart, [])

  await Promise.all(
    inRange.map(async (book) => {
      try {
        const manifest = await loadManifest(book.bookId)
        for (const p of manifest.parts[subject] || []) {
          if (p.error || !pools.has(p.sPart)) continue
          pools.get(p.sPart)!.push({
            bookId: book.bookId,
            subject,
            sId: p.sId,
            sPart: p.sPart,
            label: p.sName,
          })
        }
      } catch {
        /* 单册缺失时跳过 */
      }
    }),
  )

  const used = new Set<string>()
  const papers: MockPaper[] = []
  for (const sPart of partNums) {
    const pool = (pools.get(sPart) || []).filter(
      (p) => !used.has(paperKey(p.bookId, p.subject, p.sId)),
    )
    if (!pool.length) {
      throw new Error(`C7–C21 没有可用的${subject === 'reading' ? '阅读' : '听力'} Part ${sPart}`)
    }
    const unused = pool.filter((p) => !done.has(paperKey(p.bookId, p.subject, p.sId)))
    const source = unused.length ? unused : pool
    const pick = source[Math.floor(Math.random() * source.length)]
    used.add(paperKey(pick.bookId, pick.subject, pick.sId))
    papers.push({ ...pick, reused: unused.length === 0 })
  }
  return { papers, reusedCount: papers.filter((p) => p.reused).length }
}

export async function loadMockParts(papers: MockPaper[]): Promise<LoadedMockPart[]> {
  const loaded = await Promise.all(
    papers.map(async (paper) => {
      const part = await loadPart(paper.subject, paper.sId, paper.bookId)
      return {
        paper,
        part,
        audioUrl: audioSrc(part, paper.bookId),
      }
    }),
  )
  return loaded.sort((a, b) => a.part.sPart - b.part.sPart)
}

function paperDetails(
  part: PartData,
  bookId: number,
  graded: GradeResult,
  answers: Record<string, string>,
  durationSeconds: number,
) {
  const items = attachQuestionTypes(part, padItemsToPaper(part, graded.items, answers))
  const counts = recountGrade(items)
  const typeStats = buildTypeStats(items)
  const pct = counts.total ? Math.round((counts.correct / counts.total) * 100) : 0
  return {
    items,
    typeStats,
    pct,
    correct: counts.correct,
    total: counts.total,
    details: [
      {
        kind: 'jianya_paper',
        source: 'mock',
        bookId,
        subject: part.subject,
        sId: part.sId,
        sPart: part.sPart,
        label: part.sName,
        pct,
        correct: counts.correct,
        total: counts.total,
        durationSeconds,
        answers,
        items,
        typeStats,
      },
    ],
  }
}

export async function gradeMockPart(
  loaded: LoadedMockPart,
  answers: Record<string, string>,
  durationSeconds = 0,
): Promise<MockPartScore> {
  const key = await loadAnswerKey(loaded.paper.subject, loaded.paper.sId, loaded.paper.bookId)
  const graded = gradePart(loaded.part, answers, key)
  const items = attachQuestionTypes(loaded.part, graded.items)
  const pct = graded.total ? Math.round((graded.correct / graded.total) * 100) : 0
  return {
    paper: loaded.paper,
    graded,
    answers,
    items,
    pct,
    durationSeconds,
    typeStats: buildTypeStats(items),
  }
}

function mockSetPayload(record: MockSetRecord) {
  return {
    module_type: record.subject === 'reading' ? 'mock_reading' : 'mock_listening',
    module_name: record.subject === 'reading' ? '阅读模拟考' : '听力模拟考',
    test_type: 'mock_exam',
    score: record.pct,
    correct_count: record.correct,
    total_count: record.total,
    duration_seconds: record.durationSeconds,
    started_at: record.submittedAt,
    ended_at: record.submittedAt,
    details: [
      {
        kind: 'jianya_mock',
        source: 'mock',
        subject: record.subject,
        pct: record.pct,
        correct: record.correct,
        total: record.total,
        durationSeconds: record.durationSeconds,
        typeStats: record.typeStats,
        parts: record.parts,
      },
    ],
  }
}

export async function persistMockPart(score: MockPartScore, startedAt: number, loaded: LoadedMockPart) {
  saveAnswers(score.paper.subject, score.paper.sId, score.answers, score.paper.bookId)
  const moduleType = moduleTypeForPart(loaded.part.subject, loaded.part.sPart)
  if (!moduleType) throw new Error('无法识别该 Part，成绩未能写入服务器')
  const packed = paperDetails(
    loaded.part,
    score.paper.bookId,
    score.graded,
    score.answers,
    score.durationSeconds,
  )
  await postStudentJson('/api/student/test-records', {
    module_type: moduleType,
    module_name: `${PART_MODULE_NAMES[moduleType]}模拟考`,
    test_type: 'mock_exam',
    score: packed.correct,
    correct_count: packed.correct,
    total_count: packed.total,
    duration_seconds: score.durationSeconds,
    started_at: new Date(startedAt).toISOString(),
    details: packed.details,
  })
  saveStoredResult(score.paper.subject, loaded.part, score.graded, score.paper.bookId)
}

function mergeTypeStats(rows: Record<string, TypeStat>[]): Record<string, TypeStat> {
  const stats: Record<string, TypeStat> = {}
  for (const row of rows) {
    for (const [name, item] of Object.entries(row || {})) {
      if (!stats[name]) stats[name] = { correct: 0, total: 0, wrong: 0, blank: 0 }
      stats[name].correct += item.correct || 0
      stats[name].total += item.total || 0
      stats[name].wrong += item.wrong || 0
      stats[name].blank += item.blank || 0
    }
  }
  return stats
}

export function mockSetFromScores(
  subject: Subject,
  scores: MockPartScore[],
  startedAt: number,
): MockSetRecord {
  const parts: MockPartResult[] = scores.map((score) => ({
    bookId: score.paper.bookId,
    subject: score.paper.subject,
    sId: score.paper.sId,
    sPart: score.paper.sPart,
    label: score.paper.label,
    correct: score.graded.correct,
    total: score.graded.total,
    pct: score.pct,
    durationSeconds: score.durationSeconds,
    typeStats: score.typeStats,
    answers: score.answers,
    items: score.items,
  }))
  const correct = parts.reduce((n, p) => n + p.correct, 0)
  const total = parts.reduce((n, p) => n + p.total, 0)
  return {
    id: `local-${startedAt}`,
    subject,
    submittedAt: new Date().toISOString(),
    durationSeconds: Math.max(0, Math.round((Date.now() - startedAt) / 1000)),
    correct,
    total,
    pct: total ? Math.round((correct / total) * 100) : 0,
    typeStats: mergeTypeStats(parts.map((p) => p.typeStats)),
    parts,
  }
}

function readLocalMockSets(): MockSetRecord[] {
  try {
    const raw = localStorage.getItem(MOCK_SET_KEY)
    if (!raw) return []
    const rows = JSON.parse(raw) as MockSetRecord[]
    return Array.isArray(rows) ? rows : []
  } catch {
    return []
  }
}

function sameMockSet(a: MockSetRecord, b: MockSetRecord) {
  if (a.subject !== b.subject || a.parts.length !== b.parts.length) return false
  const samePapers = a.parts.every(
    (part, i) => part.sId === b.parts[i]?.sId && part.bookId === b.parts[i]?.bookId,
  )
  const t1 = Date.parse(a.submittedAt) || 0
  const t2 = Date.parse(b.submittedAt) || 0
  return samePapers && Math.abs(t1 - t2) < 120000
}

export async function persistMockSet(record: MockSetRecord) {
  const saved = await postStudentJson<{ id?: number }>('/api/student/test-records', mockSetPayload(record))
  if (saved?.id) record.id = `server-${saved.id}`
  return record
}

function recordFromDetails(rec: Record<string, unknown>): MockSetRecord | null {
  const details = rec.details
  const items = Array.isArray(details) ? details : details ? [details] : []
  for (const raw of items) {
    if (!raw || typeof raw !== 'object') continue
    const row = raw as Record<string, unknown>
    if (row.kind !== 'jianya_mock') continue
    const parts = Array.isArray(row.parts) ? (row.parts as MockPartResult[]) : []
    if (!parts.length) continue
    const subject = (row.subject === 'listening' ? 'listening' : 'reading') as Subject
    const correct = Number(rec.correct_count || row.correct || 0)
    const total = Number(rec.total_count || row.total || 0)
    return {
      id: `server-${rec.id || rec.created_at}`,
      subject,
      submittedAt: String(rec.created_at || rec.ended_at || ''),
      durationSeconds: Number(rec.duration_seconds || row.durationSeconds || 0),
      correct,
      total,
      pct: total ? Math.round((correct / total) * 100) : Number(row.pct || rec.score || 0),
      typeStats: (row.typeStats as Record<string, TypeStat>) || mergeTypeStats(parts.map((p) => p.typeStats || {})),
      parts: parts.map((p) => ({
        ...p,
        durationSeconds: Number(p.durationSeconds || 0),
        typeStats: p.typeStats || {},
        answers: p.answers || {},
        items: p.items || [],
      })),
    }
  }
  return null
}

export async function loadMockSets(): Promise<MockSetRecord[]> {
  const progress = await loadStudentProgress()
  const out: MockSetRecord[] = []
  for (const rec of progress.test_records || []) {
    const row = recordFromDetails(rec)
    if (row) out.push(row)
  }
  out.sort((a, b) => String(b.submittedAt).localeCompare(String(a.submittedAt)))
  return out
}

export async function migrateLocalMockSets() {
  const local = readLocalMockSets()
  if (!local.length) return
  let server: MockSetRecord[] = []
  try {
    server = await loadMockSets()
  } catch (err) {
    if (isAuthError(err)) return
    throw err
  }
  let failed = false
  for (const row of local) {
    if (server.some((item) => sameMockSet(item, row))) continue
    try {
      server.push(await persistMockSet(row))
    } catch {
      failed = true
    }
  }
  if (!failed) localStorage.removeItem(MOCK_SET_KEY)
}

export function formatTypeStats(stats: Record<string, TypeStat> | undefined) {
  const entries = Object.entries(stats || {}).filter(([, row]) => (row?.total || 0) > 0)
  if (!entries.length) return '—'
  return entries
    .map(([name, row]) => `${name} ${row.correct}/${row.total}（${row.total ? Math.round((row.correct / row.total) * 100) : 0}%）`)
    .join(' · ')
}

export function paperShortLabel(paper: { bookId: number; sPart: number }) {
  return `C${paper.bookId} Part ${paper.sPart}`
}
