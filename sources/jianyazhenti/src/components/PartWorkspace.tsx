import PaperHost from './PaperHost'
import PassageArticle from './PassageArticle'
import TextHighlightLayer from './TextHighlightLayer'
import type { GradeItem } from '../lib/grade'
import type { PartData } from '../types'

function FallbackQuestions({
  part,
  answers,
  onAnswer,
  readOnly,
  reviewItems,
}: {
  part: PartData
  answers: Record<string, string>
  onAnswer: (num: string, value: string) => void
  readOnly?: boolean
  reviewItems?: GradeItem[]
}) {
  const byNum = new Map(reviewItems?.map((it) => [it.number, it]))
  return (
    <div className="fallback-q" data-highlight-scope="fallback">
      {part.questions.map((q) => {
        const item = byNum.get(q.number)
        return (
          <div className="fallback-item" key={q.number}>
            <div className="fallback-stem">
              <strong>{q.number}.</strong> {q.stem || '填空'}
            </div>
            {q.type === 'single_choice' ? (
              <div className="opt-row">
                {q.options.map((op) => (
                  <label className="opt-label" key={op.value}>
                    <input
                      type="radio"
                      name={`q-${q.number}`}
                      value={op.value}
                      checked={answers[String(q.number)] === op.value}
                      disabled={readOnly}
                      onChange={() => onAnswer(String(q.number), op.value)}
                    />{' '}
                    {op.label}
                  </label>
                ))}
              </div>
            ) : (
              <input
                className="fallback-input"
                value={answers[String(q.number)] || ''}
                disabled={readOnly}
                readOnly={readOnly}
                onChange={(e) => onAnswer(String(q.number), e.target.value)}
                placeholder="answers here"
              />
            )}
            {item && item.status !== 'correct' && (
              <div className={`asg-review-hint is-${item.status}`}>
                <em>你的</em> {item.user?.trim() || '（空）'}
                {' · 正确'} {item.correct || '—'}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default function PartWorkspace({
  part,
  bookId,
  answers,
  onAnswer,
  locked,
  reviewItems,
  sheetOpen,
  attemptKey,
}: {
  part: PartData
  bookId: number
  answers: Record<string, string>
  onAnswer: (num: string, value: string) => void
  locked: boolean
  reviewItems?: GradeItem[]
  sheetOpen: boolean
  attemptKey: string
}) {
  const isReading = part.subject === 'reading'
  const passage = part.passage?.passages?.[0]
  const filled = Object.values(answers).filter((v) => String(v).trim()).length

  const jumpTo = (num: number) => {
    const root = document.querySelector('.paper-host')
    if (!root) return
    const el =
      (root.querySelector(`.qt-a[data-question-num="${num}"]`) as HTMLElement | null) ||
      (root.querySelector(`input[data-question-num="${num}"]:not([type=radio])`) as HTMLElement | null) ||
      (root.querySelector(`input[data-question-num="${num}"]`) as HTMLElement | null)
    el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    if (el instanceof HTMLInputElement && el.type !== 'radio' && !locked) el.focus()
  }

  return (
    <div
      className={`exam-stage ${sheetOpen ? 'with-sheet' : 'no-sheet'} ${
        isReading ? 'is-reading' : 'is-listening'
      }`}
    >
      <TextHighlightLayer />
      {isReading && (
        <section className="exam-pane passage-pane">
          <div className="pane-scroll">
            {passage ? (
              <PassageArticle
                passage={passage}
                resetKey={`${attemptKey}-${bookId}-${part.sId}`}
              />
            ) : (
              <p className="empty">暂无文章正文</p>
            )}
          </div>
        </section>
      )}

      <section className="exam-pane question-pane">
        <div className="pane-scroll">
          {part.paperHtml ? (
            <PaperHost
              key={`${attemptKey}-${bookId}-${part.sId}-${locked ? 'r' : 'e'}`}
              html={part.paperHtml}
              answers={answers}
              onAnswer={onAnswer}
              readOnly={locked}
              reviewItems={reviewItems}
            />
          ) : (
            <FallbackQuestions
              part={part}
              answers={answers}
              onAnswer={onAnswer}
              readOnly={locked}
              reviewItems={reviewItems}
            />
          )}
        </div>
      </section>

      {sheetOpen && (
        <aside className="answer-sheet">
          <div className="answer-sheet-title">Answer Sheet</div>
          <div className="sheet-grid">
            {part.questions.map((q) => {
              const item = reviewItems?.find((it) => it.number === q.number)
              const cls = [
                'sheet-item',
                answers[String(q.number)]?.trim() ? 'filled' : '',
                item ? `review-${item.status}` : '',
              ]
                .filter(Boolean)
                .join(' ')
              return (
                <button
                  key={q.number}
                  type="button"
                  className={cls}
                  onClick={() => jumpTo(q.number)}
                >
                  {q.number}
                </button>
              )
            })}
          </div>
          <div className="sheet-meta">
            {filled}/{part.questions.length}
            {locked ? ' · 已锁定' : ''}
          </div>
        </aside>
      )}
    </div>
  )
}
