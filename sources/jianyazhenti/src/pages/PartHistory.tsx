import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { listMySubmissions } from '../lib/assignments'
import { loadAnswerKey, loadPart } from '../lib/data'
import { gradePart, padItemsToPaper } from '../lib/grade'
import { PART_MODULE_NAMES as MODULE_NAMES, moduleTypeForPart, parsePartModule } from '../lib/partModules'
import { loadLocalModuleResults } from '../lib/results'
import {
  attachQuestionTypes,
  buildTypeStats,
  hasTypeStats,
  type HistoryGradeItem,
  type TypeStat,
  typeStatsFromPart,
} from '../lib/questionTypes'
import {
  isTeacherViewingStudent,
  loadStudentProgress,
  withTeacherViewParams,
} from '../lib/studentApi'
import type { Subject } from '../types'

type AttemptKind = 'study' | 'test' | 'homework' | 'mock'

type Attempt = {
  id: string
  kind: AttemptKind
  createdAt: string
  bookId: number
  subject: Subject
  sId: number
  sPart: number
  label: string
  correct: number
  total: number
  pct: number
  typeStats: Record<string, TypeStat>
  scoredTypes: boolean
  answers: Record<string, string>
  items: HistoryGradeItem[]
}

function paperFromDetails(details: unknown) {
  const items = Array.isArray(details) ? details : details ? [details] : []
  for (const raw of items) {
    if (!raw || typeof raw !== 'object') continue
    const row = raw as Record<string, unknown>
    if (row.kind === 'jianya_paper' || row.bookId) return row
  }
  return null
}

function asTypeStats(value: unknown, items: HistoryGradeItem[]): Record<string, TypeStat> {
  if (value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length) {
    return value as Record<string, TypeStat>
  }
  const stats: Record<string, TypeStat> = {}
  for (const item of items) {
    const key = item.qType || '其他'
    if (!stats[key]) stats[key] = { correct: 0, total: 0, wrong: 0, blank: 0 }
    stats[key].total += 1
    if (item.status === 'correct') stats[key].correct += 1
    else if (item.status === 'wrong') stats[key].wrong += 1
    else stats[key].blank += 1
  }
  return stats
}

function mergeAttempts(
  moduleType: string,
  testRecords: Record<string, unknown>[],
  studySessions: Record<string, unknown>[],
): Attempt[] {
  const out: Attempt[] = []
  for (const rec of testRecords) {
    if (String(rec.module_type || '') !== moduleType) continue
    const paper = paperFromDetails(rec.details)
    if (!paper) continue
    const items = Array.isArray(paper.items) ? (paper.items as HistoryGradeItem[]) : []
    const typeStats = asTypeStats(paper.typeStats, items)
    const correct = Number(rec.correct_count || paper.correct || 0)
    const total = Number(rec.total_count || paper.total || items.length || 0)
    out.push({
      id: `test-${rec.id}`,
      kind: String(paper.source || '') === 'mock' ? 'mock' : 'test',
      createdAt: String(rec.created_at || rec.ended_at || ''),
      bookId: Number(paper.bookId),
      subject: (paper.subject as Subject) || 'reading',
      sId: Number(paper.sId),
      sPart: Number(paper.sPart || 0),
      label: String(paper.label || ''),
      correct,
      total,
      pct: total ? Math.round((correct / total) * 100) : Number(paper.pct || 0),
      typeStats,
      scoredTypes: hasTypeStats(typeStats) && items.length > 0,
      answers: (paper.answers as Record<string, string>) || {},
      items,
    })
  }
  for (const rec of studySessions) {
    if (String(rec.module_type || '') !== moduleType) continue
    const paper = paperFromDetails(rec.details)
    if (!paper) continue
    const items = Array.isArray(paper.items) ? (paper.items as HistoryGradeItem[]) : []
    const typeStats = asTypeStats(paper.typeStats, items)
    const correct = Number(rec.initial_correct || paper.correct || 0)
    const total = Number(rec.words_tested || paper.total || items.length || 0)
    const pct =
      rec.score_percent != null
        ? Math.round(Number(rec.score_percent))
        : total
          ? Math.round((correct / total) * 100)
          : Number(paper.pct || 0)
    out.push({
      id: `study-${rec.id}`,
      kind:
        String(paper.source || '') === 'homework'
          ? 'homework'
          : String(paper.source || '') === 'mock'
            ? 'mock'
            : 'study',
      createdAt: String(rec.created_at || rec.ended_at || ''),
      bookId: Number(paper.bookId),
      subject: (paper.subject as Subject) || 'reading',
      sId: Number(paper.sId),
      sPart: Number(paper.sPart || 0),
      label: String(paper.label || ''),
      correct,
      total,
      pct,
      typeStats,
      scoredTypes: hasTypeStats(typeStats) && items.length > 0,
      answers: (paper.answers as Record<string, string>) || {},
      items,
    })
  }
  out.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)))
  return out
}

