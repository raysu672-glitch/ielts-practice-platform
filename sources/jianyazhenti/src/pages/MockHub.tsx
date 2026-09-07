import { useEffect } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { loadCatalog, loadManifest } from '../lib/data'
import {
  MOCK_BOOK_MAX,
  MOCK_BOOK_MIN,
  migrateLocalMockSets,
} from '../lib/mockExam'

const SUBJECTS = [
  {
    id: 'reading',
    title: '阅读',
    en: 'Reading',
    ready: true,
    desc: '从 C7–C21 随机抽取未做过的 Part 1–3，限时 60 分钟，到时自动交卷。',
  },
  {
    id: 'listening',
    title: '听力',
    en: 'Listening',
    ready: true,
    desc: '从 C7–C21 随机抽取未做过的 Part 1–4。开始后先空 15 秒，再依次播放各 Part，Part 之间空 30 秒，Part 4 结束后空 120 秒自动交卷。',
  },
  {
    id: 'writing',
    title: '写作',
    en: 'Writing',
    ready: false,
    desc: '写作模拟考即将开放。',
  },
  {
    id: 'speaking',
    title: '口语',
    en: 'Speaking',
    ready: false,
    desc: '口语模拟考即将开放。',
  },
] as const

export default function MockHub() {
  const navigate = useNavigate()
  const [search] = useSearchParams()
  const qs = search.toString()

  useEffect(() => {
    void migrateLocalMockSets().catch(() => {
      /* 未登录时跳过迁移 */
    })
    let cancelled = false
    ;(async () => {
      try {
        const books = await loadCatalog()
        if (cancelled) return
        await Promise.all(
          books
            .filter((book) => book.bookId >= MOCK_BOOK_MIN && book.bookId <= MOCK_BOOK_MAX)
            .map((book) => loadManifest(book.bookId).catch(() => null)),
        )
      } catch {
        /* 预加载失败时，进入考试页会再试 */
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="shell mock-hub">
      <header className="home-hero">
        <Link className="exam-back portal-back" to="/">
          ← 返回入口
        </Link>
        <h1 className="brand">
          模拟<span>考</span>
        </h1>
        <p className="hero-lead">
          按官方题型组一套完整模考。阅读、听力从剑雅 C7–C21 抽取你还没做过的 Part；写作和口语稍后开放。
        </p>
        <div className="hero-actions">
          <Link className="btn ghost" to={`/student/mock/history${qs ? `?${qs}` : ''}`}>
            历史记录
          </Link>
        </div>
      </header>
      <section className="mock-hub-grid">
        {SUBJECTS.map((item) => (
          <article className={`mock-hub-card ${item.ready ? '' : 'is-soon'}`} key={item.id}>
            <div className="mock-hub-kicker">{item.en}</div>
            <h2>{item.title}</h2>
            <p>{item.desc}</p>
            {item.ready ? (
              <button
                type="button"
                className="btn"
                onClick={() =>
                  navigate(`/student/mock/${item.id}${qs ? `?${qs}` : ''}`)
                }
              >
                开始模考
              </button>
            ) : (
              <span className="mock-hub-soon">即将开放</span>
            )}
          </article>
        ))}
      </section>
    </div>
  )
}
