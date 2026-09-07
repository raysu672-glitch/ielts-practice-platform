import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listAssignments } from '../lib/assignments'

export default function TeacherHome() {
  const [assigned, setAssigned] = useState(0)

  useEffect(() => {
    listAssignments()
      .then((items) => setAssigned(items.length))
      .catch(() => setAssigned(0))
  }, [])

  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back portal-back" to="/">
            ← 返回入口
          </Link>
          <h1>作业</h1>
          <p>布置作业、管理作业包，或直接打开任意试卷查看题目。作业保存在服务器，学生登录后即可看到。</p>
        </div>
      </header>

      <div className="portal-cards teacher-home-cards">
        <Link className="portal-card" to="/teacher/assignments">
          <span className="portal-card-kicker">作业</span>
          <strong>作业包与布置</strong>
          <span>
            从预设/自建作业包勾选布置，或自由选题。当前已布置 {assigned} 份。
          </span>
        </Link>
        <Link className="portal-card portal-card-teacher" to="/teacher/bank">
          <span className="portal-card-kicker">题库</span>
          <strong>浏览全部题目</strong>
          <span>按册号查看听力 / 阅读全部 Part，可打开试卷预览与试做。</span>
        </Link>
      </div>

      <div className="teacher-home-links">
        <Link className="btn ghost" to="/teacher/packs/new">
          新建作业包
        </Link>
        <Link className="btn ghost" to="/teacher/assignments/new">
          自由选题布置
        </Link>
      </div>
    </div>
  )
}
