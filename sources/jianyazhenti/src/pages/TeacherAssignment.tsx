import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  createAssignment,
  createPack,
  deleteAssignment,
  deletePack,
  listAllPacks,
  listAssignments,
  packQuestionCount,
  publishFromPacks,
  type Assignment,
  type AssignmentPack,
  type PartRef,
} from '../lib/assignments'
import {
  groupByTest,
  loadCatalog,
  loadManifest,
  parseTestNo,
  type BookInfo,
} from '../lib/data'
import type { Manifest, ManifestPart, Subject } from '../types'

function partId(bookId: number, sId: number) {
  return `${bookId}:${sId}`
}

function toRef(bookId: number, subject: Subject, p: ManifestPart): PartRef {
  return {
    bookId,
    subject,
    sId: p.sId,
    testNo: parseTestNo(p.sName),
    sPart: p.sPart,
    label: p.sName.replace(/^【听力】|【阅读】/, '').trim(),
    questionCount: p.questionCount,
  }
}

function subjectLabel(s: Subject) {
  return s === 'listening' ? '听力' : '阅读'
}

/** 教师首页：从作业包选取布置 + 已布置列表 */
export function TeacherAssignmentList() {
  const navigate = useNavigate()
  const [packs, setPacks] = useState<AssignmentPack[]>([])
  const [items, setItems] = useState<Assignment[]>([])
  const [loading, setLoading] = useState(true)
  const [subjectFilter, setSubjectFilter] = useState<'all' | Subject>('all')
  const [bookFilter, setBookFilter] = useState<'all' | number>('all')
  const [selected, setSelected] = useState<Record<string, boolean>>({})
  const [titlePrefix, setTitlePrefix] = useState('')
  const [publishing, setPublishing] = useState(false)

  const refreshPacks = () => {
    setLoading(true)
    listAllPacks()
      .then(setPacks)
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    refreshPacks()
    listAssignments().then(setItems).catch(() => setItems([]))
  }, [])

  const bookOptions = useMemo(() => {
    const set = new Set<number>()
    for (const p of packs) {
      for (const part of p.parts) set.add(part.bookId)
    }
    return [...set].sort((a, b) => b - a)
  }, [packs])

  const visible = useMemo(() => {
    return packs.filter((p) => {
      if (subjectFilter !== 'all' && p.subject !== subjectFilter) return false
      if (bookFilter !== 'all') {
        const hasBook = p.parts.some((x) => x.bookId === bookFilter)
        if (!hasBook) return false
      }
      return true
    })
  }, [packs, subjectFilter, bookFilter])

  const pickedPacks = useMemo(
    () => packs.filter((p) => selected[p.id]),
    [packs, selected],
  )

  const toggle = (id: string) => {
    setSelected((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  const publish = async () => {
    if (!pickedPacks.length) return
    setPublishing(true)
    try {
      const created = await publishFromPacks(pickedPacks, titlePrefix.trim())
      setSelected({})
      setItems(await listAssignments())
      if (created.length === 1) navigate(`/assignment/${created[0].id}?from=teacher`)
      else alert(`已布置 ${created.length} 份作业`)
    } catch (e) {
      alert(e instanceof Error ? e.message : '布置失败')
    } finally {
      setPublishing(false)
    }
  }

  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back" to="/teacher">
            ← 教师端
          </Link>
          <h1>作业包与布置</h1>
          <p>先从预设作业包里勾选布置；也可自建作业包，或临时自由选题。</p>
        </div>
        <div className="teacher-header-actions">
          <Link className="btn ghost" to="/teacher/bank">
            浏览题库
          </Link>
          <Link className="btn ghost" to="/teacher/packs/new">
            新建作业包
          </Link>
          <Link className="btn ghost" to="/teacher/assignments/new">
            自由选题
          </Link>
        </div>
      </header>

      <section className="teacher-section">
        <div className="teacher-section-head">
          <h2>作业包库</h2>
          <span>{visible.length} 个可布置</span>
        </div>

        <div className="teacher-filters pack-filters">
          <div className="filter-row">
            <span className="filter-label">科目</span>
            <div className="tabs" role="tablist">
              {(
                [
                  ['all', '全部'],
                  ['listening', '听力'],
                  ['reading', '阅读'],
                ] as const
              ).map(([k, label]) => (
                <button
                  key={k}
                  type="button"
                  className={`tab ${subjectFilter === k ? 'active' : ''}`}
                  onClick={() => setSubjectFilter(k)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <div className="filter-row">
            <span className="filter-label">册号</span>
            <div className="book-switch">
              <button
                type="button"
                className={`book-chip ${bookFilter === 'all' ? 'active' : ''}`}
                onClick={() => setBookFilter('all')}
              >
                全部
              </button>
              {bookOptions.map((id) => (
                <button
                  key={id}
                  type="button"
                  className={`book-chip ${bookFilter === id ? 'active' : ''}`}
                  onClick={() => setBookFilter(id)}
                >
                  C{id}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <p className="empty-hint">加载作业包…</p>
        ) : visible.length === 0 ? (
          <div className="teacher-empty">
            <p>没有匹配的作业包。</p>
            <Link className="btn" to="/teacher/packs/new">
              去新建
            </Link>
          </div>
        ) : (
          <div className="pack-grid">
            {visible.map((pack) => {
              const checked = Boolean(selected[pack.id])
              const q = packQuestionCount(pack)
              return (
                <label key={pack.id} className={`pack-card ${checked ? 'selected' : ''}`}>
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => toggle(pack.id)}
                  />
                  <div className="pack-card-body">
                    <div className="pack-card-top">
                      <strong>{pack.title}</strong>
                      <span className={`pill ${pack.builtin ? '' : 'ok'}`}>
                        {pack.builtin ? '内置' : '自建'}
                      </span>
                    </div>
                    <p>
                      {subjectLabel(pack.subject)} · {pack.parts.length} Part · {q} 题
                    </p>
                    {pack.description ? <p className="pack-desc">{pack.description}</p> : null}
                    {!pack.builtin && (
                      <button
                        type="button"
                        className="btn-text pack-delete"
                        onClick={(e) => {
                          e.preventDefault()
                          if (!confirm(`删除作业包「${pack.title}」？`)) return
                          deletePack(pack.id)
                            .then(() => {
                              setSelected((prev) => {
                                const next = { ...prev }
                                delete next[pack.id]
                                return next
                              })
                              refreshPacks()
                            })
                            .catch((err) => {
                              alert(err instanceof Error ? err.message : '删除失败')
                            })
                        }}
                      >
                        删除
                      </button>
                    )}
                  </div>
                </label>
              )
            })}
          </div>
        )}

        <div className="pack-publish-bar">
          <label className="field pack-prefix">
            <span>标题前缀（可选）</span>
            <input
              value={titlePrefix}
              onChange={(e) => setTitlePrefix(e.target.value)}
              placeholder="例如 Week 3"
            />
          </label>
          <div className="pack-publish-meta">
            <span>已选 {pickedPacks.length} 个包</span>
            <button
              type="button"
              className="btn"
              disabled={!pickedPacks.length || publishing}
              onClick={publish}
            >
              {publishing ? '布置中…' : '布置所选作业包'}
            </button>
          </div>
        </div>
      </section>

      <section className="teacher-section">
        <div className="teacher-section-head">
          <h2>已布置</h2>
          <span>{items.length} 份</span>
        </div>
        {items.length === 0 ? (
          <p className="empty-hint">还没有布置给学生的作业。勾选上方作业包即可发布。</p>
        ) : (
          <ul className="asg-list">
            {items.map((a) => (
              <li key={a.id}>
                <Link to={`/assignment/${a.id}?from=teacher`} className="asg-list-card">
                  <div>
                    <strong>{a.title}</strong>
                    <span>
                      {subjectLabel(a.subject)} · {a.parts.length} Part ·{' '}
                      {new Date(a.createdAt).toLocaleString()}
                    </span>
                  </div>
                  <span className="asg-id">#{a.id}</span>
                </Link>
                <button
                  type="button"
                  className="btn-text"
                  onClick={() => {
                    if (!confirm(`删除作业「${a.title}」？`)) return
                    deleteAssignment(a.id)
                      .then(() => listAssignments())
                      .then(setItems)
                      .catch((err) => alert(err instanceof Error ? err.message : '删除失败'))
                  }}
                >
                  删除
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}

type PickerMode = 'assign' | 'pack'

/** 自由选题布置 / 新建作业包（共用选题 UI） */
function PartPickerPage({ mode }: { mode: PickerMode }) {
  const navigate = useNavigate()
  const [books, setBooks] = useState<BookInfo[]>([])
  const [manifests, setManifests] = useState<Record<number, Manifest>>({})
  const [error, setError] = useState('')
  const [subject, setSubject] = useState<Subject>('listening')
  const [bookFilter, setBookFilter] = useState<number | null>(null)
  const [selected, setSelected] = useState<Record<string, PartRef>>({})
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    let cancelled = false
    loadCatalog()
      .then(async (list) => {
        if (cancelled) return
        setBooks(list)
        if (list.length) setBookFilter((prev) => prev ?? list[0].bookId)
        const entries = await Promise.all(
          list.map(async (b) => {
            try {
              const m = await loadManifest(b.bookId)
              return [b.bookId, m] as const
            } catch {
              return null
            }
          }),
        )
        if (cancelled) return
        const map: Record<number, Manifest> = {}
        for (const e of entries) {
          if (e) map[e[0]] = e[1]
        }
        setManifests(map)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message || '无法加载题库')
      })
    return () => {
      cancelled = true
    }
  }, [])

  const switchSubject = (next: Subject) => {
    if (next === subject) return
    setSubject(next)
    setSelected({})
  }

  const catalogParts = useMemo(() => {
    if (bookFilter == null) return []
    const m = manifests[bookFilter]
    if (!m) return []
    return m.parts[subject].filter((p) => !p.error)
  }, [manifests, bookFilter, subject])

  const groups = useMemo(() => groupByTest(catalogParts), [catalogParts])
  const picked = useMemo(() => Object.values(selected), [selected])
  const totalQ = picked.reduce((s, p) => s + p.questionCount, 0)

  const toggle = (ref: PartRef) => {
    const id = partId(ref.bookId, ref.sId)
    setSelected((prev) => {
      const next = { ...prev }
      if (next[id]) delete next[id]
      else next[id] = ref
      return next
    })
  }

  const save = async () => {
    if (!picked.length) return
    setSaving(true)
    try {
      if (mode === 'pack') {
        await createPack({
          title: title.trim() || defaultPackTitle(subject, picked.length),
          subject,
          description,
          parts: picked,
        })
        navigate('/teacher/assignments')
      } else {
        const asg = await createAssignment({
          title: title.trim() || defaultAssignTitle(subject, picked.length),
          subject,
          parts: picked,
        })
        navigate(`/assignment/${asg.id}?from=teacher`)
      }
    } catch (e) {
      alert(e instanceof Error ? e.message : '保存失败')
      setSaving(false)
    }
  }

  if (error) return <div className="shell status">{error}</div>
  if (!books.length || bookFilter == null) {
    return <div className="shell status">加载题库…</div>
  }

  const isPack = mode === 'pack'

  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back" to="/teacher/assignments">
            ← 作业包与布置
          </Link>
          <h1>{isPack ? '新建作业包' : '自由选题布置'}</h1>
          <p>
            {isPack
              ? '预设好后进入作业包库，之后可反复选取布置。'
              : '临时选题并立刻布置；常用组合请存成作业包。'}
          </p>
        </div>
      </header>

      <div className="teacher-layout">
        <section className="teacher-browser">
          <div className="teacher-filters">
            <div className="filter-row">
              <span className="filter-label">科目</span>
              <div className="tabs" role="tablist">
                <button
                  type="button"
                  className={`tab ${subject === 'listening' ? 'active' : ''}`}
                  onClick={() => switchSubject('listening')}
                >
                  听力 Listening
                </button>
                <button
                  type="button"
                  className={`tab ${subject === 'reading' ? 'active' : ''}`}
                  onClick={() => switchSubject('reading')}
                >
                  阅读 Reading
                </button>
              </div>
              <span className="filter-hint">切换科目会清空已选</span>
            </div>

            <div className="filter-row">
              <span className="filter-label">册号</span>
              <div className="book-switch" role="tablist" aria-label="题库册号">
                {books.map((b) => (
                  <button
                    key={b.bookId}
                    type="button"
                    className={`book-chip ${bookFilter === b.bookId ? 'active' : ''}`}
                    onClick={() => setBookFilter(b.bookId)}
                  >
                    C{b.bookId}
                  </button>
                ))}
              </div>
              <span className="filter-hint">可跨册勾选</span>
            </div>
          </div>

          <div className="teacher-catalog">
            {!manifests[bookFilter] ? (
              <p className="empty-hint">加载 C{bookFilter}…</p>
            ) : groups.length === 0 ? (
              <p className="empty-hint">该册暂无可用 Part</p>
            ) : (
              groups.map(([testNo, parts]) => (
                <div className="teacher-test" key={testNo}>
                  <h3>Test {testNo}</h3>
                  <div className="teacher-part-grid">
                    {parts.map((p) => {
                      const ref = toRef(bookFilter, subject, p)
                      const id = partId(ref.bookId, ref.sId)
                      const checked = Boolean(selected[id])
                      return (
                        <label
                          key={id}
                          className={`teacher-part-card ${checked ? 'selected' : ''}`}
                        >
                          <input
                            type="checkbox"
                            checked={checked}
                            onChange={() => toggle(ref)}
                          />
                          <span className="teacher-part-body">
                            <strong>
                              C{ref.bookId} · Part {ref.sPart}
                            </strong>
                            <span>
                              {ref.label} · {ref.questionCount} 题
                            </span>
                          </span>
                        </label>
                      )
                    })}
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        <aside className="teacher-side">
          <div className="teacher-panel">
            <div className="teacher-panel-head">
              <h2>已选 Part</h2>
              <span>{picked.length} 个</span>
            </div>
            {picked.length === 0 ? (
              <p className="empty-hint">从左侧勾选 Part。</p>
            ) : (
              <ul className="picked-list">
                {picked.map((p) => {
                  const id = partId(p.bookId, p.sId)
                  return (
                    <li key={id}>
                      <div>
                        <strong>
                          C{p.bookId} T{p.testNo} P{p.sPart}
                        </strong>
                        <span>{p.label}</span>
                      </div>
                      <button type="button" className="btn-text" onClick={() => toggle(p)}>
                        移除
                      </button>
                    </li>
                  )
                })}
              </ul>
            )}
          </div>

          <div className="teacher-panel">
            <div className="teacher-panel-head">
              <h2>{isPack ? '作业包信息' : '作业信息'}</h2>
            </div>
            <label className="field">
              <span>标题</span>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder={
                  isPack
                    ? defaultPackTitle(subject, picked.length || 3)
                    : defaultAssignTitle(subject, picked.length || 3)
                }
              />
            </label>
            {isPack && (
              <label className="field">
                <span>说明（可选）</span>
                <input
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="例如：适合入门班第一周"
                />
              </label>
            )}
            <div className="teacher-stats">
              <div>
                <strong>{picked.length}</strong>
                <span>Part 数</span>
              </div>
              <div>
                <strong>{totalQ}</strong>
                <span>总题数</span>
              </div>
            </div>
            <button
              type="button"
              className="btn teacher-publish"
              disabled={!picked.length || saving}
              onClick={save}
            >
              {saving ? '保存中…' : isPack ? '保存作业包' : '发布作业'}
            </button>
          </div>
        </aside>
      </div>
    </div>
  )
}

function defaultAssignTitle(subject: Subject, n: number) {
  return `${subjectLabel(subject)}专项 · ${n} Part`
}

function defaultPackTitle(subject: Subject, n: number) {
  return `${subjectLabel(subject)}作业包 · ${n} Part`
}

export default function TeacherAssignmentNew() {
  return <PartPickerPage mode="assign" />
}

export function TeacherPackNew() {
  return <PartPickerPage mode="pack" />
}
