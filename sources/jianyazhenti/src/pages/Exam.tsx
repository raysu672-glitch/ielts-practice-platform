import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import PaperHost from '../components/PaperHost'
import {
  getAssignment,
  getSubmission,
  loadAssignmentAnswers,
  saveAssignmentAnswers,
  saveSubmission,
} from '../lib/assignments'
import { audioSrc, getBookId, loadAnswerKey, loadAnswers, loadPart, saveAnswers } from '../lib/data'
import { gradePart, padItemsToPaper, recountGrade, type GradeItem, type GradeResult } from '../lib/grade'
import { clearPartAttempt, loadResult, submitCurrentAnswers } from '../lib/results'
import { attachQuestionTypes, buildTypeStats } from '../lib/questionTypes'
import { PART_MODULE_NAMES, moduleTypeForPart } from '../lib/partModules'
import { isAuthError, postStudentJson } from '../lib/studentApi'
import type { PartData, Subject } from '../types'

type HistoryReviewState = {
  answers?: Record<string, string>
  items?: GradeItem[]
  historyBack?: string
}

function readHistoryReview(state: unknown): HistoryReviewState | null {
  const fromState = state && typeof state === 'object' ? (state as HistoryReviewState) : null
  if (fromState && (fromState.answers || fromState.items)) return fromState
  try {
    const raw = sessionStorage.getItem('jianya-history-review')
    if (!raw) return null
    return JSON.parse(raw) as HistoryReviewState
  } catch {
    return null
  }
}

function paperDetails(
  part: PartData,
  bookId: number,
  graded: GradeResult,
  answers: Record<string, string>,
  source: string,
  assignmentId = '',
  durationSeconds = 0,
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
        source,
        assignmentId: assignmentId || undefined,
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

function reportHostResult(
  mode: string,
  graded: GradeResult,
  startedAt: number,
  part: PartData,
  bookId: number,
  answers: Record<string, string>,
) {
  if (window.parent === window) return
  const durationSeconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000))
  const packed = paperDetails(part, bookId, graded, answers, mode === 'test' ? 'test' : 'study', '', durationSeconds)
  if (mode === 'test') {
    window.parent.postMessage(
      {
        type: 'genericTestComplete',
        completed: true,
        score: packed.correct,
        correctCount: packed.correct,
        totalCount: packed.total,
        scorePercent: packed.pct,
        durationSeconds,
        details: packed.details,
      },
      window.location.origin,
    )
  } else if (mode === 'study') {
    window.parent.postMessage(
      {
        type: 'genericStudyComplete',
        durationSeconds,
        totalCount: packed.total,
        correctCount: packed.correct,
        scorePercent: packed.pct,
        details: packed.details,
      },
      window.location.origin,
    )
  }
}

async function persistPartAttempt(
  hostMode: string,
  homework: boolean,
  assignmentId: string,
  graded: GradeResult,
  startedAt: number,
  part: PartData,
  bookId: number,
  answers: Record<string, string>,
) {
  if (hostMode === 'study' || hostMode === 'test') return
  const moduleType = moduleTypeForPart(part.subject, part.sPart)
  if (!moduleType) return
  const durationSeconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000))
  const packed = paperDetails(
    part,
    bookId,
    graded,
    answers,
    homework ? 'homework' : 'practice',
    assignmentId,
    durationSeconds,
  )
  try {
    await postStudentJson('/api/student/study-sessions', {
      module_type: moduleType,
      module_name: PART_MODULE_NAMES[moduleType],
      session_kind: 'study',
      words_tested: packed.total,
      initial_correct: packed.correct,
      score_percent: packed.pct,
      duration_seconds: durationSeconds,
      details: packed.details,
    })
  } catch (err) {
    if (isAuthError(err) || homework) return
    throw err
  }
}

