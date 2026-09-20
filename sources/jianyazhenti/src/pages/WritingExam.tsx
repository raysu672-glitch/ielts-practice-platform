import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import {
  getAssignment,
  getSubmission,
  loadAssignmentAnswers,
  saveAssignmentAnswers,
  type PartRef,
  type WritingCorrection,
} from '../lib/assignments'
import { writingTaskLabel, writingTipsFor } from '../lib/writingTopics'
import { writingReferenceFor } from '../lib/writingReference'

function wordCount(text: string) {
  return text.trim() ? text.trim().split(/\s+/).length : 0
}

function formatCheckedAt(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString('zh-CN', { hour12: false })
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
  const [correction, setCorrection] = useState<WritingCorrection | null>(null)
  const draftTimer = useRef<number | null>(null)

  const studentId = sessionStorage.getItem('jianya-student-id') || ''

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
    setCorrection(null)
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
          if (submitted.correction) setCorrection(submitted.correction)
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

  // 学生提交：跳到改错训练页，学生逐句改完语法错误后再由改错页回写作业提交。
  const startCorrection = () => {
    if (!part || !homeworkMode || locked) return
    if (!outline.trim() || !essay.trim()) {
      alert('中文思路和英文作文都要写完')
      return
    }
    const topic = [writingTaskLabel(part.task || ''), part.label, part.prompt]
      .filter(Boolean)
      .join('\n')
    const payload = {
      assignmentId,
      bookId,
      sId,
      topic,
      essay: essay.trim(),
      outline: outline.trim(),
      studentId,
      returnTo: `/jianyazhenti/assignment/${encodeURIComponent(assignmentId)}?embed=1`,
    }
    try {
      sessionStorage.setItem('ielts_assignment_payload', JSON.stringify(payload))
    } catch {
      alert('无法保存作业草稿，请重试')
      return
    }
    window.location.href = '/xiezuopigai/ielts-student-practice.html?assignment=1'
  }

  if (error) return <div className="exam-status">{error}</div>
  if (!part) return <div className="exam-status">加载题目…</div>

  const readOnly = locked || teacherReviewing || !homeworkMode

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
              readOnly={readOnly}
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
              readOnly={readOnly}
            />
            <div className="writing-essay-meta">
              <span>约 {words} 词（建议 ≥ {minWords}）</span>
              {locked ? <span>已提交，不可再改</span> : null}
            </div>
          </label>
        </section>

        {correction ? (
          <section className="writing-correction">
            <div className="writing-correction-head">
              <h2>AI 语法检查报告</h2>
              <span>
                {correction.count ? `共 ${correction.count} 处建议` : '未发现明显语法错误'}
                {correction.checkedAt ? ` · ${formatCheckedAt(correction.checkedAt)}` : ''}
              </span>
            </div>
            {correction.aiFailed ? (
              <p className="writing-correction-note">
                {correction.aiMessage || 'AI 批改未成功，以下仅供参考。'}
              </p>
            ) : null}
            {correction.count ? (
              <ul className="writing-correction-list">
                {correction.errors.map((err) => (
                  <li key={err.id} className="writing-correction-item">
                    <div className="writing-correction-item-head">
                      <span className="writing-correction-category">{err.category}</span>
                      <span className="writing-correction-question">{err.question}</span>
                    </div>
                    <div className="writing-correction-row">
                      <span className="writing-correction-tag">出错片段</span>
                      <mark className="writing-correction-bad">{err.matchedText || '—'}</mark>
                    </div>
                    {err.corrected ? (
                      <div className="writing-correction-row">
                        <span className="writing-correction-tag">参考改法</span>
                        <span className="writing-correction-good">{err.corrected}</span>
                      </div>
                    ) : null}
                    {err.explanation ? (
                      <p className="writing-correction-expl">{err.explanation}</p>
                    ) : null}
                    {err.hints.length ? (
                      <ul className="writing-correction-hints">
                        {err.hints.map((h, i) => (
                          <li key={i}>{h}</li>
                        ))}
                      </ul>
                    ) : null}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="writing-correction-note ok">很好，AI 没有发现语法错误。</p>
            )}
          </section>
        ) : null}

        {homeworkMode && !locked ? (
          <div className="writing-exam-actions">
            <button
              type="button"
              className="btn teacher-publish"
              onClick={startCorrection}
            >
              提交并开始改错
            </button>
          </div>
        ) : null}
      </main>
    </div>
  )
}