import { Navigate, Route, Routes } from 'react-router-dom'
import Portal from './pages/Portal'
import Home from './pages/Home'
import Exam from './pages/Exam'
import Result from './pages/Result'
import Overview from './pages/Overview'
import PartHistory from './pages/PartHistory'
import TeacherHome from './pages/TeacherHome'
import TeacherBank from './pages/TeacherBank'
import TeacherAssignmentNew, {
  TeacherAssignmentList,
  TeacherPackNew,
} from './pages/TeacherAssignment'
import AssignmentHub from './pages/AssignmentHub'
import MockHub from './pages/MockHub'
import MockExam from './pages/MockExam'
import MockHistory from './pages/MockHistory'
import './App.css'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Portal />} />
      <Route path="/student" element={<Home />} />
      <Route path="/student/overview" element={<Overview />} />
      <Route path="/student/history" element={<PartHistory />} />
      <Route path="/student/mock" element={<MockHub />} />
      <Route path="/student/mock/history" element={<MockHistory />} />
      <Route path="/student/mock/:subject" element={<MockExam />} />
      <Route path="/overview" element={<Navigate to="/student/overview" replace />} />
      <Route path="/teacher" element={<TeacherHome />} />
      <Route path="/teacher/bank" element={<TeacherBank />} />
      <Route path="/teacher/assignments" element={<TeacherAssignmentList />} />
      <Route path="/teacher/assignments/new" element={<TeacherAssignmentNew />} />
      <Route path="/teacher/packs/new" element={<TeacherPackNew />} />
      <Route path="/assignment/:id" element={<AssignmentHub />} />
      <Route path="/exam/:bookId/:subject/:sId" element={<Exam />} />
      <Route path="/exam/:subject/:sId" element={<Exam />} />
      <Route path="/result/:subject/:sId" element={<Result />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
