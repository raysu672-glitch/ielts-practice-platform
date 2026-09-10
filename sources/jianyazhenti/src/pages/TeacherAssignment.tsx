import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  createAssignment,
  createPack,
  deleteAssignment,
  deletePack,
  listAllPacks,
  listAssignments,
  listTeacherStudents,
  packQuestionCount,
  publishFromPacks,
  type Assignment,
  type AssignmentPack,
  type PartRef,
  type TeacherStudent,
} from '../lib/assignments'
import StudentPicker, { selectedIds } from '../components/StudentPicker'
import SubjectTabs from '../components/SubjectTabs'
import {
  canBuildPacks,
  isExamSubject,
  isWritingSubject,
  subjectLabel,
  type ExamSubject,
  type PackSubject,
} from '../lib/packSubjects'
import { loadTeacherPackSubject, peekLocalPackSubject, saveTeacherPackSubject } from '../lib/teacherPrefs'
import {
  groupByTest,
  loadCatalog,
  loadManifest,
  parseTestNo,
  type BookInfo,
} from '../lib/data'
import type { Manifest, ManifestPart } from '../types'
import { topicToPart, writingLessons, writingTaskLabel } from '../lib/writingTopics'

function partId(bookId: number, sId: number) {
  return `${bookId}:${sId}`
}

