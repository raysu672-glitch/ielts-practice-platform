import { useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  listMockWritingTopics,
  type MockWritingTopic,
} from '../lib/writingMockTopics'
import { postStudentJson } from '../lib/studentApi'

const TASK1_MIN_WORDS = 150
const TASK2_MIN_WORDS = 250

function wordCount(text: string) {
  return text.trim() ? text.trim().split(/\s+/).length : 0
}

const TASK1_TYPES = ['柱状图', '曲线图', '表格', '混合图', '地图', '流程图']
const TASK2_TOPICS = ['教育类', '环境类', '生活类', '政府类', '经济类']

export default function WritingJijingBank() {
  const [search] = useSearchParams()
  const fromTeacher = search.get('from') === 'teacher'
  const backTo = fromTeacher ? '/teacher' : '/student'
  const topics = useMemo(() => listMockWritingTopics(), [])

  const [task, setTask] = useState<'task1' | 'task2'>('task1')
  const [typeFilter, setTypeFilter] = useState('全部')
  const [active, setActive] = useState<MockWritingTopic | null>(null)
  const [essay, setEssay] = useState('')
  const [saving, setSaving] = useState(false)
  const [done, setDone] = useState(false)
  const [doneId, setDoneId] = useState<number | null>(null)

  const pool = topics.filter((t) => t.task === task)
  const filters = task === 'task1' ? TASK1_TYPES : TASK2_TOPICS
  const visible =
    typeFilter === '全部' ? pool : pool.filter((t) => (task === 'task1' ? t.qType : t.topic) === typeFilter)

  const minWords = active?.task === 'task1' ? TASK1_MIN_WORDS : TASK2_MIN_WORDS
  const words = useMemo(() => wordCount(essay), [essay])

  const openPractice = (topic: MockWritingTopic) => {
    setActive((prev) => (prev?.id === topic.id ? null : topic))
    setEssay('')
    setDone(false)
    setDoneId(null)
  }

  const submit = async () => {
    if (!active || saving) return
    if (!essay.trim()) {
      alert('请先写下作文再交卷')
      return
    }
    if (words < minWords) {
      const ok = window.confirm(
        `当前 ${words} 词，低于要求 ${minWords} 词，仍要提交吗？`,
      )
      if (!ok) return
    }
    setSaving(true)
    try {
      const details = [
        {
          kind: 'jianya_jijing_writing',
          task: active.task,
          topicId: active.id,
          title: active.title,
          prompt: active.prompt,
          essay: essay.trim(),
          words,
          submittedAt: new Date().toISOString(),
        },
      ]
      await postStudentJson('/api/student/test-records', {
        module_type: 'writing_jijing',
        module_name: '当季机经写作',
        test_type: 'practice',
        score: words,
        correct_count: words,
        total_count: minWords,
        duration_seconds: 0,
        started_at: new Date().toISOString(),
        ended_at: new Date().toISOString(),
        details,
      })
      setDone(true)
      setDoneId(active.id)
    } catch (err) {
      alert(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="shell jijing-shell">
      <header className="home-hero">
        <Link className="exam-back portal-back" to={backTo}>
          ← {fromTeacher ? '返回教师端' : '返回学生端'}
        </Link>
        <h1 className="brand">
          当季<span>机经</span>
        </h1>
        <p className="hero-lead">
          当季写作机经真题（A 类）。Task 1 共 {topics.filter((t) => t.task === 'task1').length}{' '}
          篇，Task 2 共 {topics.filter((t) => t.task === 'task2').length} 篇，按题型/话题筛选，点开即可练习。
        </p>
      </header>

      <div className="jijing-tabs" role="tablist">
        <button
          type="button"
          className={`jijing-tab ${task === 'task1' ? 'active' : ''}`}
          onClick={() => {
            setTask('task1')
            setTypeFilter('全部')
            setActive(null)
          }}
        >
          Task 1 小作文
        </button>
        <button
          type="button"
          className={`jijing-tab ${task === 'task2' ? 'active' : ''}`}
          onClick={() => {
            setTask('task2')
            setTypeFilter('全部')
            setActive(null)
          }}
        >
          Task 2 大作文
        </button>
      </div>

      <div className="jijing-filters" role="tablist">
        {['全部', ...filters].map((f) => (
          <button
            key={f}
            type="button"
            className={`book-chip ${typeFilter === f ? 'active' : ''}`}
            onClick={() => setTypeFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <section className="jijing-list">
        {visible.length === 0 ? (
          <p className="empty-hint">该筛选下暂无题目。</p>
        ) : (
          visible.map((t) => (
            <article className="jijing-card" key={t.id}>
              <button
                type="button"
                className="jijing-card-head"
                onClick={() => openPractice(t)}
              >
                <div>
                  <strong>{t.title}</strong>
                  <span className="jijing-card-meta">{t.examMeta}</span>
                </div>
                <span className="jijing-card-toggle">
                  {done && doneId === t.id ? '已交' : active?.id === t.id ? '收起' : '练习'}
                </span>
              </button>
              {active?.id === t.id ? (
                <div className="jijing-practice">
                  <div className="jijing-prompt">
                    <span className="mock-writing-task-label">
                      {task === 'task1' ? 'WRITING TASK 1' : 'WRITING TASK 2'}
                    </span>
                    {t.image ? (
                      <div className="jijing-chart">
                        <img src={t.image} alt={t.title} loading="lazy" />
                      </div>
                    ) : null}
                    <p className="mock-writing-prompt-text">{t.prompt}</p>
                  </div>
                  <label className="mock-writing-field">
                    <textarea
                      value={essay}
                      onChange={(e) => setEssay(e.target.value)}
                      placeholder="Write your essay here…"
                    />
                    <div className="mock-writing-field-meta">
                      <span className={words >= minWords ? 'is-ok' : ''}>
                        {words} 词（要求 ≥ {minWords}）
                      </span>
                      {done ? <span>已交</span> : null}
                    </div>
                  </label>
                  {!done ? (
                    <div className="mock-writing-actions">
                      <button
                        type="button"
                        className="btn teacher-publish"
                        disabled={saving}
                        onClick={() => void submit()}
                      >
                        {saving ? '提交中…' : '交卷'}
                      </button>
                    </div>
                  ) : null}
                </div>
              ) : null}
            </article>
          ))
        )}
      </section>
    </div>
  )
}