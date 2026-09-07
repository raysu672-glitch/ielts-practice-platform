import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  getBookId,
  loadCatalog,
  loadManifest,
  parseTestNo,
  setBookId,
  type BookInfo,
} from '../lib/data'
import {
  clearAllAttempts,
  clearPartAttempt,
  loadAllResults,
  type StoredResult,
} from '../lib/results'
import type { Manifest, Subject } from '../types'

export default function Overview() {
  const [books, setBooks] = useState<BookInfo[]>([])
  const [bookId, setBookIdState] = useState(getBookId)
  const [manifest, setManifest] = useState<Manifest | null>(null)
  const [results, setResults] = useState<StoredResult[]>([])
  const [error, setError] = useState('')

  const refresh = useCallback((id = bookId) => setResults(loadAllResults(id)), [bookId])

  useEffect(() => {
    loadCatalog()
      .then((list) => {
        setBooks(list)
        const current = getBookId()
        if (list.length && !list.some((b) => b.bookId === current)) {
          const next = list[0].bookId
          setBookId(next)
          setBookIdState(next)
        } else {
          setBookIdState(current)
        }
      })
      .catch(() => setBooks([]))
  }, [])

  useEffect(() => {
    setManifest(null)
    setError('')
    setResults(loadAllResults(bookId))
    loadManifest(bookId)
      .then(setManifest)
      .catch((e: Error) => setError(e.message))
  }, [bookId])

  const totalParts = manifest
    ? manifest.parts.listening.filter((p) => !p.error).length +
      manifest.parts.reading.filter((p) => !p.error).length
    : 28

  const summary = useMemo(() => {
    const done = results.length
    const totalQ = results.reduce((s, r) => s + r.total, 0)
    const totalOk = results.reduce((s, r) => s + r.correct, 0)
    const avg = done ? Math.round(results.reduce((s, r) => s + r.pct, 0) / done) : 0
    return { done, totalQ, totalOk, avg }
  }, [results])

  const bookSummaries = useMemo(() => {
    return books.map((b) => {
      const rows = loadAllResults(b.bookId)
      const totalQ = rows.reduce((s, r) => s + r.total, 0)
      const totalOk = rows.reduce((s, r) => s + r.correct, 0)
      return {
        bookId: b.bookId,
        label: b.label,
        done: rows.length,
        totalOk,
        totalQ,
        avg: rows.length ? Math.round(rows.reduce((s, r) => s + r.pct, 0) / rows.length) : 0,
      }
    })
  }, [books, results])

  const grouped = useMemo(() => {
    const map = new Map<string, StoredResult[]>()
    for (const r of results) {
      const k = `${r.subject}-${r.testNo}`
      if (!map.has(k)) map.set(k, [])
      map.get(k)!.push(r)
    }
    for (const list of map.values()) list.sort((a, b) => a.sPart - b.sPart)
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b))
  }, [results])

  const onPickBook = (id: number) => {
    if (id === bookId) return
    setBookId(id)
    setBookIdState(id)
  }

  const onClearAll = () => {
    if (!confirm(`清空 C${bookId} 的全部作答与成绩？此操作不可恢复。`)) return
    clearAllAttempts(bookId)
    refresh(bookId)
  }

  const onRetake = (subject: Subject, sId: number) => {
    if (!confirm('清除本题作答与成绩，重新开始？')) return
    clearPartAttempt(subject, sId, bookId)
    refresh(bookId)
    window.location.href = `/exam/${subject}/${sId}`
  }

  if (error && !manifest) {
    return <div className="shell status">{error}</div>
  }

  return (
    <div className="shell overview-shell">
      <header className="overview-hero">
        <Link className="overview-back" to="/student">
          ← 返回学生端
        </Link>
        <h1>成绩总览</h1>
        <p>
          各册成绩分开保存。当前查看：ACADEMIC C{manifest?.bookId ?? bookId}（保存在本机浏览器）
        </p>

        {books.length > 0 && (
          <div className="book-switch" role="tablist" aria-label="题库册号">
            {books.map((b) => (
              <button
                key={b.bookId}
                type="button"
                className={`book-chip ${b.bookId === bookId ? 'active' : ''}`}
                onClick={() => onPickBook(b.bookId)}
              >
                C{b.bookId}
              </button>
            ))}
          </div>
        )}

        {bookSummaries.length > 1 && (
          <div className="overview-book-strip">
            {bookSummaries.map((b) => (
              <button
                key={b.bookId}
                type="button"
                className={`overview-book-card ${b.bookId === bookId ? 'active' : ''}`}
                onClick={() => onPickBook(b.bookId)}
              >
                <strong>C{b.bookId}</strong>
                <span>
                  {b.done ? `${b.totalOk}/${b.totalQ || '—'} · ${b.avg}%` : '暂无记录'}
                </span>
              </button>
            ))}
          </div>
        )}

        <div className="overview-actions">
          <button type="button" className="btn ghost" onClick={onClearAll}>
            清空本册记录
          </button>
        </div>
        {error && manifest && <p className="overview-error">{error}</p>}
      </header>

      <section className="overview-stats">
        <div className="stat-card">
          <strong>{summary.done}</strong>
          <span>已交卷 Part</span>
        </div>
        <div className="stat-card">
          <strong>
            {summary.done}/{totalParts}
          </strong>
          <span>完成进度</span>
        </div>
        <div className="stat-card">
          <strong>
            {summary.totalOk}/{summary.totalQ}
          </strong>
          <span>总答对题数</span>
        </div>
        <div className="stat-card">
          <strong>{summary.avg}%</strong>
          <span>平均正确率</span>
        </div>
      </section>

      {results.length === 0 ? (
        <section className="overview-empty">
          <p>C{bookId} 还没有交卷记录。做题并交卷后会出现在这里。</p>
        </section>
      ) : (
        grouped.map(([key, rows]) => {
          const [subject, testNo] = key.split('-') as [Subject, string]
          const testCorrect = rows.reduce((s, r) => s + r.correct, 0)
          const testTotal = rows.reduce((s, r) => s + r.total, 0)
          return (
            <section className="overview-block" key={`${bookId}-${key}`}>
              <div className="overview-block-head">
                <h2>
                  {subject === 'listening' ? '听力' : '阅读'} · Test {testNo}
                </h2>
                <span className="overview-block-score">
                  {testCorrect}/{testTotal}（
                  {testTotal ? Math.round((testCorrect / testTotal) * 100) : 0}%）
                </span>
              </div>
              <div className="overview-table">
                <div className="overview-row head">
                  <span>Part</span>
                  <span>名称</span>
                  <span>得分</span>
                  <span>正确率</span>
                  <span>交卷时间</span>
                  <span>操作</span>
                </div>
                {rows.map((r) => (
                  <div className="overview-row" key={r.sId}>
                    <span>Part {r.sPart}</span>
                    <span className="overview-label">{r.label}</span>
                    <span>
                      <strong className={r.pct >= 60 ? 'ok' : r.pct >= 40 ? 'mid' : 'bad'}>
                        {r.correct}/{r.total}
                      </strong>
                    </span>
                    <span>{r.pct}%</span>
                    <span className="overview-time">
                      {new Date(r.submittedAt).toLocaleString('zh-CN', {
                        month: 'numeric',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                    <span className="overview-ops">
                      <Link
                        to={`/exam/${bookId}/${r.subject}/${r.sId}?review=1&from=overview`}
                      >
                        详情
                      </Link>
                      <button type="button" onClick={() => onRetake(r.subject, r.sId)}>
                        重测
                      </button>
                    </span>
                  </div>
                ))}
              </div>
            </section>
          )
        })
      )}

      {manifest && (
        <section className="overview-pending">
          <h3>未交卷 Part（C{bookId}）</h3>
          <div className="pending-grid">
            {(['listening', 'reading'] as Subject[]).flatMap((subject) =>
              manifest.parts[subject]
                .filter((p) => !p.error && !results.some((r) => r.subject === subject && r.sId === p.sId))
                .map((p) => (
                  <Link
                    className="pending-link"
                    key={`${subject}-${p.sId}`}
                    to={`/exam/${subject}/${p.sId}`}
                  >
                    {subject === 'listening' ? '听力' : '阅读'} T{parseTestNo(p.sName)} P{p.sPart}
                  </Link>
                )),
            )}
          </div>
        </section>
      )}
    </div>
  )
}