function toRef(bookId: number, subject: ExamSubject, p: ManifestPart): PartRef {
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

function packKindLabel(pack: AssignmentPack) {
  if (pack.builtin) return '内置'
  if (pack.fromAdmin || pack.createdBy === 'admin') return '管理员'
  return '我的'
}

function packBooks(pack: AssignmentPack) {
  if (isWritingSubject(pack.subject)) return []
  return [...new Set(pack.parts.map((p) => p.bookId))].sort((a, b) => b - a)
}

function packSummary(pack: AssignmentPack) {
  if (isWritingSubject(pack.subject)) {
    const first = pack.parts[0]
    const lessons = [...new Set(pack.parts.map((p) => p.lesson || p.testNo).filter(Boolean))]
    const lessonText = lessons.length ? `第${lessons.join('/')}课` : '写作'
    const task = writingTaskLabel(first?.task || 'task2')
    if (pack.parts.length === 1) {
      return `${subjectLabel(pack.subject)} · ${lessonText} · ${task}`
    }
    return `${subjectLabel(pack.subject)} · ${lessonText} · ${pack.parts.length} 题`
  }
  const books = packBooks(pack)
  const q = packQuestionCount(pack)
  return `${subjectLabel(pack.subject)}${books.length ? ` · ${books.map((id) => `C${id}`).join(' / ')}` : ''} · ${pack.parts.length} Part · ${q} 题`
}

function PackCard({
  pack,
  checked,
  onToggle,
  onDeleted,
}: {
  pack: AssignmentPack
  checked: boolean
  onToggle: () => void
  onDeleted?: () => void
}) {
  const kind = packKindLabel(pack)
  return (
    <label className={`pack-card ${isWritingSubject(pack.subject) ? 'writing-pack' : ''} ${checked ? 'selected' : ''}`}>
      <input type="checkbox" checked={checked} onChange={onToggle} />
      <div className="pack-card-body">
        <div className="pack-card-top">
          <strong>{pack.title}</strong>
          <span className={`pill ${kind === '管理员' ? 'ok' : pack.builtin ? '' : 'ok'}`}>
            {kind}
          </span>
        </div>
        <p>{packSummary(pack)}</p>
        {pack.description ? <p className="pack-desc">{pack.description}</p> : null}
        {!pack.builtin && onDeleted ? (
          <button
            type="button"
            className="btn-text pack-delete"
            onClick={(e) => {
              e.preventDefault()
              if (!confirm(`删除作业包「${pack.title}」？`)) return
              onDeleted()
            }}
          >
            删除
          </button>
        ) : null}
      </div>
    </label>
  )
}

/** 教师首页：从作业包选取布置 + 已布置列表 */
export function TeacherAssignmentList() {
  const navigate = useNavigate()
  const [packs, setPacks] = useState<AssignmentPack[]>([])
  const [items, setItems] = useState<Assignment[]>([])
  const [loading, setLoading] = useState(true)
  const [teacherId, setTeacherId] = useState('')
  const [subject, setSubject] = useState<PackSubject>(peekLocalPackSubject)
  const [bookFilter, setBookFilter] = useState<'all' | number>('all')
  const [lessonFilter, setLessonFilter] = useState<'all' | number>('all')
  const [selected, setSelected] = useState<Record<string, boolean>>({})
  const [titlePrefix, setTitlePrefix] = useState('')
  const [publishing, setPublishing] = useState(false)
  const [students, setStudents] = useState<TeacherStudent[]>([])
  const [pickedStudents, setPickedStudents] = useState<Record<string, boolean>>({})

  const refreshPacks = () => {
    setLoading(true)
    listAllPacks()
      .then(setPacks)
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    refreshPacks()
    listAssignments().then(setItems).catch(() => setItems([]))
    listTeacherStudents().then(setStudents).catch(() => setStudents([]))
    loadTeacherPackSubject().then((prefs) => {
      setTeacherId(prefs.teacherId)
      setSubject(prefs.subject)
    })
  }, [])

  const changeSubject = (next: PackSubject) => {
    setSubject(next)
    setBookFilter('all')
    setLessonFilter('all')
    void saveTeacherPackSubject(teacherId, next)
  }

  const customPacks = useMemo(
    () =>
      packs.filter(
        (p) => !p.builtin && p.subject === subject,
      ),
    [packs, subject],
  )

  const builtinPacks = useMemo(
    () =>
      packs.filter((p) => {
        if (!p.builtin || p.subject !== subject) return false
        if (isWritingSubject(subject)) {
          if (lessonFilter !== 'all') {
            const hasLesson = p.parts.some((x) => (x.lesson || x.testNo) === lessonFilter)
            if (!hasLesson) return false
          }
          return true
        }
        if (bookFilter !== 'all') {
          const hasBook = p.parts.some((x) => x.bookId === bookFilter)
          if (!hasBook) return false
        }
        return true
      }),
    [packs, subject, bookFilter, lessonFilter],
  )

  const visibleAssignments = useMemo(
    () => items.filter((row) => row.subject === subject),
    [items, subject],
  )

  const lessonOptions = useMemo(() => {
    const set = new Set<number>()
    for (const p of packs) {
      if (!p.builtin || !isWritingSubject(p.subject)) continue
      for (const part of p.parts) {
        const lesson = part.lesson || part.testNo
        if (lesson) set.add(lesson)
      }
    }
    return [...set].sort((a, b) => a - b)
  }, [packs])

  const bookOptions = useMemo(() => {
    const set = new Set<number>()
    for (const p of packs) {
      if (!p.builtin || p.subject !== subject) continue
      for (const part of p.parts) set.add(part.bookId)
    }
    return [...set].sort((a, b) => b - a)
  }, [packs, subject])

  const pickedPacks = useMemo(
    () => packs.filter((p) => selected[p.id]),
    [packs, selected],
  )

  const toggle = (id: string) => {
    setSelected((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  const publish = async () => {
    if (!pickedPacks.length) return
    const studentIds = selectedIds(pickedStudents)
    if (!studentIds.length) {
      alert('请选择要布置的学生')
      return
    }
    setPublishing(true)
    try {
      const created = await publishFromPacks(pickedPacks, titlePrefix.trim(), studentIds)
      setSelected({})
      setItems(await listAssignments())
      if (created.length === 1) navigate(`/assignment/${created[0].id}?from=teacher`)
      else alert(`已布置 ${created.length} 份作业（${studentIds.length} 名学生）`)
    } catch (e) {
      alert(e instanceof Error ? e.message : '布置失败')
    } finally {
      setPublishing(false)
    }
  }

  const removePack = (id: string) => {
    setSelected((prev) => {
      const next = { ...prev }
      delete next[id]
      return next
    })
  }

  return (
    <div className="shell teacher-shell">
      <header className="teacher-header">
        <div>
          <Link className="exam-back" to="/teacher">
            ← 教师端
          </Link>
          <h1>作业包与布置</h1>
          <p>管理员建立的作业包所有老师都能看到，并排在最前面。每位老师只能看到自己布置的作业。</p>
        </div>
        <div className="teacher-header-actions">
          <Link className="btn ghost" to="/teacher/bank">
            浏览题库
          </Link>
          {canBuildPacks(subject) ? (
            <>
              <Link className="btn ghost" to="/teacher/packs/new">
                新建作业包
              </Link>
              <Link className="btn ghost" to="/teacher/assignments/new">
                自由选题
              </Link>
            </>
          ) : null}
        </div>
      </header>

      <div className="teacher-subject-bar">
        <span className="filter-label">科目</span>
        <SubjectTabs value={subject} onChange={changeSubject} />
      </div>

      <div className="teacher-layout assign-home">
        <section className="teacher-section assign-custom">
            <div className="teacher-section-head">
              <h2>作业包</h2>
              <span>{customPacks.length} 个</span>
            </div>
            <p className="filter-hint">管理员共享的作业包在最前，后面是你自己建的包。</p>
            {loading ? (
              <p className="empty-hint">加载作业包…</p>
            ) : customPacks.length === 0 ? (
              <div className="teacher-empty">
                <p>
                  {canBuildPacks(subject)
                    ? '这个科目还没有管理员共享或你自建的作业包。'
                    : '口语作业包即将开放。'}
                </p>
                {canBuildPacks(subject) ? (
                  <Link className="btn" to="/teacher/packs/new">
                    去新建
                  </Link>
                ) : null}
              </div>
            ) : (
              <div className="pack-grid">
                {customPacks.map((pack) => (
                  <PackCard
                    key={pack.id}
                    pack={pack}
                    checked={Boolean(selected[pack.id])}
                    onToggle={() => toggle(pack.id)}
                    onDeleted={
                      pack.createdBy === teacherId
                        ? () => {
                            deletePack(pack.id)
                              .then(() => {
                                removePack(pack.id)
                                refreshPacks()
                              })
                              .catch((err) => {
                                alert(err instanceof Error ? err.message : '删除失败')
                              })
                          }
                        : undefined
                    }
                  />
                ))}
              </div>
            )}
        </section>

        <div className="assign-main">
          <section className="teacher-section">
            <div className="teacher-section-head">
              <h2>内置作业包</h2>
              <span>{builtinPacks.length} 个</span>
            </div>
            <div className="teacher-filters pack-filters">
              {isExamSubject(subject) ? (
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
              ) : isWritingSubject(subject) ? (
                <div className="filter-row">
                  <span className="filter-label">课次</span>
                  <div className="book-switch">
                    <button
                      type="button"
                      className={`book-chip ${lessonFilter === 'all' ? 'active' : ''}`}
                      onClick={() => setLessonFilter('all')}
                    >
                      全部
                    </button>
                    {lessonOptions.map((lesson) => (
                      <button
                        key={lesson}
                        type="button"
                        className={`book-chip ${lessonFilter === lesson ? 'active' : ''}`}
                        onClick={() => setLessonFilter(lesson)}
                      >
                        第{lesson}课
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="filter-hint">口语暂无内置作业包。</p>
              )}
            </div>
            {loading ? (
              <p className="empty-hint">加载作业包…</p>
            ) : builtinPacks.length === 0 ? (
              <p className="empty-hint">没有匹配的内置作业包。</p>
            ) : (
              <div
                className={`pack-grid pack-grid-scroll ${
                  isWritingSubject(subject) ? 'writing-pack-grid' : ''
                }`}
              >
                {builtinPacks.map((pack) => (
                  <PackCard
                    key={pack.id}
                    pack={pack}
                    checked={Boolean(selected[pack.id])}
                    onToggle={() => toggle(pack.id)}
                  />
                ))}
              </div>
            )}
          </section>

          <section className="teacher-section">
            <div className="teacher-section-head">
              <h2>已布置</h2>
              <span>{visibleAssignments.length} 份</span>
            </div>
            {visibleAssignments.length === 0 ? (
              <p className="empty-hint">
                {canBuildPacks(subject)
                  ? '这个科目还没有你布置的作业。勾选作业包并在右侧选择学生后即可发布。'
                  : '口语作业即将开放。'}
              </p>
            ) : (
              <ul className="asg-list">
                {visibleAssignments.map((a) => (
                  <li key={a.id}>
                    <Link to={`/assignment/${a.id}?from=teacher`} className="asg-list-card">
                      <div>
                        <strong>{a.title}</strong>
                        <span>
                          {subjectLabel(a.subject)} · {a.parts.length} Part · 已布置{' '}
                          {a.assignedCount || 0} 人 / 已交 {a.submittedCount || 0} 人
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

        <aside className="teacher-side assign-side">
          <div className="teacher-panel">
            <div className="teacher-panel-head">
              <h2>已选作业包</h2>
              <span>{pickedPacks.length} 个</span>
            </div>
            {pickedPacks.length === 0 ? (
              <p className="empty-hint">从左侧勾选自建或内置作业包。</p>
            ) : (
              <ul className="picked-list">
                {pickedPacks.map((p) => (
                  <li key={p.id}>
                    <div>
                      <strong>{p.title}</strong>
                      <span>{packKindLabel(p)}</span>
                    </div>
                    <button type="button" className="btn-text" onClick={() => removePack(p.id)}>
                      移除
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="teacher-panel">
            <div className="teacher-panel-head">
              <h2>布置给学生</h2>
              <span>必选</span>
            </div>
            <StudentPicker
              students={students}
              selected={pickedStudents}
              onChange={setPickedStudents}
              emptyHint="还没有学生账号。请先在教师端添加学生。"
            />
            <label className="field pack-prefix">
              <span>标题前缀（可选）</span>
              <input
                value={titlePrefix}
                onChange={(e) => setTitlePrefix(e.target.value)}
                placeholder="例如 Week 3"
              />
            </label>
            <div className="pack-publish-meta">
              <span>
                {pickedPacks.length} 个包 · {selectedIds(pickedStudents).length} 名学生
              </span>
              <button
                type="button"
                className="btn teacher-publish"
                disabled={!pickedPacks.length || !selectedIds(pickedStudents).length || publishing}
                onClick={publish}
              >
                {publishing ? '布置中…' : '布置所选作业包'}
              </button>
            </div>
          </div>
        </aside>
      </div>
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
  const [teacherId, setTeacherId] = useState('')
  const [subject, setSubject] = useState<PackSubject>(peekLocalPackSubject)
  const [bookFilter, setBookFilter] = useState<number | null>(null)
  const [selected, setSelected] = useState<Record<string, PartRef>>({})
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [saving, setSaving] = useState(false)
  const [students, setStudents] = useState<TeacherStudent[]>([])
  const [pickedStudents, setPickedStudents] = useState<Record<string, boolean>>({})

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
    if (mode === 'assign') {
      listTeacherStudents()
        .then((rows) => {
          if (!cancelled) setStudents(rows)
        })
        .catch(() => {
          if (!cancelled) setStudents([])
        })
    }
    loadTeacherPackSubject().then((prefs) => {
      if (!cancelled) {
        setTeacherId(prefs.teacherId)
        setSubject(prefs.subject)
      }
    })
    return () => {
      cancelled = true
    }
  }, [mode])

  const switchSubject = (next: PackSubject) => {
    if (next === subject) return
    setSubject(next)
    setSelected({})
    void saveTeacherPackSubject(teacherId, next)
  }

  const catalogParts = useMemo(() => {
    if (!isExamSubject(subject) || bookFilter == null) return []
    const m = manifests[bookFilter]
    if (!m) return []
    return m.parts[subject].filter((p) => !p.error)
  }, [manifests, bookFilter, subject])

  const groups = useMemo(() => groupByTest(catalogParts), [catalogParts])
  const writingGroups = useMemo(() => writingLessons(), [])
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
        const studentIds = selectedIds(pickedStudents)
        if (!studentIds.length) {
          alert('请选择要布置的学生')
          setSaving(false)
          return
        }
        const asg = await createAssignment({
          title: title.trim() || defaultAssignTitle(subject, picked.length),
          subject,
          parts: picked,
          studentIds,
        })
        navigate(`/assignment/${asg.id}?from=teacher`)
      }
    } catch (e) {
      alert(e instanceof Error ? e.message : '保存失败')
      setSaving(false)
    }
  }

  if (error && isExamSubject(subject)) return <div className="shell status">{error}</div>
  if (!isWritingSubject(subject) && (!books.length || bookFilter == null)) {
    return <div className="shell status">{error || '加载题库…'}</div>
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
              : '临时选题并立刻布置；必须选择布置给哪些学生。常用组合请存成作业包。'}
          </p>
        </div>
      </header>

      <div className="teacher-layout">
        <section className="teacher-browser">
          <div className="teacher-filters">
            <div className="filter-row">
              <span className="filter-label">科目</span>
              <SubjectTabs value={subject} onChange={switchSubject} />
              <span className="filter-hint">切换科目会清空已选</span>
            </div>

            {isExamSubject(subject) ? (
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
            ) : isWritingSubject(subject) ? (
              <p className="filter-hint">从强化段写作题库勾选题目，可跨课次组合。</p>
            ) : null}
          </div>

          <div className="teacher-catalog">
            {isWritingSubject(subject) ? (
              writingGroups.map((group) => (
                <div className="teacher-test" key={group.lesson}>
                  <h3>{group.title}</h3>
                  <div className="teacher-part-grid writing-topic-grid">
                    {group.topics.map((topic) => {
                      const ref = topicToPart(topic)
                      const id = partId(ref.bookId, ref.sId)
                      const checked = Boolean(selected[id])
                      return (
                        <label
                          key={id}
                          className={`teacher-part-card writing-topic-card ${checked ? 'selected' : ''}`}
                        >
                          <input
                            type="checkbox"
                            checked={checked}
                            onChange={() => toggle(ref)}
                          />
                          <span className="teacher-part-body">
                            <strong>
                              {writingTaskLabel(topic.task)} · {topic.title}
                            </strong>
                            <span className="teacher-topic-prompt">{topic.prompt}</span>
                            {topic.examMeta ? <span>{topic.examMeta}</span> : null}
                          </span>
                        </label>
                      )
                    })}
                  </div>
                </div>
              ))
            ) : !isExamSubject(subject) ? (
              <p className="empty-hint">口语作业包即将开放，目前可布置听力、阅读和写作。</p>
            ) : bookFilter == null || !manifests[bookFilter] ? (
              <p className="empty-hint">加载 C{bookFilter}…</p>
            ) : groups.length === 0 ? (
              <p className="empty-hint">该册暂无可用 Part</p>
            ) : (
              groups.map(([testNo, parts]) => (
                <div className="teacher-test" key={testNo}>
                  <h3>Test {testNo}</h3>
                  <div className="teacher-part-grid">
                    {parts.map((p) => {
                      const ref = toRef(bookFilter as number, subject as ExamSubject, p)
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
              <h2>{isWritingSubject(subject) ? '已选题目' : '已选 Part'}</h2>
              <span>{picked.length} {isWritingSubject(subject) ? '题' : '个'}</span>
            </div>
            {picked.length === 0 ? (
              <p className="empty-hint">
                {isWritingSubject(subject) ? '从左侧勾选写作题目。' : '从左侧勾选 Part。'}
              </p>
            ) : (
              <ul className="picked-list">
                {picked.map((p) => {
                  const id = partId(p.bookId, p.sId)
                  return (
                    <li key={id}>
                      <div>
                        <strong>
                          {isWritingSubject(subject)
                            ? `${writingTaskLabel(p.task || '')} · 第${p.lesson || p.testNo}课`
                            : `C${p.bookId} T${p.testNo} P${p.sPart}`}
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
            {!isPack && (
              <div className="field">
                <span>布置给学生（必选）</span>
                <StudentPicker
                  students={students}
                  selected={pickedStudents}
                  onChange={setPickedStudents}
                  emptyHint="还没有学生账号。"
                />
              </div>
            )}
            <div className="teacher-stats">
              <div>
                <strong>{picked.length}</strong>
                <span>{isWritingSubject(subject) ? '题目数' : 'Part 数'}</span>
              </div>
              {isExamSubject(subject) ? (
                <div>
                  <strong>{totalQ}</strong>
                  <span>总题数</span>
                </div>
              ) : null}
            </div>
            <button
              type="button"
              className="btn teacher-publish"
              disabled={
                !canBuildPacks(subject) ||
                !picked.length ||
                saving ||
                (!isPack && !selectedIds(pickedStudents).length)
              }
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

function defaultAssignTitle(subject: PackSubject, n: number) {
  return isWritingSubject(subject)
    ? `${subjectLabel(subject)}作业 · ${n} 题`
    : `${subjectLabel(subject)}专项 · ${n} Part`
}

function defaultPackTitle(subject: PackSubject, n: number) {
  return isWritingSubject(subject)
    ? `${subjectLabel(subject)}作业包 · ${n} 题`
    : `${subjectLabel(subject)}作业包 · ${n} Part`
}

export default function TeacherAssignmentNew() {
  return <PartPickerPage mode="assign" />
}

export function TeacherPackNew() {
  return <PartPickerPage mode="pack" />
}