function mockSetAttempts(moduleType: string, testRecords: Record<string, unknown>[]): Attempt[] {
  const out: Attempt[] = []
  for (const rec of testRecords) {
    const details = rec.details
    const items = Array.isArray(details) ? details : details ? [details] : []
    for (const raw of items) {
      if (!raw || typeof raw !== 'object') continue
      const row = raw as Record<string, unknown>
      if (row.kind !== 'jianya_mock' || !Array.isArray(row.parts)) continue
      for (const part of row.parts as Record<string, unknown>[]) {
        const sPart = Number(part.sPart || 0)
        const subject = (part.subject as Subject) || 'reading'
        if (moduleTypeForPart(subject, sPart) !== moduleType) continue
        const gradeItems = Array.isArray(part.items) ? (part.items as HistoryGradeItem[]) : []
        const typeStats = asTypeStats(part.typeStats, gradeItems)
        const correct = Number(part.correct || 0)
        const total = Number(part.total || gradeItems.length || 0)
        out.push({
          id: `mock-${rec.id}-${part.sId}`,
          kind: 'mock',
          createdAt: String(rec.created_at || rec.ended_at || ''),
          bookId: Number(part.bookId),
          subject,
          sId: Number(part.sId),
          sPart,
          label: String(part.label || ''),
          correct,
          total,
          pct: total ? Math.round((correct / total) * 100) : Number(part.pct || 0),
          typeStats,
          scoredTypes: hasTypeStats(typeStats) && gradeItems.length > 0,
          answers: (part.answers as Record<string, string>) || {},
          items: gradeItems,
        })
      }
    }
  }
  return out
}

function kindLabel(kind: AttemptKind) {
  if (kind === 'mock') return '模拟考'
  if (kind === 'test') return '测试'
  if (kind === 'homework') return '作业'
  return '学习'
}

function nearDuplicate(existing: Attempt[], next: Attempt) {
  const t = Date.parse(next.createdAt) || 0
  return existing.some((row) => {
    if (row.bookId !== next.bookId || row.sId !== next.sId || row.subject !== next.subject) return false
    const other = Date.parse(row.createdAt) || 0
    return Math.abs(other - t) < 120000
  })
}

function homeworkAttempts(moduleType: string, rows: Awaited<ReturnType<typeof listMySubmissions>>): Attempt[] {
  const out: Attempt[] = []
  for (const rec of rows) {
    const sPart = Number(rec.sPart || 0)
    if (moduleTypeForPart(rec.subject, sPart) !== moduleType) continue
    const correct = Number(rec.correct || 0)
    const total = Number(rec.total || 0)
    out.push({
      id: `hw-${rec.assignmentId}-${rec.bookId}-${rec.sId}-${rec.submittedAt}`,
      kind: 'homework',
      createdAt: String(rec.submittedAt || ''),
      bookId: Number(rec.bookId),
      subject: rec.subject,
      sId: Number(rec.sId),
      sPart,
      label: rec.assignmentTitle
        ? `${rec.assignmentTitle}${rec.label ? ' · ' + rec.label.replace(/^【听力】|【阅读】/, '') : ''}`
        : String(rec.label || ''),
      correct,
      total,
      pct: total ? Math.round((correct / total) * 100) : Number(rec.pct || 0),
      typeStats: {},
      scoredTypes: false,
      answers: rec.answers || {},
      items: [],
    })
  }
  return out
}

function localAttempts(moduleType: string): Attempt[] {
  const parsed = parsePartModule(moduleType)
  if (!parsed) return []
  return loadLocalModuleResults(parsed.subject, parsed.sPart).map((row) => ({
    id: `local-${row.bookId}-${row.subject}-${row.sId}`,
    kind: 'study' as const,
    createdAt: String(row.submittedAt || ''),
    bookId: Number(row.bookId),
    subject: row.subject,
    sId: Number(row.sId),
    sPart: Number(row.sPart),
    label: String(row.label || ''),
    correct: Number(row.correct || 0),
    total: Number(row.total || 0),
    pct: Number(row.pct || 0),
    typeStats: {},
    scoredTypes: false,
    answers: row.answers || {},
    items: [],
  }))
}

