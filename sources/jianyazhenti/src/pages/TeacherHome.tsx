import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import SubjectTabs from '../components/SubjectTabs'
import {
  getRoster,
  listAssignments,
  type Assignment,
  type RosterStudent,
} from '../lib/assignments'
import { canBuildPacks, subjectLabel, type PackSubject } from '../lib/packSubjects'
import { loadTeacherPackSubject, peekLocalPackSubject, saveTeacherPackSubject } from '../lib/teacherPrefs'

type StatusRow = Assignment & {
  missing: RosterStudent[]
  partial: RosterStudent[]
}

function studentLabel(row: RosterStudent) {
  return row.name || row.studentId
}

export default function TeacherHome() {
  const [rows, setRows] = useState<StatusRow[]>([])
  const [loading, setLoading] = useState(true)
  const [teacherId, setTeacherId] = useState('')
  const [subject, setSubject] = useState<PackSubject>(peekLocalPackSubject)

  useEffect(() => {
    let cancelled = false
    loadTeacherPackSubject().then((prefs) => {
      if (cancelled) return
      setTeacherId(prefs.teacherId)
      setSubject(prefs.subject)
    })
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    listAssignments()
      .then(async (items) => {
        const next = await Promise.all(
          items.map(async (item) => {
            try {
              const roster = await getRoster(item.id)
              return {
                ...item,
                assignedCount: roster.assignedCount,
                submittedCount: roster.submittedCount,
                missing: roster.students.filter((s) => s.status === 'missing'),
                partial: roster.students.filter((s) => s.status === 'partial'),
              }
            } catch {
              return { ...item, missing: [], partial: [] }
            }
          }),
        )
        if (!cancelled) setRows(next)
      })
      .catch(() => {
        if (!cancelled) setRows([])
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const visible = useMemo(
    () => rows.filter((row) => row.subject === subject),
    [rows, subject],
  )

  const changeSubject = (next: PackSubject) => {
    setSubject(next)
    void saveTeacherPackSubject(teacherId, next)
  }

  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back portal-back" to="/">
            ← 返回入口
          </Link>
          <h1>作业</h1>
          <p>布置作业时必须选择学生。作业保存在服务器，只有被指定的学生登录后才能看到。</p>
        </div>
      </header>

      <div className="teacher-subject-bar">
        <span className="filter-label">科目</span>
        <SubjectTabs value={subject} onChange={changeSubject} />
      </div>

      <div className="portal-cards teacher-home-cards">
        <Link className="portal-card" to="/teacher/assignments">
          <span className="portal-card-kicker">作业</span>
          <strong>作业包与布置</strong>
          <span>
            从预设/自建作业包勾选布置，或自由选题。当前本科已布置 {visible.length} 份。
          </span>
        </Link>
        <Link className="portal-card" to="/student/jijing?from=teacher">
          <span className="portal-card-kicker">当季机经</span>
          <strong>当季机经真题</strong>
          <span>当季写作机经真题（A 类），Task 1 / Task 2 共 39 篇，按题型与话题浏览。</span>
        </Link>
        <Link className="portal-card portal-card-teacher" to="/teacher/bank">
          <span className="portal-card-kicker">题库</span>
          <strong>浏览全部题目</strong>
          <span>按册号查看听力 / 阅读全部 Part，可打开试卷预览与试做。</span>
        </Link>
      </div>

      <div className="teacher-home-links">
        {canBuildPacks(subject) ? (
          <>
            <Link className="btn ghost" to="/teacher/packs/new">
              新建作业包
            </Link>
            <Link className="btn ghost" to="/teacher/assignments/new">
              自由选题布置
            </Link>
          </>
        ) : (
          <p className="filter-hint">口语作业包即将开放，目前可布置听力、阅读和写作。</p>
        )}
      </div>

      <section className="teacher-section teacher-home-status">
        <div className="teacher-section-head">
          <h2>提交情况 · {subjectLabel(subject)}</h2>
          <span>{loading ? '加载中' : `${visible.length} 份`}</span>
        </div>
        {loading ? (
          <p className="empty-hint">加载提交情况…</p>
        ) : visible.length === 0 ? (
          <p className="empty-hint">
            {canBuildPacks(subject)
              ? '这个科目还没有你布置的作业。布置后，这里会显示每个学生的提交进度。'
              : '口语作业即将开放。'}
          </p>
        ) : (
          <ul className="asg-list">
            {visible.map((a) => {
              const assigned = a.assignedCount || 0
              const submitted = a.submittedCount || 0
              const done = assigned > 0 && submitted >= assigned
              return (
                <li key={a.id}>
                  <Link to={`/assignment/${a.id}?from=teacher`} className="asg-list-card">
                    <div>
                      <strong>{a.title}</strong>
                      <span>
                        {subjectLabel(a.subject)} · {a.parts.length} Part · 已布置 {assigned} 人
                        / 已交 {submitted} 人
                      </span>
                      {done ? (
                        <span className="status-line ok">已交齐</span>
                      ) : (
                        <span className="status-line warn">
                          {a.partial.length
                            ? `部分完成：${a.partial.map(studentLabel).join('、')}`
                            : ''}
                          {a.partial.length && a.missing.length ? ' · ' : ''}
                          {a.missing.length
                            ? `未交：${a.missing.map(studentLabel).join('、')}`
                            : a.partial.length
                              ? ''
                              : '还没有人提交'}
                        </span>
                      )}
                    </div>
                    <span className="asg-id">{done ? '查看' : '催交 / 查看'}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        )}
      </section>
    </div>
  )
}
