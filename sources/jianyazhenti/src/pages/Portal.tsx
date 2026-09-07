import { Link } from 'react-router-dom'

export default function Portal() {
  return (
    <div className="shell portal-shell">
      <header className="portal-hero">
        <h1 className="brand">
          模考<span>中心</span>
        </h1>
        <p className="hero-lead">选择身份进入对应工作台。学生自由练题；教师布置作业、查看题库。</p>
      </header>

      <div className="portal-cards">
        <Link className="portal-card" to="/student">
          <span className="portal-card-kicker">Student</span>
          <strong>学生端</strong>
          <span>自由练习听力 / 阅读，查看本机成绩；通过链接完成教师布置的作业。</span>
        </Link>
        <Link className="portal-card portal-card-teacher" to="/teacher">
          <span className="portal-card-kicker">Teacher</span>
          <strong>教师端</strong>
          <span>作业包库、布置作业，并浏览全部题库试卷。</span>
        </Link>
      </div>
    </div>
  )
}
