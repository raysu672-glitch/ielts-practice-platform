import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { absoluteAppUrl } from '../lib/embed'
import StudentPicker, { selectedIds } from '../components/StudentPicker'
import {
  addRecipients,
  assignmentPartPath,
  getAssignment,
  getRoster,
  isPartSubmitted,
  listSubmissions,
  listTeacherStudents,
  saveReview,
  type Assignment,
  type AssignmentRoster,
  type AssignmentSubmission,
  type RosterStudent,
  type TeacherStudent,
} from '../lib/assignments'

function statusLabel(row: RosterStudent) {
  if (row.status === 'submitted') return '已交'
  if (row.status === 'partial') return `部分完成 ${row.submittedParts}/${row.totalParts}`
  return '未交'
}

export default function AssignmentHub() {
  const { id = '' } = useParams()
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const fromTeacher = search.get('from') === 'teacher'
  const reviewStudentId = search.get('student') || ''
  const [assignment, setAssignment] = useState<Assignment | null>(null)
  const [loadError, setLoadError] = useState(false)
  const [subs, setSubs] = useState<AssignmentSubmission[]>([])
  const [roster, setRoster] = useState<AssignmentRoster | null>(null)
  const [students, setStudents] = useState<TeacherStudent[]>([])
  const [adding, setAdding] = useState<Record<string, boolean>>({})
  const [savingAdd, setSavingAdd] = useState(false)
  const [comment, setComment] = useState('')
  const [savingComment, setSavingComment] = useState(false)
  const [copied, setCopied] = useState(false)

  const loadTeacherData = async (asgId: string, studentId?: string) => {
    const [nextRoster, teacherStudents] = await Promise.all([
      getRoster(asgId),
      listTeacherStudents().catch(() => [] as TeacherStudent[]),
    ])
    setRoster(nextRoster)
    setStudents(teacherStudents)
    if (studentId) {
      const rows = await listSubmissions(asgId, studentId).catch(() => [])
      setSubs(rows)
      const row = nextRoster.students.find((s) => s.studentId === studentId)
      setComment(row?.comment || '')
    } else {
      setSubs([])
    }
  }

  useEffect(() => {
    let cancelled = false
    setAssignment(null)
    setLoadError(false)
    getAssignment(id).then(async (a) => {
      if (cancelled) return
      setAssignment(a)
      setLoadError(!a)
      if (!a) {
        setSubs([])
        setRoster(null)
        return
      }
      try {
        if (fromTeacher) {
          await loadTeacherData(a.id, reviewStudentId || undefined)
        } else {
          const list = await listSubmissions(a.id)
          if (!cancelled) setSubs(list)
        }
      } catch {
        if (!cancelled) {
          setSubs([])
          setRoster(null)
        }
      }
    })
    return () => {
      cancelled = true
    }
  }, [id, fromTeacher, reviewStudentId])

  const doneMap = useMemo(() => {
    const m = new Map<string, AssignmentSubmission>()
    for (const s of subs) {
      m.set(`${s.bookId}:${s.subject}:${s.sId}`, s)
    }
    return m
  }, [subs])

  const doneCount = assignment
    ? assignment.parts.filter((p) => isPartSubmitted(subs, p.bookId, p.subject, p.sId)).length
    : 0

  const assignedCount = roster?.assignedCount ?? assignment?.assignedCount ?? 0
  const submittedCount = roster?.submittedCount ?? assignment?.submittedCount ?? 0
  const reviewStudent = roster?.students.find((s) => s.studentId === reviewStudentId) || null
  const missing = (roster?.students || []).filter((s) => s.status !== 'submitted')
  const submitted = (roster?.students || []).filter((s) => s.status === 'submitted')
  const alreadyAssigned = new Set((roster?.students || []).map((s) => s.studentId))

  const copyLink = async () => {
    const url = absoluteAppUrl(`/assignment/${id}`)
    try {
      await navigator.clipboard.writeText(url)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1600)
    } catch {
      prompt('复制链接：', url)
    }
  }

  const addStudents = async () => {
    const ids = selectedIds(adding)
    if (!ids.length || !assignment) return
    setSavingAdd(true)
    try {
      const next = await addRecipients(assignment.id, ids)
      setRoster(next)
      setAdding({})
      setAssignment(await getAssignment(assignment.id))
    } catch (e) {
      alert(e instanceof Error ? e.message : '添加失败')
    } finally {
      setSavingAdd(false)
    }
  }

  const saveComment = async () => {
    if (!assignment || !reviewStudentId) return
    setSavingComment(true)
    try {
      const saved = await saveReview(assignment.id, reviewStudentId, comment)
      setComment(saved.comment)
      setRoster(await getRoster(assignment.id))
    } catch (e) {
      alert(e instanceof Error ? e.message : '点评保存失败')
    } finally {
      setSavingComment(false)
    }
  }

  if (!assignment) {
    return (
      <div className={`shell ${fromTeacher ? 'teacher-shell' : ''}`}>
        <div className="teacher-empty">
          <p>{loadError ? `找不到作业 #${id}` : '加载作业…'}</p>
          <Link className="btn" to={fromTeacher ? '/teacher/assignments' : '/student'}>
            {fromTeacher ? '返回作业列表' : '返回学生端'}
          </Link>
        </div>
      </div>
    )
  }

  const openStudent = (sid: string) => {
    navigate(`/assignment/${assignment.id}?from=teacher&student=${encodeURIComponent(sid)}`)
  }

  return (
    <div className={`shell ${fromTeacher ? 'teacher-shell' : ''}`}>
      <header className="teacher-header asg-hub-header">
        <div>
          <div className="asg-hub-nav">
            {fromTeacher ? (
              <>
                <Link className="exam-back" to="/teacher/assignments">
                  ← 作业包与布置
                </Link>
                {reviewStudentId ? (
                  <Link className="exam-back" to={`/assignment/${assignment.id}?from=teacher`}>
                    返回名单
                  </Link>
                ) : (
                  <Link className="exam-back" to="/teacher">
                    教师端
                  </Link>
                )}
              </>
            ) : (
              <Link className="exam-back" to="/student">
                ← 学生端
              </Link>
            )}
          </div>
          <h1>{assignment.title}</h1>
          <p>
            {assignment.subject === 'listening' ? '听力' : '阅读'} · {assignment.parts.length}{' '}
            Part · 任意顺序完成 · 每 Part 交卷后锁定
            {fromTeacher ? ` · 已布置 ${assignedCount} 人 / 已交 ${submittedCount} 人` : ''}
          </p>
        </div>
        <div className="asg-hub-actions">
          {fromTeacher && !reviewStudentId ? (
            <button type="button" className="btn ghost" onClick={copyLink}>
              {copied ? '已复制' : '复制学生链接'}
            </button>
          ) : null}
          <span className="asg-progress">
            {fromTeacher
              ? `已布置 ${assignedCount} 人 / 已交 ${submittedCount} 人`
              : `进度 ${doneCount}/${assignment.parts.length}`}
          </span>
        </div>
      </header>

      {!fromTeacher && assignment.comment ? (
        <section className="teacher-comment-card">
          <h2>老师点评</h2>
          <p>{assignment.comment}</p>
        </section>
      ) : null}

      {fromTeacher && reviewStudent ? (
        <section className="teacher-section">
          <div className="teacher-section-head">
            <h2>
              {reviewStudent.name} · {reviewStudent.studentId}
            </h2>
            <span>{statusLabel(reviewStudent)}</span>
          </div>
          <label className="field">
            <span>点评</span>
            <textarea
              rows={4}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="写给学生看的评语"
            />
          </label>
          <button type="button" className="btn" disabled={savingComment} onClick={saveComment}>
            {savingComment ? '保存中…' : '保存点评'}
          </button>
        </section>
      ) : null}

      {fromTeacher && !reviewStudentId ? (
        <>
          <section className="teacher-section">
            <div className="teacher-section-head">
              <h2>未交明细</h2>
              <span>{missing.length} 人</span>
            </div>
            {missing.length === 0 ? (
              <p className="empty-hint">全部学生都已交齐。</p>
            ) : (
              <ul className="roster-list">
                {missing.map((row) => (
                  <li key={row.studentId}>
                    <button type="button" className="roster-row" onClick={() => openStudent(row.studentId)}>
                      <div>
                        <strong>{row.name}</strong>
                        <span>{row.studentId}</span>
                      </div>
                      <span className={`pill ${row.status === 'partial' ? '' : 'warn'}`}>
                        {statusLabel(row)}
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="teacher-section">
            <div className="teacher-section-head">
              <h2>已交作业</h2>
              <span>{submitted.length} 人</span>
            </div>
            {submitted.length === 0 ? (
              <p className="empty-hint">还没有学生交齐。</p>
            ) : (
              <ul className="roster-list">
                {submitted.map((row) => (
                  <li key={row.studentId}>
                    <button type="button" className="roster-row" onClick={() => openStudent(row.studentId)}>
                      <div>
                        <strong>{row.name}</strong>
                        <span>
                          {row.studentId}
                          {row.comment ? ' · 已点评' : ''}
                        </span>
                      </div>
                      <span className="pill ok">查看并点评</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="teacher-section">
            <div className="teacher-section-head">
              <h2>追加学生</h2>
            </div>
            <StudentPicker
              students={students}
              selected={adding}
              onChange={setAdding}
              excludeIds={alreadyAssigned}
              emptyHint="没有可追加的学生。"
            />
            <button
              type="button"
              className="btn"
              disabled={!selectedIds(adding).length || savingAdd}
              onClick={addStudents}
            >
              {savingAdd ? '添加中…' : `把所选学生加入作业`}
            </button>
          </section>
        </>
      ) : null}

      <ul className="asg-part-list">
        {assignment.parts.map((p) => {
          const key = `${p.bookId}:${p.subject}:${p.sId}`
          const sub = doneMap.get(key)
          const done = Boolean(sub)
          let to = assignmentPartPath(assignment.id, p, done, {
            ...(fromTeacher ? { from: 'teacher' } : {}),
            ...(reviewStudentId ? { student: reviewStudentId } : {}),
          })
          return (
            <li key={key}>
              <Link to={to} className={`asg-part-card ${done ? 'done' : ''}`}>
                <div>
                  <strong>
                    C{p.bookId} Test {p.testNo} Part {p.sPart}
                  </strong>
                  <span>
                    {p.label} · {p.questionCount} 题
                  </span>
                </div>
                {fromTeacher && !reviewStudentId ? (
                  <div className="asg-part-status">
                    <span className="pill">打开试卷</span>
                  </div>
                ) : fromTeacher && reviewStudentId ? (
                  <div className="asg-part-status">
                    {done && sub ? (
                      <>
                        <span className="pill ok">已交 · 查看作答</span>
                        <span>
                          {sub.correct}/{sub.total}（{sub.pct}%）
                        </span>
                      </>
                    ) : (
                      <span className="pill warn">该生尚未提交</span>
                    )}
                  </div>
                ) : done && sub ? (
                  <div className="asg-part-status">
                    <span className="pill ok">已完成 · 锁定</span>
                    <span>
                      {sub.correct}/{sub.total}（{sub.pct}%）
                    </span>
                  </div>
                ) : (
                  <span className="pill">未完成 · 开始作答</span>
                )}
              </Link>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
