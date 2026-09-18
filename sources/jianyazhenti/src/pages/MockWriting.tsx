import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { pickMockWritingTopic, type MockWritingTopic } from '../lib/writingMockTopics'
import { postStudentJson } from '../lib/studentApi'
import { formatClock } from '../lib/mockExam'

const WRITING_LIMIT_SEC = 60 * 60
const TASK1_MIN_WORDS = 150
const TASK2_MIN_WORDS = 250

function wordCount(text: string) {
  return text.trim() ? text.trim().split(/\s+/).length : 0
}

export default function MockWriting() {
  const [search] = useSearchParams()
  const backTo = `/student/mock${search.toString() ? `?${search.toString()}` : ''}`

  const [started, setStarted] = useState(false)
  const [locked, setLocked] = useState(false)
  const [activeTask, setActiveTask] = useState<'task1' | 'task2'>('task1')
  const [task1Topic, setTask1Topic] = useState<MockWritingTopic | null>(null)
  const [task2Topic, setTask2Topic] = useState<MockWritingTopic | null>(null)
  const [task1Essay, setTask1Essay] = useState('')
  const [task2Essay, setTask2Essay] = useState('')
  const [remaining, setRemaining] = useState(WRITING_LIMIT_SEC)
  const [saving, setSaving] = useState(false)
  const [submitHint, setSubmitHint] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const startedAtRef = useRef(0)
  const tickRef = useRef<number | null>(null)
  const deadlineRef = useRef(0)

  const currentTopic = activeTask === 'task1' ? task1Topic : task2Topic
  const currentEssay = activeTask === 'task1' ? task1Essay : task2Essay
  const setCurrentEssay = activeTask === 'task1' ? setTask1Essay : setTask2Essay
  const minWords = activeTask === 'task1' ? TASK1_MIN_WORDS : TASK2_MIN_WORDS
  const words = useMemo(() => wordCount(currentEssay), [currentEssay])

  const task1Words = useMemo(() => wordCount(task1Essay), [task1Essay])
  const task2Words = useMemo(() => wordCount(task2Essay), [task2Essay])

  useEffect(() => {
    setTask1Topic(pickMockWritingTopic('task1'))
    setTask2Topic(pickMockWritingTopic('task2'))
  }, [])

  const clearTick = () => {
    if (tickRef.current) {
      window.clearInterval(tickRef.current)
      tickRef.current = null
    }
  }

  const startCountdown = (seconds: number, onDone: () => void) => {
    clearTick()
    deadlineRef.current = Date.now() + seconds * 1000
    setRemaining(seconds)
    tickRef.current = window.setInterval(() => {
      const left = Math.max(0, Math.ceil((deadlineRef.current - Date.now()) / 1000))
      setRemaining(left)
      if (left <= 0) {
        clearTick()
        onDone()
      }
    }, 200)
  }

  const startExam = () => {
    if (!task1Topic || !task2Topic) return
    startedAtRef.current = Date.now()
    setStarted(true)
    startCountdown(WRITING_LIMIT_SEC, () => {
      void submitExam(true)
    })
  }

  const submitExam = async (auto = false) => {
    if (locked || saving) return
    if (!auto && !window.confirm('确认交卷？提交后不可再修改。')) return
    if (!task1Essay.trim() && !task2Essay.trim()) {
      alert('请至少完成一篇作文再交卷')
      return
    }
    setSaving(true)
    clearTick()
    setSubmitHint(auto ? '时间到，正在交卷…' : '正在交卷…')
    try {
      const durationSeconds = Math.max(0, Math.round((Date.now() - startedAtRef.current) / 1000))
      const details = [
        {
          kind: 'jianya_writing_mock',
          task1: task1Topic
            ? {
                topicId: task1Topic.id,
                title: task1Topic.title,
                prompt: task1Topic.prompt,
                essay: task1Essay.trim(),
                words: task1Words,
              }
            : null,
          task2: task2Topic
            ? {
                topicId: task2Topic.id,
                title: task2Topic.title,
                prompt: task2Topic.prompt,
                essay: task2Essay.trim(),
                words: task2Words,
              }
            : null,
          submittedAt: new Date().toISOString(),
        },
      ]
      await postStudentJson('/api/student/test-records', {
        module_type: 'mock_writing',
        module_name: '写作模拟考',
        test_type: 'mock_exam',
        score: task1Words + task2Words,
        correct_count: task1Words + task2Words,
        total_count: TASK1_MIN_WORDS + TASK2_MIN_WORDS,
        duration_seconds: durationSeconds,
        started_at: new Date(startedAtRef.current).toISOString(),
        ended_at: new Date().toISOString(),
        details,
      })
      setLocked(true)
      setSubmitted(true)
      setSubmitHint('')
    } catch (err) {
      setSubmitHint('')
      alert(err instanceof Error ? err.message : '交卷失败')
    } finally {
      setSaving(false)
    }
  }

  useEffect(() => {
    return () => clearTick()
  }, [])

  useEffect(() => {
    const onLeave = (e: BeforeUnloadEvent) => {
      if (started && !locked) {
        e.preventDefault()
        e.returnValue = ''
      }
    }
    window.addEventListener('beforeunload', onLeave)
    return () => window.removeEventListener('beforeunload', onLeave)
  }, [started, locked])

  if (!task1Topic || !task2Topic) {
    return <div className="exam-status">正在抽取写作题目…</div>
  }

  if (submitted) {
    return (
      <div className="exam-shell">
        <header className="exam-chrome">
          <div className="exam-chrome-left">
            <Link className="exam-back" to={backTo}>
              ← 模拟考
            </Link>
            <div className="exam-badge">WRITING MOCK</div>
          </div>
        </header>
        <main className="mock-writing-result">
          <div className="mock-writing-result-card">
            <h2>写作模拟考已交卷</h2>
            <p>
              Task 1：{task1Topic.title}（{task1Words} 词）
            </p>
            <p>
              Task 2：{task2Topic.title}（{task2Words} 词）
            </p>
            <p>总词数：{task1Words + task2Words} 词</p>
            <div className="mock-writing-result-actions">
              <Link className="btn" to={backTo}>
                返回模拟考
              </Link>
              <Link className="btn ghost" to={`/student/mock/history${search.toString() ? `?${search.toString()}` : ''}`}>
                查看历史记录
              </Link>
            </div>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="exam-shell mock-writing-exam">
      <header className="exam-chrome">
        <div className="exam-chrome-left">
          <Link
            className="exam-back"
            to={backTo}
            onClick={(e) => {
              if (started && !locked && !window.confirm('考试进行中，确定离开？')) {
                e.preventDefault()
              }
            }}
          >
            ← 模拟考
          </Link>
          <div className="exam-badge">WRITING MOCK</div>
          <div className="exam-chrome-meta">
            <strong>写作模拟考</strong>
            <span>限时 60 分钟</span>
          </div>
        </div>
        <div className="exam-chrome-right">
          {started && !locked ? (
            <div className={`exam-timer ${remaining <= 300 ? 'is-warn' : ''}`}>
              剩余 {formatClock(remaining)}
            </div>
          ) : null}
          {locked ? (
            <Link className="exam-tool" to={`/student/mock/history${search.toString() ? `?${search.toString()}` : ''}`}>
              历史记录
            </Link>
          ) : started ? (
            <button type="button" className="exam-tool primary" onClick={() => void submitExam(false)} disabled={saving}>
              {saving ? '交卷中…' : '交卷'}
            </button>
          ) : null}
        </div>
      </header>

      <div className="mock-writing-tabs" role="tablist">
        <button
          type="button"
          className={`mock-writing-tab ${activeTask === 'task1' ? 'active' : ''}`}
          onClick={() => setActiveTask('task1')}
        >
          <span>Task 1 小作文</span>
          <small>
            {task1Words}/{TASK1_MIN_WORDS} 词
          </small>
        </button>
        <button
          type="button"
          className={`mock-writing-tab ${activeTask === 'task2' ? 'active' : ''}`}
          onClick={() => setActiveTask('task2')}
        >
          <span>Task 2 大作文</span>
          <small>
            {task2Words}/{TASK2_MIN_WORDS} 词
          </small>
        </button>
      </div>

      {submitHint ? <div className="mock-submit-hint">{submitHint}</div> : null}

      {!started ? (
        <div className="mock-start-overlay">
          <div className="mock-start-card">
            <h2>写作模拟考</h2>
            <p>已随机抽取 Task 1 和 Task 2 各一篇，限时 60 分钟。</p>
            <ul>
              <li>Task 1：{task1Topic.title}（建议 20 分钟，≥150 词）</li>
              <li>Task 2：{task2Topic.title}（建议 40 分钟，≥250 词）</li>
            </ul>
            <p>点击开始后计时，到时自动交卷。可自由切换 Task。</p>
            <button type="button" className="btn" onClick={startExam}>
              开始考试
            </button>
          </div>
        </div>
      ) : (
        <main className="mock-writing-main">
          <section className="mock-writing-prompt">
            <span className="mock-writing-task-label">
              {activeTask === 'task1' ? 'WRITING TASK 1' : 'WRITING TASK 2'}
            </span>
            <h1>{currentTopic?.title}</h1>
            <p className="mock-writing-prompt-meta">
              {activeTask === 'task1'
                ? 'You should spend about 20 minutes on this task. Write at least 150 words.'
                : 'You should spend about 40 minutes on this task. Write at least 250 words.'}
              {currentTopic?.examMeta ? ` · ${currentTopic.examMeta}` : ''}
            </p>
            {currentTopic?.image ? (
              <div className="jijing-chart">
                <img src={currentTopic.image} alt={currentTopic.title} />
              </div>
            ) : null}
            <p className="mock-writing-prompt-text">{currentTopic?.prompt}</p>
          </section>

          <section className="mock-writing-compose">
            <label className="mock-writing-field">
              <textarea
                value={currentEssay}
                onChange={(e) => setCurrentEssay(e.target.value)}
                readOnly={locked}
                placeholder="Write your essay here…"
              />
              <div className="mock-writing-field-meta">
                <span className={words >= minWords ? 'is-ok' : ''}>
                  {words} 词（要求 ≥ {minWords}）
                </span>
                {locked ? <span>已交卷</span> : null}
              </div>
            </label>
          </section>

          {!locked ? (
            <div className="mock-writing-actions">
              <button
                type="button"
                className="btn teacher-publish"
                disabled={saving}
                onClick={() => void submitExam(false)}
              >
                {saving ? '交卷中…' : '交卷'}
              </button>
            </div>
          ) : null}
        </main>
      )}
    </div>
  )
}