function samePaper(existing: Attempt[], next: Attempt) {
  return existing.some(
    (row) =>
      row.bookId === next.bookId &&
      row.sId === next.sId &&
      row.subject === next.subject &&
      Number(row.sPart) === Number(next.sPart),
  )
}

function mergeLocalAttempts(base: Attempt[], extra: Attempt[]) {
  const out = [...base]
  for (const row of extra) {
    if (samePaper(out, row)) continue
    out.push(row)
  }
  out.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)))
  return out
}

function mergeExtraAttempts(base: Attempt[], extra: Attempt[]) {
  const out = [...base]
  for (const row of extra) {
    if (nearDuplicate(out, row)) continue
    out.push(row)
  }
  out.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)))
  return out
}

function hasFilledAnswers(answers: Record<string, string>) {
  return Object.values(answers).some((v) => String(v || '').trim())
}

async function fillMissingTypeStats(rows: Attempt[]): Promise<Attempt[]> {
  const cache = new Map<string, Awaited<ReturnType<typeof loadPart>>>()
  const out: Attempt[] = []
  for (const row of rows) {
    if (!row.bookId || !row.sId) {
      out.push(row)
      continue
    }
    const cacheKey = `${row.bookId}:${row.subject}:${row.sId}`
    try {
      if (!cache.has(cacheKey)) {
        cache.set(cacheKey, await loadPart(row.subject, row.sId, row.bookId))
      }
      const part = cache.get(cacheKey)!
      const paperTotal = (part.questions || []).length
      const answers: Record<string, string> = { ...(row.answers || {}) }
      for (const it of row.items || []) {
        const num = String(it.number)
        if (it.user && !String(answers[num] || '').trim()) answers[num] = it.user
      }
      const incomplete = paperTotal > 0 && (row.total < paperTotal || (row.items || []).length < paperTotal)
      if (paperTotal && (incomplete || !row.scoredTypes || !hasTypeStats(row.typeStats))) {
        let items: HistoryGradeItem[]
        if ((row.items || []).length > 0) {
          items = attachQuestionTypes(part, padItemsToPaper(part, row.items, answers))
        } else if (hasFilledAnswers(answers)) {
          const key = await loadAnswerKey(row.subject, row.sId, row.bookId)
          items = attachQuestionTypes(part, gradePart(part, answers, key).items)
        } else {
          items = attachQuestionTypes(part, padItemsToPaper(part, [], answers))
        }
        const correct = items.filter((it) => it.status === 'correct').length
        out.push({
          ...row,
          items,
          typeStats: buildTypeStats(items),
          scoredTypes: true,
          correct,
          total: items.length,
          pct: items.length ? Math.round((correct / items.length) * 100) : 0,
          answers,
        })
        continue
      }
      if (row.scoredTypes || (hasTypeStats(row.typeStats) && row.items.length)) {
        out.push({ ...row, scoredTypes: true })
        continue
      }
      const typeStats = typeStatsFromPart(part)
      out.push({
        ...row,
        total: Math.max(row.total, paperTotal),
        typeStats,
        scoredTypes: row.correct === 0 && paperTotal > 0 && hasTypeStats(typeStats),
      })
    } catch {
      out.push(row)
    }
  }
  return out
}

function formatTypeCell(attempt: Attempt) {
  const entries = Object.entries(attempt.typeStats).filter(([, row]) => (row?.total || 0) > 0)
  if (!entries.length) return '—'
  return entries
    .map(([name, row]) =>
      attempt.scoredTypes ? `${name} ${row.correct}/${row.total}` : `${name} ${row.total}题`,
    )
    .join(' · ')
}

function pctClass(pct: number) {
  if (pct >= 70) return 'ok'
  if (pct >= 50) return 'mid'
  return 'bad'
}