function Timer({ paused }: { paused?: boolean }) {
  const [elapsed, setElapsed] = useState(0)
  useEffect(() => {
    if (paused) return
    const t = window.setInterval(() => setElapsed((x) => x + 1), 1000)
    return () => window.clearInterval(t)
  }, [paused])
  const h = String(Math.floor(elapsed / 3600)).padStart(2, '0')
  const m = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0')
  const s = String(elapsed % 60).padStart(2, '0')
  return (
    <div className="exam-timer">
      答题时长：{h}:{m}:{s}
    </div>
  )
}

export default function Exam() {
  const params = useParams()
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const location = useLocation()

  const bookFromRoute = params.bookId && /^\d+$/.test(params.bookId) ? Number(params.bookId) : null
  const subject = (params.subject || 'listening') as Subject
  const id = Number(params.sId)
  const bookId = bookFromRoute ?? getBookId()
  const assignmentId = search.get('assignment') || ''
  const wantReview = search.get('review') === '1'
  const fromTeacher = search.get('from') === 'teacher'
  const fromOverview = search.get('from') === 'overview'
  const fromHistory = search.get('from') === 'history'
  const hostMode = search.get('mode') || ''
  const homeworkMode = Boolean(assignmentId) && !fromTeacher
  const historyReview = fromHistory ? readHistoryReview(location.state) : null
  const startedAtRef = useRef(Date.now())

  const [part, setPart] = useState<PartData | null>(null)
  const [error, setError] = useState('')
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [sheetOpen, setSheetOpen] = useState(true)
  const [ready, setReady] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const [locked, setLocked] = useState(false)
  const [reviewItems, setReviewItems] = useState<GradeItem[] | undefined>()
  const [scoreLine, setScoreLine] = useState('')
  const draftTimer = useRef<number | null>(null)

  const catalogQuery = (() => {
    const q = new URLSearchParams(search)
    q.delete('review')
    q.delete('assignment')
    return q.toString()
  })()
  const backTo = assignmentId
    ? `/assignment/${assignmentId}${fromTeacher ? '?from=teacher' : ''}`
    : fromHistory
      ? historyReview?.historyBack || `/student/history?${catalogQuery}`
      : fromOverview
        ? '/student/overview'
        : fromTeacher
          ? '/teacher/bank'
          : catalogQuery
            ? `/student?${catalogQuery}`
            : '/student'

  const backLabel = assignmentId
    ? '作业'
    : fromHistory
      ? String(historyReview?.historyBack || '').includes('/student/mock')
        ? '模拟考历史'
        : '历史'
      : fromOverview
        ? '成绩总览'
        : fromTeacher
          ? '题库'
          : '学生端'

  useEffect(() => {
    if (!id) return
    let cancelled = false
    setError('')
    setPart(null)
    setReady(false)
    setAnswers({})
    setReviewItems(undefined)
    setScoreLine('')
    setLocked(false)
    startedAtRef.current = Date.now()

    const practiceResult = !homeworkMode ? loadResult(subject, id, bookId) : null

    ;(async () => {
      try {
        if (homeworkMode) {
          const asg = await getAssignment(assignmentId)
          if (cancelled) return
          if (!asg) {
            setError('作业不存在或已删除')
            return
          }
        }
        const submitted = homeworkMode
          ? await getSubmission(assignmentId, bookId, subject, id)
          : null
        const data = await loadPart(subject, id, bookId)
        if (cancelled) return
        setPart(data)
        if (submitted) {
          setAnswers(submitted.answers)
          setLocked(true)
          try {
            const key = await loadAnswerKey(subject, id, bookId)
            const graded = gradePart(data, submitted.answers, key)
            setReviewItems(graded.items)
            setScoreLine(`${graded.correct}/${graded.total}（${submitted.pct}%）`)
          } catch {
            setReviewItems(undefined)
          }
        } else if (fromHistory && historyReview?.answers) {
          setAnswers(historyReview.answers)
          setLocked(true)
          if (historyReview.items && historyReview.items.length) {
            setReviewItems(historyReview.items)
            const ok = historyReview.items.filter((it) => it.status === 'correct').length
            const tot = historyReview.items.length
            setScoreLine(`${ok}/${tot}（${tot ? Math.round((ok / tot) * 100) : 0}%）`)
          } else {
            try {
              const key = await loadAnswerKey(subject, id, bookId)
              const graded = gradePart(data, historyReview.answers, key)
              setReviewItems(graded.items)
              setScoreLine(
                `${graded.correct}/${graded.total}（${
                  graded.total ? Math.round((graded.correct / graded.total) * 100) : 0
                }%）`,
              )
            } catch (e) {
              setError(e instanceof Error ? e.message : '无法加载答案比对')
              return
            }
          }
        } else if (wantReview && !homeworkMode) {
          const stored = loadAnswers(subject, id, bookId)
          if (!practiceResult && !Object.values(stored).some((v) => String(v).trim())) {
            setError('尚无交卷记录，请先完成作答')
            return
          }
          setAnswers(stored)
          setLocked(true)
          try {
            const key = await loadAnswerKey(subject, id, bookId)
            const graded = gradePart(data, stored, key)
            setReviewItems(graded.items)
            const pct =
              practiceResult?.pct ??
              (graded.total ? Math.round((graded.correct / graded.total) * 100) : 0)
            setScoreLine(`${graded.correct}/${graded.total}（${pct}%）`)
          } catch (e) {
            setError(e instanceof Error ? e.message : '无法加载答案比对')
            return
          }
        } else if (homeworkMode) {
          const stored = await loadAssignmentAnswers(assignmentId, bookId, subject, id)
          if (cancelled) return
          setAnswers(stored)
        } else {
          setAnswers(loadAnswers(subject, id, bookId))
        }
        if (!cancelled) setReady(true)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : '无法加载试卷')
      }
    })()

    return () => {
      cancelled = true
    }
  }, [subject, id, bookId, assignmentId, wantReview, homeworkMode, fromHistory])

  useEffect(() => {
    if (!part || !ready || locked) return
    if (homeworkMode) {
      if (draftTimer.current) window.clearTimeout(draftTimer.current)
      draftTimer.current = window.setTimeout(() => {
        saveAssignmentAnswers(assignmentId, bookId, subject, part.sId, answers).catch(() => {
          /* keep typing even if draft save fails */
        })
      }, 600)
      return () => {
        if (draftTimer.current) window.clearTimeout(draftTimer.current)
      }
    }
    saveAnswers(subject, part.sId, answers, bookId)
  }, [answers, part, subject, ready, locked, assignmentId, bookId, homeworkMode])

  const filled = useMemo(
    () => Object.values(answers).filter((v) => String(v).trim()).length,
    [answers],
  )

  const onAnswer = (num: string, value: string) => {
    if (locked) return
    setAnswers((prev) => (prev[num] === value ? prev : { ...prev, [num]: value }))
  }

  const enterReview = (graded: GradeResult, pct: number) => {
    setLocked(true)
    setReviewItems(graded.items)
    setScoreLine(`${graded.correct}/${graded.total}（${pct}%）`)
    const q = new URLSearchParams(search)
    q.set('review', '1')
    navigate(`/exam/${bookId}/${subject}/${id}?${q.toString()}`, { replace: true })
  }

  const submitExam = async () => {
    if (!part || locked) return
    try {
      if (homeworkMode) {
        await saveAssignmentAnswers(assignmentId, bookId, subject, part.sId, answers)
        const key = await loadAnswerKey(subject, part.sId, bookId)
        const graded = gradePart(part, answers, key)
        const sub = await saveSubmission({
          assignmentId,
          bookId,
          subject,
          sId: part.sId,
          answers,
          graded,
        })
        reportHostResult(hostMode, graded, startedAtRef.current, part, bookId, answers)
        await persistPartAttempt(
          hostMode,
          true,
          assignmentId,
          graded,
          startedAtRef.current,
          part,
          bookId,
          answers,
        )
        enterReview(graded, sub.pct)
      } else {
        saveAnswers(subject, part.sId, answers, bookId)
        const submitted = await submitCurrentAnswers(subject, part.sId, bookId)
        reportHostResult(hostMode, submitted.graded, startedAtRef.current, part, bookId, answers)
        await persistPartAttempt(
          hostMode,
          false,
          assignmentId,
          submitted.graded,
          startedAtRef.current,
          part,
          bookId,
          answers,
        )
        enterReview(submitted.graded, submitted.stored.pct)
      }
    } catch (e) {
      alert(e instanceof Error ? e.message : '无法批改')
    }
  }

  const retakeExam = () => {
    if (!part || assignmentId) return
    if (!confirm('清除本题作答与成绩，重新开始？')) return
    clearPartAttempt(subject, part.sId, bookId)
    setAnswers({})
    setReviewItems(undefined)
    setScoreLine('')
    setLocked(false)
    startedAtRef.current = Date.now()
    setAttempt((n) => n + 1)
    const q = new URLSearchParams(search)
    q.delete('review')
    const qs = q.toString()
    navigate(`/exam/${bookId}/${subject}/${id}${qs ? `?${qs}` : ''}`, { replace: true })
  }

  const jumpTo = (num: number) => {
    const root = document.querySelector('.paper-host')
    if (!root) return
    const el =
      (root.querySelector(`.qt-a[data-question-num="${num}"]`) as HTMLElement | null) ||
      (root.querySelector(`input[data-question-num="${num}"]:not([type=radio])`) as HTMLElement | null) ||
      (root.querySelector(`input[data-question-num="${num}"]`) as HTMLElement | null)
    el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    if (el instanceof HTMLInputElement && el.type !== 'radio' && !locked) el.focus()
  }

  if (error) return <div className="exam-status">{error}</div>
  if (!part) return <div className="exam-status">加载试卷…</div>

  const src = audioSrc(part, bookId)
  const passage = part.passage?.passages?.[0]
  const isReading = part.subject === 'reading' || subject === 'reading'
  const nums = part.questions.map((q) => q.number)
  const qRange = nums.length
    ? `Questions ${Math.min(...nums)}-${Math.max(...nums)}`
    : 'Questions'
  const passageBlocks = (passage?.paragraphs || []).filter(
    (p) => (p.html || p.text || '').trim() || (p.name || '').trim(),
  )

  return (
    <div className={`exam-shell ${isReading ? 'mode-reading' : 'mode-listening'}`}>
      <header className="exam-chrome">
        <div className="exam-chrome-left">
          <Link className="exam-back" to={backTo}>
            ← {backLabel}
          </Link>
          <div className="exam-badge">{isReading ? 'READING' : 'LISTENING'}</div>
          <div className="exam-chrome-meta">
            <strong>
              C{bookId} Part {part.sPart}
            </strong>
            <span>{qRange}</span>
            {locked && scoreLine ? <span className="exam-score-chip">{scoreLine}</span> : null}
          </div>
        </div>
        <div className="exam-chrome-right">
          <Timer paused={locked} />
          {!assignmentId && !fromHistory && (
            <button type="button" className="exam-tool" onClick={retakeExam}>
              重新测试
            </button>
          )}
          <button type="button" className="exam-tool" onClick={() => setSheetOpen((v) => !v)}>
            {sheetOpen ? '收起答题卡' : '答题卡'}
          </button>
          {locked ? (
            <span className="exam-tool locked">已交卷 · 比对中</span>
          ) : (
            <button type="button" className="exam-tool primary" onClick={submitExam}>
              交卷
            </button>
          )}
        </div>
      </header>

      <div
        className={`exam-stage ${sheetOpen ? 'with-sheet' : 'no-sheet'} ${
          isReading ? 'is-reading' : 'is-listening'
        }`}
      >
        {isReading && (
          <section className="exam-pane passage-pane">
            <div className="pane-scroll">
              {passage ? (
                <article className="passage-article">
                  {passage.title && <h1 className="passage-title">{passage.title}</h1>}
                  {passage.subtitle && <p className="passage-sub">{passage.subtitle}</p>}
                  {passageBlocks.map((p, i) => {
                    const label = (p.name || '').trim()
                    const body = (p.html || p.text || '').trim()
                    if (!body && !label) return null
                    return (
                      <div className={`passage-block ${label ? 'has-label' : ''}`} key={i}>
                        {label ? <div className="passage-label">{label}</div> : null}
                        {p.html ? (
                          <div
                            className="passage-html"
                            dangerouslySetInnerHTML={{ __html: p.html }}
                          />
                        ) : (
                          <p className="passage-text">{p.text}</p>
                        )}
                      </div>
                    )
                  })}
                </article>
              ) : (
                <p className="empty">暂无文章正文</p>
              )}
            </div>
          </section>
        )}

        <section className="exam-pane question-pane">
          <div className="pane-scroll">
            {part.paperHtml ? (
              <PaperHost
                key={`${bookId}-${subject}-${part.sId}-${attempt}-${locked ? 'r' : 'e'}`}
                html={part.paperHtml}
                answers={answers}
                onAnswer={onAnswer}
                readOnly={locked}
                reviewItems={reviewItems}
              />
            ) : (
              <FallbackQuestions
                part={part}
                answers={answers}
                onAnswer={onAnswer}
                readOnly={locked}
                reviewItems={reviewItems}
              />
            )}
          </div>
        </section>

        {sheetOpen && (
          <aside className="answer-sheet">
            <div className="answer-sheet-title">Answer Sheet</div>
            <div className="sheet-grid">
              {part.questions.map((q) => {
                const item = reviewItems?.find((it) => it.number === q.number)
                const cls = [
                  'sheet-item',
                  answers[String(q.number)]?.trim() ? 'filled' : '',
                  item ? `review-${item.status}` : '',
                ]
                  .filter(Boolean)
                  .join(' ')
                return (
                  <button
                    key={q.number}
                    type="button"
                    className={cls}
                    onClick={() => jumpTo(q.number)}
                  >
                    {q.number}
                  </button>
                )
              })}
            </div>
            <div className="sheet-meta">
              {filled}/{part.questions.length}
              {locked ? ' · 已锁定' : ''}
            </div>
          </aside>
        )}
      </div>

      {!isReading && src && (
        <footer className="audio-dock">
          <div className="audio-dock-label">Audio</div>
          <audio controls preload="metadata" src={src} />
        </footer>
      )}
    </div>
  )
}

