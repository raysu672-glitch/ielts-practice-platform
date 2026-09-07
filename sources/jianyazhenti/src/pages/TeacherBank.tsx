import { Link } from 'react-router-dom'
import BankCatalog from '../components/BankCatalog'

export default function TeacherBank() {
  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back" to="/teacher">
            ← 教师端
          </Link>
          <h1>题库浏览</h1>
          <p>教师可查看全部册号与试卷；打开后可预览作答，作答保存在本机，与学生作业隔离。</p>
        </div>
        <div className="teacher-header-actions">
          <Link className="btn ghost" to="/teacher/assignments">
            去布置作业
          </Link>
        </div>
      </header>

      <BankCatalog
        examTo={(subject, sId, bookId) =>
          `/exam/${bookId}/${subject}/${sId}?from=teacher`
        }
        sectionLead="选择册号与 Part，打开试卷查看题目。"
      />
    </div>
  )
}
