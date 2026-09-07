import { useEffect, useRef } from 'react'
import { NORMALIZE_VERSION, normalizePaperHtml } from '../lib/normalizePaper'
import type { GradeItem } from '../lib/grade'

type Props = {
  html: string
  answers: Record<string, string>
  onAnswer: (num: string, value: string) => void
  readOnly?: boolean
  reviewItems?: GradeItem[]
}

/** 题干只挂载一次，避免 React 重渲染打断输入。 */
export default function PaperHost({
  html,
  answers,
  onAnswer,
  readOnly = false,
  reviewItems,
}: Props) {
  const ref = useRef<HTMLDivElement>(null)
  const onAnswerRef = useRef(onAnswer)
  onAnswerRef.current = onAnswer

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.innerHTML = normalizePaperHtml(html)

    const applyMultiSelect = (label: HTMLLabelElement) => {
      const start = label.dataset.qStart
      const end = label.dataset.qEnd
      const count = Number(label.dataset.count || 0)
      if (!start || !end || count < 2) return false
      const list = label.closest('.opt-list')
      if (!list) return false
      const checked = [...list.querySelectorAll<HTMLInputElement>('input[type=checkbox]:checked')].map(
        (i) => i.value,
      )
      if (checked.length > count) {
        const boxes = [...list.querySelectorAll<HTMLInputElement>('input[type=checkbox]:checked')]
        boxes.slice(0, checked.length - count).forEach((b) => {
          b.checked = false
        })
      }
      const final = [...list.querySelectorAll<HTMLInputElement>('input[type=checkbox]:checked')].map(
        (i) => i.value,
      )
      const s = Number(start)
      const e = Number(end)
      for (let n = s; n <= e; n++) onAnswerRef.current(String(n), '')
      final.forEach((letter, idx) => {
        onAnswerRef.current(String(s + idx), letter)
      })
      return true
    }

    const handler = (e: Event) => {
      if (readOnly) {
        e.preventDefault()
        return
      }
      const t = e.target as HTMLInputElement
      if (!t || t.tagName !== 'INPUT') return
      const label = t.closest('label.opt-label') as HTMLLabelElement | null
      if (t.type === 'checkbox' && label && applyMultiSelect(label)) return
      const num = t.getAttribute('data-question-num')
      if (!num) return
      if (t.type === 'checkbox') {
        onAnswerRef.current(num, t.checked ? t.value : '')
      } else {
        onAnswerRef.current(num, t.value)
      }
    }
    el.addEventListener('input', handler)
    el.addEventListener('change', handler)
    return () => {
      el.removeEventListener('input', handler)
      el.removeEventListener('change', handler)
      el.innerHTML = ''
    }
  }, [html, NORMALIZE_VERSION, readOnly])

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.querySelectorAll<HTMLInputElement>('input[data-question-num]').forEach((inp) => {
      const num = inp.getAttribute('data-question-num') || ''
      const val = answers[num] || ''
      if (inp.type === 'radio') {
        inp.checked = inp.value === val
      } else if (inp.type === 'checkbox') {
        const label = inp.closest('label.opt-label') as HTMLLabelElement | null
        const start = label?.dataset.qStart
        const end = label?.dataset.qEnd
        if (start && end) {
          const picked: string[] = []
          for (let n = Number(start); n <= Number(end); n++) {
            const v = answers[String(n)]
            if (v) picked.push(v)
          }
          inp.checked = picked.includes(inp.value)
        } else {
          inp.checked = val === inp.value
        }
      } else if (document.activeElement !== inp && inp.value !== val) {
        inp.value = val
      }
      if (readOnly) {
        inp.disabled = true
        inp.readOnly = true
      }
    })
  }, [answers, html, readOnly])

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.querySelectorAll('.asg-review-hint').forEach((n) => n.remove())
    el.querySelectorAll('.asg-review-mark').forEach((n) => {
      n.classList.remove('asg-review-mark', 'is-correct', 'is-wrong', 'is-blank')
    })
    if (!reviewItems?.length) return

    const byNum = new Map(reviewItems.map((it) => [String(it.number), it]))
    const painted = new Set<string>()

    el.querySelectorAll<HTMLInputElement>('input[data-question-num]').forEach((inp) => {
      const num = inp.getAttribute('data-question-num') || ''
      const item = byNum.get(num)
      if (!item || painted.has(num)) return
      painted.add(num)

      const host =
        (inp.closest('.qt-a, .gap, .blank, label.opt-label, .opt-list') as HTMLElement | null) ||
        inp.parentElement
      if (!host) return

      host.classList.add('asg-review-mark', `is-${item.status}`)

      // 仅错题/未答显示「你的答案」；对题只保留题面着色
      if (item.status === 'correct') return

      const hint = document.createElement('span')
      hint.className = `asg-review-hint is-${item.status}`
      const user = item.user?.trim() || '（空）'
      hint.innerHTML = `<em>你的</em> ${escapeHtml(user)} <em>· 正确</em> ${escapeHtml(item.correct || '—')}`
      host.insertAdjacentElement('afterend', hint)
    })
  }, [reviewItems, html, answers])

  return <div className="paper-html paper-host" ref={ref} />
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