export default function PartHistory() {
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const moduleType = search.get('module_type') || ''
  const title = MODULE_NAMES[moduleType] || '真题记录'
  const [attempts, setAttempts] = useState<Attempt[] | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    setError('')
    setAttempts(null)
    loadStudentProgress()
      .then((data) =>
        mergeExtraAttempts(
          mergeAttempts(moduleType, data.test_records || [], data.study_sessions || []),
          mockSetAttempts(moduleType, data.test_records || []),
        ),
      )
      .then(async (rows) => {
        if (isTeacherViewingStudent()) return rows
        const homework = await listMySubmissions().catch(() => [])
        const withHomework = mergeExtraAttempts(rows, homeworkAttempts(moduleType, homework))
        return mergeLocalAttempts(withHomework, localAttempts(moduleType))
      })
      .then((rows) => fillMissingTypeStats(rows))
      .then((rows) => {
        if (!cancelled) setAttempts(rows)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message)
      })
    return () => {
      cancelled = true
    }
  }, [moduleType])

  const typeTotals = useMemo(() => {
    const stats: Record<string, TypeStat> = {}
    for (const attempt of attempts || []) {
      if (!attempt.scoredTypes) continue
      for (const [name, row] of Object.entries(attempt.typeStats || {})) {
        if (!stats[name]) stats[name] = { correct: 0, total: 0, wrong: 0, blank: 0 }
        stats[name].correct += row.correct || 0
        stats[name].total += row.total || 0
        stats[name].wrong += row.wrong || 0
        stats[name].blank += row.blank || 0
      }
    }
    return Object.entries(stats).sort((a, b) => b[1].total - a[1].total)
  }, [attempts])

  const openReview = (attempt: Attempt) => {
    if (!attempt.bookId || !attempt.sId) return
    const backQs = withTeacherViewParams(search).toString()
    const payload = {
      answers: attempt.answers,
      items: attempt.items,
      historyBack: `/student/history?${backQs}`,
    }
    try {
      sessionStorage.setItem('jianya-history-review', JSON.stringify(payload))
    } catch {
      /* ignore */
    }
    const q = withTeacherViewParams(search)
    q.set('review', '1')
    q.set('from', 'history')
    navigate(`/exam/${attempt.bookId}/${attempt.subject}/${attempt.sId}?${q.toString()}`, {
      state: payload,
    })
  }

  return (
    <div className="shell overview-shell">
      <header className="overview-hero">
        <h1>{title} 历史</h1>
        <p>
          {isTeacherViewingStudent()
            ? '教师查看：该生本 Part 的学习/测试记录。点进去看对错对照。'
            : '进度表学习/测试、作业交卷、剑雅真题页作答都会记在这里。点进去看对错对照。'}
        </p>
      </header>

      {error ? <p className="overview-error">{error}</p> : null}

      {attempts === null && !error ? <p className="status">加载记录…</p> : null}

      {attempts && attempts.length > 0 ? (
        <section className="overview-stats">
          {typeTotals.length ? (
            typeTotals.map(([name, row]) => (
              <div className="stat-card" key={name}>
                <strong>
                  {row.correct}/{row.total}
                </strong>
                <span>
                  {name} · {row.total ? Math.round((row.correct / row.total) * 100) : 0}%
                </span>
              </div>
            ))
          ) : (
            <div className="stat-card">
              <strong>{attempts.length}</strong>
              <span>已记录次数</span>
            </div>
          )}
        </section>
      ) : null}

      {attempts && attempts.length === 0 ? (
        <section className="overview-empty">
          <p>还没有{title}的学习或测试记录。交卷后会出现在这里。</p>
        </section>
      ) : null}

      {attempts && attempts.length > 0 ? (
        <section className="overview-block">
          <div className="overview-block-head">
            <h2>作答记录</h2>
            <span className="overview-block-score">{attempts.length} 次</span>
          </div>
          <div className="overview-table hist-table">
            <div className="overview-row hist-row head">
              <span>时间</span>
              <span>类型</span>
              <span>试卷</span>
              <span>正确率</span>
              <span>题型</span>
            </div>
            {attempts.map((attempt) => (
              <button
                type="button"
                className="overview-row hist-row hist-row-btn"
                key={attempt.id}
                onClick={() => openReview(attempt)}
              >
                <span className="overview-time">
                  {attempt.createdAt
                    ? new Date(attempt.createdAt).toLocaleString('zh-CN', {
                        month: 'numeric',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })
                    : '—'}
                </span>
                <span>{kindLabel(attempt.kind)}</span>
                <span className="overview-label">
                  C{attempt.bookId} Part {attempt.sPart}
                  {attempt.label ? ` · ${attempt.label.replace(/^【听力】|【阅读】/, '')}` : ''}
                </span>
                <span>
                  <strong className={pctClass(attempt.pct)}>
                    {attempt.correct}/{attempt.total}（{attempt.pct}%）
                  </strong>
                </span>
                <span className="hist-types">{formatTypeCell(attempt)}</span>
              </button>
            ))}
          </div>
          <p className="empty-hint">点开任意一次记录，查看当时的对错对照页。</p>
        </section>
      ) : null}
    </div>
  )
}
