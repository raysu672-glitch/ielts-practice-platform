import { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import BankCatalog from '../components/BankCatalog'
import { listAssignments, type Assignment } from '../lib/assignments'
import {
  listPartsForFilter,
  loadLocalDoneKeys,
  loadServerDoneKeys,
  pickRandomUnused,
} from '../lib/randomTest'
import type { Subject } from '../types'

function subjectLabel(subject: Assignment['subject']) {
  return subject === 'listening' ? '听力' : '阅读'
}

function examPath(subject: string, sId: number, bookId?: number) {
  const q = new URLSearchParams(window.location.search)
  const prefix = bookId ? `/exam/${bookId}/${subject}/${sId}` : `/exam/${subject}/${sId}`
  const qs = q.toString()
  return qs ? `${prefix}?${qs}` : prefix
}

export default function Home() {
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const partFilter = search.get('subject') && search.get('part')
  const testMode = search.get('mode') === 'test'
  const lockSubject = search.get('subject')
  const lockPart = Number(search.get('part') || 0)
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [pickError, setPickError] = useState('')
  const [picking, setPicking] = useState(testMode && !!lockSubject && lockPart >= 1)
  const searchText = search.toString()

  useEffect(() => {
    if (partFilter) return
    listAssignments()
      .then(setAssignments)
      .catch(() => setAssignments([]))
  }, [partFilter])

  useEffect(() => {
    if (!testMode) return
    if (lockSubject !== 'listening' && lockSubject !== 'reading') return
    if (lockPart < 1 || lockPart > 4) return
    let cancelled = false
    setPicking(true)
    setPickError('')
    ;(async () => {
      try {
        const pool = await listPartsForFilter(lockSubject as Subject, lockPart)
        if (cancelled) return
        if (!pool.length) {
          setPickError('本题库没有对应 Part，请改用学习入口自选试卷。')
          setPicking(false)
          return
        }
        const params = new URLSearchParams(searchText)
        const moduleType =
          params.get('module_type') ||
          `${lockSubject === 'reading' ? 'reading' : 'listening'}_p${lockPart}`
        const done = new Set([
          ...loadLocalDoneKeys(),
          ...(await loadServerDoneKeys(moduleType)),
        ])
        if (cancelled) return
        const paper = pickRandomUnused(pool, done)
        if (!paper) {
          setPickError('没有可抽的试卷。')
          setPicking(false)
          return
        }
        const q = new URLSearchParams(searchText)
        navigate(`/exam/${paper.bookId}/${paper.subject}/${paper.sId}?${q.toString()}`, {
          replace: true,
        })
      } catch (e) {
        if (!cancelled) {
          setPickError(e instanceof Error ? e.message : '抽题失败')
          setPicking(false)
        }
      }
    })()
    return () => {
      cancelled = true
    }
  }, [testMode, lockSubject, lockPart, navigate, searchText])

  if (testMode && (picking || pickError)) {
    return (
      <div className="shell">
        <p className="status">{pickError || '正在抽取一篇还没做过的试卷…'}</p>
      </div>
    )
  }

  return (
    <div className="shell">
      <header className="home-hero">
        <Link className="exam-back portal-back" to="/">
          ← 返回入口
        </Link>
        <h1 className="brand">
          学生<span>端</span>
        </h1>
        <p className="hero-lead">
          {partFilter
            ? '从进度页进入：只显示对应科目的 Part，点开即可作答。交卷后成绩会记入学习进度。'
            : '先完成老师布置的剑雅作业，也可以按册号自由练习听力与阅读。'}
        </p>
        {!partFilter ? (
        <div className="hero-actions">
          {!partFilter && assignments.length > 0 ? (
            <button
              className="btn"
              type="button"
              onClick={() => {
                document.getElementById('homework')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
              }}
            >
              查看作业（{assignments.length}）
            </button>
          ) : null}
          <Link className="btn ghost" to="/student/overview">
            成绩总览
          </Link>
          <button
            className="btn ghost"
            type="button"
            onClick={() => {
              document.getElementById('bank')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }}
          >
            自由练习
          </button>
        </div>
        ) : null}
      </header>

      {!partFilter ? (
      <section className="section" id="homework">
        <h2>老师布置的作业</h2>
        {assignments.length === 0 ? (
          <p className="empty-hint">暂时没有作业。老师在「作业」里布置后会显示在这里。</p>
        ) : (
          <ul className="asg-list">
            {assignments.map((a) => (
              <li key={a.id}>
                <Link to={`/assignment/${a.id}`} className="asg-list-card">
                  <div>
                    <strong>{a.title}</strong>
                    <span>
                      {subjectLabel(a.subject)} · {a.parts.length} Part ·{' '}
                      {new Date(a.createdAt).toLocaleString()}
                    </span>
                  </div>
                  <span className="asg-id">开始</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
      ) : null}

      <BankCatalog
        examTo={(subject, sId, bookId) => examPath(subject, sId, bookId)}
        sectionLead="按 Test 选择 Part，开始听力或阅读练习。自由练习的作答保存在本机浏览器。"
      />
    </div>
  )
}
