import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import {
  formatClock,
  formatTypeStats,
  loadMockSets,
  migrateLocalMockSets,
  paperShortLabel,
  type MockSetRecord,
} from '../lib/mockExam'
import { isTeacherViewingStudent, withTeacherViewParams } from '../lib/studentApi'
import type { Subject } from '../types'

function pctClass(pct: number) {
  if (pct >= 70) return 'ok'
  if (pct >= 50) return 'mid'
  return 'bad'
}

function subjectLabel(subject: Subject) {
  return subject === 'listening' ? '听力' : '阅读'
}

export default function MockHistory() {
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const qs = search.toString()
  const [rows, setRows] = useState<MockSetRecord[] | null>(null)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<'all' | Subject>('all')

  useEffect(() => {
    let cancelled = false
    const boot = isTeacherViewingStudent()
      ? Promise.resolve()
      : migrateLocalMockSets()
    boot
      .then(() => loadMockSets())
      .then((data) => {
        if (!cancelled) setRows(data)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message || '加载失败')
      })
    return () => {
      cancelled = true
    }
  }, [])

  const visible = useMemo(
    () => (rows || []).filter((row) => filter === 'all' || row.subject === filter),
    [rows, filter],
  )

  const openReview = (part: MockSetRecord['parts'][number]) => {
    const backQs = withTeacherViewParams(search).toString()
    const payload = {
      answers: part.answers || {},
      items: part.items || [],
      historyBack: `/student/mock/history${backQs ? `?${backQs}` : ''}`,
    }
    try {
      sessionStorage.setItem('jianya-history-review', JSON.stringify(payload))
    } catch {
      /* ignore */
    }
    const q = withTeacherViewParams(search)
    q.set('review', '1')
    q.set('from', 'history')
    navigate(`/exam/${part.bookId}/${part.subject}/${part.sId}?${q.toString()}`, { state: payload })
  }

  return (
    <div className="shell overview-shell mock-hist">
      <header className="overview-hero">
        {isTeacherViewingStudent() ? null : (
          <Link className="exam-back" to={`/student/mock${qs ? `?${qs}` : ''}`}>
            ← 返回模拟考
          </Link>
        )}
        <h1>模拟考历史</h1>
        <p>
          {isTeacherViewingStudent()
            ? '教师查看：该生每套模考的总分、题型正确率与各 Part 用时。点 Part 可看对错对照。'
            : '每套模考会记下总分、各题型正确率，以及你在每个 Part 停留作答的时间。点 Part 可看对错对照。'}
        </p>
      {isTeacherViewingStudent() ? null : (
        <div className="hero-actions">
          <Link className="btn ghost" to={`/student/mock${qs ? `?${qs}` : ''}`}>
            返回模拟考
          </Link>
        </div>
      )}
      </header>

      <div className="mock-hist-filters">
        {(['all', 'reading', 'listening'] as const).map((key) => (
          <button
            key={key}
            type="button"
            className={`book-chip ${filter === key ? 'active' : ''}`}
            onClick={() => setFilter(key)}
          >
            {key === 'all' ? '全部' : subjectLabel(key)}
          </button>
        ))}
      </div>

      {error ? <p className="overview-error">{error}</p> : null}
      {rows === null && !error ? <p className="status">加载记录…</p> : null}

      {rows && visible.length === 0 ? (
        <section className="overview-empty">
          <p>还没有模拟考记录。交卷后会出现在这里。</p>
        </section>
      ) : null}

      {visible.map((row) => (
        <article className="mock-hist-card" key={row.id}>
          <header>
            <div>
              <strong>{subjectLabel(row.subject)}模拟考</strong>
              <span className="overview-time">
                {row.submittedAt ? new Date(row.submittedAt).toLocaleString('zh-CN') : '—'}
              </span>
            </div>
            <div className="mock-hist-score">
              <strong className={pctClass(row.pct)}>
                {row.correct}/{row.total}（{row.pct}%）
              </strong>
              <span>整场 {formatClock(row.durationSeconds)}</span>
            </div>
          </header>
          <p className="hist-types mock-hist-types">{formatTypeStats(row.typeStats)}</p>
          <div className="overview-table">
            <div className="overview-row mock-hist-row head">
              <span>Part</span>
              <span>试卷</span>
              <span>得分</span>
              <span>用时</span>
              <span>题型正确率</span>
            </div>
            {row.parts.map((part) => (
              <button
                type="button"
                className="overview-row mock-hist-row hist-row-btn"
                key={`${row.id}-${part.sId}`}
                onClick={() => openReview(part)}
              >
                <span>P{part.sPart}</span>
                <span className="overview-label">
                  {paperShortLabel(part)}
                  {part.label ? ` · ${String(part.label).replace(/^【听力】|【阅读】/, '')}` : ''}
                </span>
                <span>
                  <strong className={pctClass(part.pct)}>
                    {part.correct}/{part.total}（{part.pct}%）
                  </strong>
                </span>
                <span>{formatClock(part.durationSeconds)}</span>
                <span className="hist-types">{formatTypeStats(part.typeStats)}</span>
              </button>
            ))}
          </div>
        </article>
      ))}
    </div>
  )
}
