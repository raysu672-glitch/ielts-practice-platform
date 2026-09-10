import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import {
  getAssignment,
  getSubmission,
  loadAssignmentAnswers,
  saveAssignmentAnswers,
  saveSubmission,
  type PartRef,
} from '../lib/assignments'
import { writingTaskLabel, writingTipsFor } from '../lib/writingTopics'
import { writingReferenceFor } from '../lib/writingReference'

function wordCount(text: string) {
  return text.trim() ? text.trim().split(/\s+/).length : 0
}

export default function WritingExam() {
  const params = useParams()
  const [search] = useSearchParams()
  const bookId = Number(params.bookId || 100)
  const sId = Number(params.sId)
  const assignmentId = search.get('assignment') || ''
  const fromTeacher = search.get('from') === 'teacher'
  const reviewStudentId = search.get('student') || ''
  const homeworkMode = Boolean(assignmentId) && !fromTeacher
  const teacherReviewing = fromTeacher && Boolean(assignmentId) && Boolean(reviewStudentId)

  const [part, setPart] = useState<PartRef | null>(null)
  const [outline, setOutline] = useState('')
  const [essay, setEssay] = useState('')
  const [error, setError] = useState('')
  const [locked, setLocked] = useState(false)
  const [saving, setSaving] = useState(false)
  const draftTimer = useRef<number | null>(null)

  const backTo = assignmentId
    ? `/assignment/${assignmentId}${
        fromTeacher
          ? `?from=teacher${reviewStudentId ? `&student=${encodeURIComponent(reviewStudentId)}` : ''}`
          : ''
      }`
    : '/student'

  const minWords = part?.task === 'task1' ? 150 : 250

  useEffect(() => {
    let cancelled = false
    setError('')
    setPart(null)
    setOutline('')
    setEssay('')
    setLocked(false)
    if (!assignmentId || !sId) {
      setError('缺少作业题目')
      return
    }
    ;(async () => {
      try {
        const asg = await getAssignment(assignmentId)
        if (cancelled) return
        const found = (asg?.parts || []).find(
          (row) => row.subject === 'writing' && row.bookId === bookId && row.sId === sId,
        )
        if (!asg || !found) {
          setError('找不到这道写作题')
          return
        }
        setPart(found)
        const submitted = await getSubmission(
          assignmentId,
          bookId,
          'writing',
          sId,
          teacherReviewing ? reviewStudentId : undefined,
        )
        if (cancelled) return
        if (submitted) {
          setOutline(submitted.answers.outline || '')
          setEssay(submitted.answers.essay || '')
          setLocked(true)
          return
        }
        if (homeworkMode) {
          const draft = await loadAssignmentAnswers(assignmentId, bookId, 'writing', sId)
          if (!cancelled) {
            setOutline(draft.outline || '')
            setEssay(draft.essay || '')
          }
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : '无法加载题目')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [assignmentId, bookId, sId, homeworkMode, teacherReviewing, reviewStudentId])

  useEffect(() => {
    if (!homeworkMode || locked || !part) return
    if (draftTimer.current) window.clearTimeout(draftTimer.current)
    draftTimer.current = window.setTimeout(() => {
      void saveAssignmentAnswers(assignmentId, bookId, 'writing', sId, { outline, essay })
    }, 800)
    return () => {
      if (draftTimer.current) window.clearTimeout(draftTimer.current)
    }
  }, [outline, essay, homeworkMode, locked, part, assignmentId, bookId, sId])

  const words = useMemo(() => wordCount(essay), [essay])
  const tips = writingTipsFor(part)
  const reference = useMemo(() => writingReferenceFor(part?.sId), [part])

  const submit = async () => {
    if (!part || !homeworkMode || locked) return
    if (!outline.trim()) {
      alert('请先在左侧写下中文思路')
      return
    }
    if (!essay.trim()) {
      alert('请先写完英文作文再提交')
      return
    }
    setSaving(true)
    try {
      await saveSubmission({
        assignmentId,
        bookId,
        subject: 'writing',
        sId,
        answers: { outline: outline.trim(), essay: essay.trim() },
        graded: { total: 1, correct: 0, wrong: 0, blank: 0, score: 0, items: [] },
      })
      if (window.parent !== window) {
        window.parent.postMessage(
          { type: 'jianyaAssignmentSubmitted', assignmentId },
          window.location.origin,
        )
      }
      setLocked(true)
    } catch (err) {
      alert(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSaving(false)
    }
  }

  if (error) return <div className="exam-status">{error}</div>
  if (!part) return <div className="exam-status">加载题目…</div>

  return (
    <div className="exam-shell writing-exam">
      <header className="exam-chrome">
        <div className="exam-chrome-left">
          <Link className="exam-back" to={backTo}>
            ← 作业
          </Link>
          <div className="exam-badge">WRITING</div>
          <div className="exam-chrome-meta">
            <strong>
              {writingTaskLabel(part.task || '')} · {part.label}
            </strong>
            <span>至少 {minWords} 词</span>
          </div>
        </div>
      </header>
      <main className="writing-exam-main">
        <section className="writing-prompt-card writing-prompt-compact">
          <p className="writing-prompt-kicker">
            第{part.lesson || part.testNo}课
            {part.pattern ? ` · ${part.pattern}` : ''}
            {part.examMeta ? ` · ${part.examMeta}` : ''}
          </p>
          <h1>{part.label}</h1>
          <p className="writing-prompt-text">{part.prompt}</p>
        </section>
        <section className="writing-ref-grid">
          <article className="writing-ref-card writing-ref-tips">
            <h2>老师提示</h2>
            {tips ? (
              <p className="writing-tips-text">{tips}</p>
            ) : (
              <p className="writing-ref-empty">本题暂无提纲</p>
            )}
          </article>
          <article className="writing-ref-card writing-ref-vocab">
            <h2>题材词汇</h2>
            {reference.vocab.length ? (
              <ul className="writing-vocab-list">
                {reference.vocab.map((item) => (
                  <li key={`${item.en}-${item.zh}`}>{item.zh}</li>
                ))}
              </ul>
            ) : (
              <p className="writing-ref-empty">本题暂无对应词伙</p>
            )}
          </article>
          <article className="writing-ref-card writing-ref-sentences">
            <h2>句子中文</h2>
            {reference.sentences.length ? (
              <ol className="writing-sentence-list">
                {reference.sentences.map((item) => (
                  <li key={item.zh}>{item.zh}</li>
                ))}
              </ol>
            ) : (
              <p className="writing-ref-empty">本题暂无对应句子</p>
            )}
          </article>
        </section>
        <section className="writing-compose">
          <label className="writing-essay-field">
            <span>中文思路</span>
            <textarea
              value={outline}
              onChange={(e) => setOutline(e.target.value)}
              readOnly={locked || teacherReviewing || !homeworkMode}
            />
            <div className="writing-essay-meta">
              <span>写完思路后再写右侧英文</span>
              {locked ? <span>已提交</span> : null}
            </div>
          </label>
          <label className="writing-essay-field">
            <span>英文作文</span>
            <textarea
              value={essay}
              onChange={(e) => setEssay(e.target.value)}
              readOnly={locked || teacherReviewing || !homeworkMode}
            />
            <div className="writing-essay-meta">
              <span>约 {words} 词（建议 ≥ {minWords}）</span>
              {locked ? <span>已提交，不可再改</span> : null}
            </div>
          </label>
        </section>
        {homeworkMode && !locked ? (
          <div className="writing-exam-actions">
            <button type="button" className="btn teacher-publish" disabled={saving} onClick={submit}>
              {saving ? '提交中…' : '提交作文'}
            </button>
          </div>
        ) : null}
      </main>
    </div>
  )
}
