import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import PartWorkspace from '../components/PartWorkspace'
import type { GradeItem } from '../lib/grade'
import {
  formatClock,
  formatTypeStats,
  gradeMockPart,
  listeningStatusText,
  loadMockParts,
  mockDurations,
  mockSetFromScores,
  persistMockPart,
  persistMockSet,
  pickMockSet,
  paperShortLabel,
  type ListeningPhase,
  type LoadedMockPart,
  type MockPartScore,
} from '../lib/mockExam'
import type { Subject } from '../types'

type AnswersMap = Record<number, Record<string, string>>

export default function MockExam() {
  const { subject = '' } = useParams()
  const [search] = useSearchParams()
  const sub = subject as Subject
  const fast = search.get('fast') === '1'
  const durations = mockDurations(fast)
  const backTo = `/student/mock${search.toString() ? `?${search.toString()}` : ''}`

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [loaded, setLoaded] = useState<LoadedMockPart[]>([])
  const [reusedCount, setReusedCount] = useState(0)
  const [activePart, setActivePart] = useState(1)
  const [answers, setAnswers] = useState<AnswersMap>({})
  const [sheetOpen, setSheetOpen] = useState(true)
  const [started, setStarted] = useState(false)
  const [locked, setLocked] = useState(false)
  const [remaining, setRemaining] = useState(durations.readingLimit)
  const [phase, setPhase] = useState<ListeningPhase>({ kind: 'idle' })
  const [scores, setScores] = useState<MockPartScore[] | null>(null)
  const [submitHint, setSubmitHint] = useState('')
  const [reloadToken, setReloadToken] = useState(0)

  const startedAtRef = useRef(0)
  const submittingRef = useRef(false)
  const answersRef = useRef(answers)
  const loadedRef = useRef(loaded)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const tickRef = useRef<number | null>(null)
  const deadlineRef = useRef(0)
  const playIndexRef = useRef(0)
  const startedRef = useRef(false)
  const lockedRef = useRef(false)
  const ignoreAudioRef = useRef(false)
  const partSecondsRef = useRef<Record<number, number>>({})
  const partViewRef = useRef<{ sPart: number; at: number } | null>(null)

  answersRef.current = answers
  loadedRef.current = loaded
  startedRef.current = started
  lockedRef.current = locked

  const current = loaded.find((item) => item.part.sPart === activePart) || loaded[0]
  const isReading = sub === 'reading'
  const isListening = sub === 'listening'

  useEffect(() => {
    if (sub !== 'reading' && sub !== 'listening') {
      setError('该科目暂未开放模拟考')
      setLoading(false)
      return
    }
    let cancelled = false
    setLoading(true)
    setError('')
    ;(async () => {
      try {
        const picked = await pickMockSet(sub)
        const parts = await loadMockParts(picked.papers)
        if (cancelled) return
        setLoaded(parts)
        setReusedCount(picked.reusedCount)
        setActivePart(parts[0]?.part.sPart || 1)
        setAnswers({})
        setLoading(false)
      } catch (e) {
        if (!cancelled) {
          const raw = e instanceof Error ? e.message : '组卷失败'
          setError(
            /failed to fetch|networkerror|load failed/i.test(raw)
              ? '题库加载失败，请点击重新组卷'
              : raw,
          )
          setLoading(false)
        }
      }
    })()
    return () => {
      cancelled = true
    }
  }, [sub, reloadToken])

  const clearTick = () => {
    if (tickRef.current) {
      window.clearInterval(tickRef.current)
      tickRef.current = null
    }
  }

  const stopAudio = () => {
    const audio = audioRef.current
    if (!audio) return
    ignoreAudioRef.current = true
    audio.pause()
    audio.removeAttribute('src')
    audio.load()
  }

  const flushPartTime = (now = Date.now()) => {
    const cur = partViewRef.current
    if (!cur) return
    const add = Math.max(0, (now - cur.at) / 1000)
    partSecondsRef.current[cur.sPart] = (partSecondsRef.current[cur.sPart] || 0) + add
    partViewRef.current = null
  }

  const startPartClock = (sPart: number) => {
    flushPartTime()
    partViewRef.current = { sPart, at: Date.now() }
  }

  const submitExam = async (auto = false) => {
    if (submittingRef.current || lockedRef.current) return
    if (!auto && startedRef.current && !window.confirm('确认交卷？未填的题将记为空。')) return
    submittingRef.current = true
    clearTick()
    stopAudio()
    flushPartTime()
    partViewRef.current = null
    setSubmitHint(auto ? '时间到，正在交卷…' : '正在交卷…')
    try {
      const parts = loadedRef.current
      const map = answersRef.current
      const startedAt = startedAtRef.current || Date.now()
      const result: MockPartScore[] = []
      for (const item of parts) {
        const scored = await gradeMockPart(
          item,
          map[item.part.sPart] || {},
          Math.round(partSecondsRef.current[item.part.sPart] || 0),
        )
        result.push(scored)
      }
      for (let i = 0; i < parts.length; i += 1) {
        await persistMockPart(result[i], startedAt, parts[i])
      }
      await persistMockSet(mockSetFromScores(sub, result, startedAt))
      setScores(result)
      setLocked(true)
      setPhase({ kind: 'done' })
      setSubmitHint('')
    } catch (e) {
      setSubmitHint('')
      submittingRef.current = false
      alert(e instanceof Error ? e.message : '交卷失败')
    }
  }

  const submitRef = useRef(submitExam)
  submitRef.current = submitExam

  const playPartAudio = (index: number) => {
    const item = loadedRef.current[index]
    if (!item) {
      submitRef.current(true)
      return
    }
    playIndexRef.current = index
    setPhase({ kind: 'play', part: item.part.sPart })
    const audio = audioRef.current
    const url = item.audioUrl
    if (!audio || !url) {
      window.setTimeout(() => afterAudioEnded(index), 400)
      return
    }
    ignoreAudioRef.current = false
    audio.src = url
    const play = audio.play()
    if (play && typeof play.catch === 'function') {
      play.catch(() => {
        window.setTimeout(() => afterAudioEnded(index), 400)
      })
    }
  }

  const afterAudioEnded = (index: number) => {
    if (lockedRef.current || !startedRef.current) return
    const next = index + 1
    if (next < loadedRef.current.length) {
      startCountdown(durations.gap, () => playPartAudio(next), (left) =>
        setPhase({ kind: 'gap', nextPart: loadedRef.current[next].part.sPart, remaining: left }),
      )
      return
    }
    startCountdown(durations.end, () => submitRef.current(true), (left) =>
      setPhase({ kind: 'ending', remaining: left }),
    )
  }

  const startCountdown = (
    seconds: number,
    onDone: () => void,
    onTick: (left: number) => void,
  ) => {
    clearTick()
    deadlineRef.current = Date.now() + seconds * 1000
    onTick(seconds)
    tickRef.current = window.setInterval(() => {
      const left = Math.max(0, Math.ceil((deadlineRef.current - Date.now()) / 1000))
      onTick(left)
      if (left <= 0) {
        clearTick()
        onDone()
      }
    }, 200)
  }

  const startExam = () => {
    if (!loaded.length || started) return
    startedAtRef.current = Date.now()
    partSecondsRef.current = {}
    startPartClock(activePart)
    setStarted(true)
    if (isReading) {
      startCountdown(durations.readingLimit, () => submitRef.current(true), setRemaining)
      return
    }
    startCountdown(durations.intro, () => playPartAudio(0), (left) =>
      setPhase({ kind: 'intro', remaining: left }),
    )
  }

  useEffect(() => {
    if (!started || locked) return
    startPartClock(activePart)
    return () => {
      flushPartTime()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [started, locked, activePart])

  useEffect(() => {
    const onVis = () => {
      if (document.hidden) flushPartTime()
      else if (startedRef.current && !lockedRef.current) startPartClock(activePart)
    }
    document.addEventListener('visibilitychange', onVis)
    return () => document.removeEventListener('visibilitychange', onVis)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activePart])

  useEffect(() => {
    return () => {
      clearTick()
      stopAudio()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const onLeave = (e: BeforeUnloadEvent) => {
      if (startedRef.current && !lockedRef.current) {
        e.preventDefault()
        e.returnValue = ''
      }
    }
    window.addEventListener('beforeunload', onLeave)
    return () => window.removeEventListener('beforeunload', onLeave)
  }, [])

  const onAnswer = (num: string, value: string) => {
    if (locked) return
    const sPart = current?.part.sPart
    if (!sPart) return
    setAnswers((prev) => {
      const prevPart = prev[sPart] || {}
      if (prevPart[num] === value) return prev
      return { ...prev, [sPart]: { ...prevPart, [num]: value } }
    })
  }

  const reviewItems: GradeItem[] | undefined = useMemo(() => {
    if (!locked || !scores || !current) return undefined
    return scores.find((s) => s.paper.sId === current.paper.sId)?.items
  }, [locked, scores, current])

  const scoreLine = useMemo(() => {
    if (!scores) return ''
    const totalCorrect = scores.reduce((n, s) => n + s.graded.correct, 0)
    const totalQ = scores.reduce((n, s) => n + s.graded.total, 0)
    const pct = totalQ ? Math.round((totalCorrect / totalQ) * 100) : 0
    return `${totalCorrect}/${totalQ}（${pct}%）`
  }, [scores])

  const overallTypes = useMemo(() => {
    if (!scores?.length) return {}
    return mockSetFromScores(sub, scores, startedAtRef.current || Date.now()).typeStats
  }, [scores, sub])

  const onAudioEnded = () => {
    if (ignoreAudioRef.current || lockedRef.current) return
    afterAudioEnded(playIndexRef.current)
  }

  if (sub !== 'reading' && sub !== 'listening') {
    return (
      <div className="exam-status">
        该科目暂未开放。
        <div>
          <Link className="btn-link" to={backTo}>
            返回模拟考
          </Link>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="exam-status">
        {error}
        <div className="mock-error-actions">
          <button type="button" className="btn" onClick={() => setReloadToken((n) => n + 1)}>
            重新组卷
          </button>
          <Link className="btn-link" to={backTo}>
            返回模拟考
          </Link>
        </div>
      </div>
    )
  }

  if (loading || !current) {
    return <div className="exam-status">正在从 C7–C21 抽取未做过的 Part…</div>
  }

  const playingPart =
    phase.kind === 'play' ? phase.part : phase.kind === 'gap' ? phase.nextPart : 0

  return (
    <div className={`exam-shell ${isReading ? 'mode-reading' : 'mode-listening'}`}>
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
          <div className="exam-badge">{isReading ? 'READING MOCK' : 'LISTENING MOCK'}</div>
          <div className="exam-chrome-meta">
            <strong>{paperShortLabel(current.paper)}</strong>
            {locked && scoreLine ? <span className="exam-score-chip">{scoreLine}</span> : null}
          </div>
        </div>
        <div className="exam-chrome-right">
          {isReading && started && !locked ? (
            <div className={`exam-timer ${remaining <= 300 ? 'is-warn' : ''}`}>
              剩余 {formatClock(remaining)}
            </div>
          ) : null}
          {isListening && started && !locked ? (
            <div className="exam-timer">{listeningStatusText(phase)}</div>
          ) : null}
          <button type="button" className="exam-tool" onClick={() => setSheetOpen((v) => !v)}>
            {sheetOpen ? '收起答题卡' : '答题卡'}
          </button>
          {locked ? (
            <Link className="exam-tool" to={`/student/mock/history${search.toString() ? `?${search.toString()}` : ''}`}>
              历史记录
            </Link>
          ) : started ? (
            <button type="button" className="exam-tool primary" onClick={() => submitExam(false)}>
              交卷
            </button>
          ) : null}
        </div>
      </header>

      <div className="mock-part-tabs" role="tablist">
        {loaded.map((item) => {
          const sPart = item.part.sPart
          const filled = Object.values(answers[sPart] || {}).filter((v) => String(v).trim()).length
          const scored = scores?.find((s) => s.paper.sId === item.paper.sId)
          return (
            <button
              key={item.paper.sId}
              type="button"
              className={`mock-part-tab ${activePart === sPart ? 'active' : ''} ${
                playingPart === sPart ? 'is-playing' : ''
              }`}
              onClick={() => setActivePart(sPart)}
            >
              <span>Part {sPart}</span>
              <em>{paperShortLabel(item.paper)}</em>
              <small>
                {scored
                  ? `${scored.graded.correct}/${scored.graded.total} · ${formatClock(scored.durationSeconds)}`
                  : `${filled}/${item.part.questions.length}`}
              </small>
            </button>
          )
        })}
      </div>

      {locked && scores ? (
        <div className="mock-result-bar">
          <div>
            <strong>总分 {scoreLine}</strong>
            <span>{formatTypeStats(overallTypes)}</span>
          </div>
          <ul>
            {scores.map((s) => (
              <li key={s.paper.sId}>
                Part {s.paper.sPart} {paperShortLabel(s.paper)} · {s.graded.correct}/{s.graded.total}（{s.pct}%） · 用时{' '}
                {formatClock(s.durationSeconds)}
                <em>{formatTypeStats(s.typeStats)}</em>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {submitHint ? <div className="mock-submit-hint">{submitHint}</div> : null}

      {!started && !locked ? (
        <div className="mock-start-overlay">
          <div className="mock-start-card">
            <h2>{isReading ? '阅读模拟考' : '听力模拟考'}</h2>
            <p>
              已从 C7–C21 抽取{isReading ? ' 3 ' : ' 4 '}个还没做过的 Part
              {reusedCount ? `（其中 ${reusedCount} 个该 Part 都做过了，已重复抽取）` : ''}。
            </p>
            <ul>
              {loaded.map((item) => (
                <li key={item.paper.sId}>
                  Part {item.part.sPart} · {item.part.sName || paperShortLabel(item.paper)}
                  {item.paper.reused ? '（重复）' : ''}
                </li>
              ))}
            </ul>
            {isReading ? (
              <p>点击开始后限时 60 分钟，到时自动交卷。考试中可自由切换 Part。</p>
            ) : (
              <p>
                点击开始后先空 15 秒，再播放 Part 1；每段音频结束后空 30 秒播放下一段；Part 4
                结束后空 120 秒自动交卷。播放期间可自由切换答题界面，音频不会中断。
              </p>
            )}
            <button type="button" className="btn" onClick={startExam}>
              开始考试
            </button>
          </div>
        </div>
      ) : (
        <PartWorkspace
          part={current.part}
          bookId={current.paper.bookId}
          answers={answers[current.part.sPart] || {}}
          onAnswer={onAnswer}
          locked={locked}
          reviewItems={reviewItems}
          sheetOpen={sheetOpen}
          attemptKey={`mock-${current.paper.sId}`}
        />
      )}

      {isListening ? (
        <footer className="audio-dock mock-audio-dock">
          <div className="audio-dock-label">Audio</div>
          <div className="mock-audio-status">{listeningStatusText(phase)}</div>
          <audio
            ref={audioRef}
            preload="auto"
            onEnded={onAudioEnded}
            onError={() => {
              if (ignoreAudioRef.current || lockedRef.current) return
              afterAudioEnded(playIndexRef.current)
            }}
          />
        </footer>
      ) : null}
    </div>
  )
}
