import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  getBookId,
  groupByTest,
  loadCatalog,
  loadManifest,
  setBookId,
  type BookInfo,
} from '../lib/data'
import type { Manifest, Subject } from '../types'

type Props = {
  examTo: (subject: Subject, sId: number, bookId: number) => string
  sectionTitle?: string
  sectionLead?: string
}

export default function BankCatalog({
  examTo,
  sectionTitle,
  sectionLead = '按 Test 选择 Part，开始听力或阅读。',
}: Props) {
  const [search] = useSearchParams()
  const lockSubject = (search.get('subject') === 'listening' || search.get('subject') === 'reading'
    ? search.get('subject')
    : null) as Subject | null
  const lockPart = Number(search.get('part') || 0)
  const partFilter = lockPart >= 1 && lockPart <= 4 ? lockPart : 0

  const [books, setBooks] = useState<BookInfo[]>([])
  const [bookId, setBookIdState] = useState(getBookId)
  const [manifest, setManifest] = useState<Manifest | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<Subject>(lockSubject || 'listening')

  useEffect(() => {
    loadCatalog()
      .then((list) => {
        setBooks(list)
        const current = getBookId()
        if (list.length && !list.some((b) => b.bookId === current)) {
          const next = list[0].bookId
          setBookId(next)
          setBookIdState(next)
        } else {
          setBookId(current)
          setBookIdState(current)
        }
      })
      .catch(() => setBooks([]))
  }, [])

  useEffect(() => {
    if (lockSubject) setTab(lockSubject)
  }, [lockSubject])

  useEffect(() => {
    setManifest(null)
    setError('')
    loadManifest(bookId)
      .then(setManifest)
      .catch((e: Error) => setError(e.message))
  }, [bookId])

  const groups = useMemo(() => {
    if (!manifest) return []
    const parts = manifest.parts[tab].filter((p) => !partFilter || p.sPart === partFilter)
    return groupByTest(parts)
  }, [manifest, tab, partFilter])

  const onPickBook = (id: number) => {
    setBookId(id)
    setBookIdState(id)
  }

  if (error && !manifest) return <div className="status">{error}</div>
  if (!manifest) return <div className="status">加载题库…</div>

  const listenN = manifest.parts.listening.filter((p) => !p.error).length
  const readN = manifest.parts.reading.filter((p) => !p.error).length
  const title = sectionTitle ?? `ACADEMIC C${manifest.bookId}`

  return (
    <>
      {books.length > 1 && (
        <div className="book-switch" role="tablist" aria-label="题库册号">
          {books.map((b) => (
            <button
              key={b.bookId}
              type="button"
              className={`book-chip ${b.bookId === bookId ? 'active' : ''}`}
              onClick={() => onPickBook(b.bookId)}
            >
              C{b.bookId}
            </button>
          ))}
        </div>
      )}

      <p className="bank-meta">
        当前题库：{manifest.label}（听力 {listenN} Part · 阅读{' '}
        {readN} Part）
      </p>

      <section className="section" id="bank">
        <h2>{title}</h2>
        <p>
          {partFilter
            ? `只显示${tab === 'reading' ? '阅读' : '听力'} Part ${partFilter}，点开即可作答。`
            : sectionLead}
        </p>

        {!lockSubject ? (
        <div className="tabs" role="tablist">
          <button
            type="button"
            className={`tab ${tab === 'listening' ? 'active' : ''}`}
            onClick={() => setTab('listening')}
          >
            听力 Listening
          </button>
          <button
            type="button"
            className={`tab ${tab === 'reading' ? 'active' : ''}`}
            onClick={() => setTab('reading')}
          >
            阅读 Reading
          </button>
        </div>
        ) : (
          <p className="bank-meta">科目：{tab === 'reading' ? '阅读' : '听力'} Part {partFilter || ''}</p>
        )}

        <div className="test-grid">
          {groups.map(([testNo, parts]) => (
            <article className="test-block" key={`${tab}-${testNo}`}>
              <h3>Test {testNo}</h3>
              <div className="part-list">
                {parts.map((p) => (
                  <Link
                    className="part-link"
                    key={p.sId}
                    to={examTo(tab, p.sId, bookId)}
                  >
                    <strong>Part {p.sPart}</strong>
                    <span>{p.questionCount} 题</span>
                  </Link>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}