function FallbackQuestions({
  part,
  answers,
  onAnswer,
  readOnly,
  reviewItems,
}: {
  part: PartData
  answers: Record<string, string>
  onAnswer: (num: string, value: string) => void
  readOnly?: boolean
  reviewItems?: GradeItem[]
}) {
  const byNum = new Map(reviewItems?.map((it) => [it.number, it]))
  return (
    <div className="fallback-q">
      {part.questions.map((q) => {
        const item = byNum.get(q.number)
        return (
          <div className="fallback-item" key={q.number}>
            <div className="fallback-stem">
              <strong>{q.number}.</strong> {q.stem || '填空'}
            </div>
            {q.type === 'single_choice' ? (
              <div className="opt-row">
                {q.options.map((op) => (
                  <label className="opt-label" key={op.value}>
                    <input
                      type="radio"
                      name={`q-${q.number}`}
                      value={op.value}
                      checked={answers[String(q.number)] === op.value}
                      disabled={readOnly}
                      onChange={() => onAnswer(String(q.number), op.value)}
                    />{' '}
                    {op.label}
                  </label>
                ))}
              </div>
            ) : (
              <input
                className="fallback-input"
                value={answers[String(q.number)] || ''}
                disabled={readOnly}
                readOnly={readOnly}
                onChange={(e) => onAnswer(String(q.number), e.target.value)}
                placeholder="answers here"
              />
            )}
            {item && item.status !== 'correct' && (
              <div className={`asg-review-hint is-${item.status}`}>
                <em>你的</em> {item.user?.trim() || '（空）'}
                {' '}
                <em>· 正确</em> {item.correct || '—'}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
