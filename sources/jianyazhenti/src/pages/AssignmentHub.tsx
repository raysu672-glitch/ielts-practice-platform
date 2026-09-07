import { useEffect, useMemo, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import {
  assignmentPartPath,
  getAssignment,
  isPartSubmitted,
  listSubmissions,
  type Assignment,
  type AssignmentSubmission,
} from '../lib/assignments'
import { absoluteAppUrl } from '../lib/embed'

export default function AssignmentHub() {
  const { id = '' } = useParams()
  const [search] = useSearchParams()
  const fromTeacher = search.get('from') === 'teacher'
  const [assignment, setAssignment] = useState<Assignment | null>(null)
  const [subs, setSubs] = useState<AssignmentSubmission[]>([])
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    let cancelled = false
    getAssignment(id).then(async (a) => {
      if (cancelled) return
      setAssignment(a)
      if (!a) {
        setSubs([])
        return
      }
      try {
        const list = await listSubmissions(a.id)
        if (!cancelled) setSubs(list)
      } catch {
        if (!cancelled) setSubs([])
      }
    })
    return () => {
      cancelled = true
    }
  }, [id])

  const doneMap = useMemo(() => {
    const m = new Map<string, AssignmentSubmission>()
    for (const s of subs) {
      m.set(`${s.bookId}:${s.subject}:${s.sId}`, s)
    }
    return m
  }, [subs])

  const studentCountByPart = useMemo(() => {
    const m = new Map<string, number>()
    const seen = new Map<string, Set<string>>()
    for (const s of subs) {
      const key = `${s.bookId}:${s.subject}:${s.sId}`
      if (!seen.has(key)) seen.set(key, new Set())
      seen.get(key)!.add(s.studentId)
    }
    for (const [key, set] of seen) m.set(key, set.size)
    return m
  }, [subs])

  const doneCount = assignment
    ? assignment.parts.filter((p) =>
        isPartSubmitted(subs, p.bookId, p.subject, p.sId),
      ).length
    : 0

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

  if (!assignment) {
    return (
      <div className={`shell ${fromTeacher ? 'teacher-shell' : ''}`}>
        <div className="teacher-empty">
          <p>找不到作业 #{id}</p>
          <Link className="btn" to={fromTeacher ? '/teacher/assignments' : '/student'}>
            {fromTeacher ? '返回作业列表' : '返回学生端'}
          </Link>
        </div>
      </div>
    )
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
                <Link className="exam-back" to="/teacher">
                  教师端
                </Link>
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
            {fromTeacher ? ' · 可将下方链接发给学生' : ''}
          </p>
        </div>
        <div className="asg-hub-actions">
          {fromTeacher ? (
            <button type="button" className="btn ghost" onClick={copyLink}>
              {copied ? '已复制' : '复制学生链接'}
            </button>
          ) : null}
          <span className="asg-progress">
            进度 {doneCount}/{assignment.parts.length}
          </span>
        </div>
      </header>

      <ul className="asg-part-list">
        {assignment.parts.map((p) => {
          const key = `${p.bookId}:${p.subject}:${p.sId}`
          const sub = doneMap.get(key)
          const done = Boolean(sub)
          let to = assignmentPartPath(assignment.id, p, done)
          if (fromTeacher) {
            const [path, qs = ''] = to.split('?')
            const q = new URLSearchParams(qs)
            q.set('from', 'teacher')
            to = `${path}?${q.toString()}`
          }
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
                {fromTeacher ? (
                  <div className="asg-part-status">
                    <span className="pill">{studentCountByPart.get(key) || 0} 人已交</span>
                    <span className="pill">打开试卷</span>
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
