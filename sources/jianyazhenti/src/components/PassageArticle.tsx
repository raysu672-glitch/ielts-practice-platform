import { useEffect, useRef } from 'react'
import type { PartData } from '../types'

type Passage = NonNullable<NonNullable<PartData['passage']>['passages']>[number]

/**
 * 文章只挂载一次 DOM，避免答题时 React 重渲染清掉划词高亮。
 */
export default function PassageArticle({
  passage,
  resetKey,
}: {
  passage: Passage
  resetKey: string
}) {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const blocks = (passage.paragraphs || []).filter(
      (p) => (p.html || p.text || '').trim() || (p.name || '').trim(),
    )
    const parts: string[] = []
    if (passage.title) {
      parts.push(`<h1 class="passage-title">${escapeHtml(passage.title)}</h1>`)
    }
    if (passage.subtitle) {
      parts.push(`<p class="passage-sub">${escapeHtml(passage.subtitle)}</p>`)
    }
    blocks.forEach((p) => {
      const label = (p.name || '').trim()
      const body = (p.html || p.text || '').trim()
      if (!body && !label) return
      const labelHtml = label ? `<div class="passage-label">${escapeHtml(label)}</div>` : ''
      const bodyHtml = p.html
        ? `<div class="passage-html">${p.html}</div>`
        : `<p class="passage-text">${escapeHtml(p.text || '')}</p>`
      parts.push(
        `<div class="passage-block${label ? ' has-label' : ''}">${labelHtml}${bodyHtml}</div>`,
      )
    })
    el.innerHTML = parts.join('')
    return () => {
      el.innerHTML = ''
    }
  }, [passage, resetKey])

  return <article className="passage-article" ref={ref} data-highlight-scope="passage" />
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
