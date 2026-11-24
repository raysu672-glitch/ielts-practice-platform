/** 划词高亮：选中文字后包裹 <mark class="jianya-hl">，支持两级颜色与取消。 */

export const HL_ATTR = 'data-jianya-hl'
export const HL_CLASS = 'jianya-hl'
export const SCOPE_ATTR = 'data-highlight-scope'
export const TOOLBAR_ATTR = 'data-jianya-hl-toolbar'

export type HighlightLevel = 1 | 2

const MAX_CHARS = 500

function isForbiddenNode(node: Node | null): boolean {
  let cur: Node | null = node
  while (cur) {
    if (cur instanceof Element) {
      if (cur.closest(`input, textarea, select, button, a, [${TOOLBAR_ATTR}]`)) return true
      if (cur.closest('[contenteditable="true"]')) return true
    }
    cur = cur.parentNode
  }
  return false
}

export function findHighlightScope(node: Node | null): HTMLElement | null {
  let cur: Node | null = node
  while (cur) {
    if (cur instanceof HTMLElement && cur.hasAttribute(SCOPE_ATTR)) return cur
    cur = cur.parentNode
  }
  return null
}

export function getSelectionInfo(): {
  text: string
  range: Range
  scope: HTMLElement
  rect: DOMRect
} | null {
  const sel = window.getSelection()
  if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null
  const text = sel.toString().replace(/\s+/g, ' ').trim()
  if (!text || text.length > MAX_CHARS) return null
  const range = sel.getRangeAt(0).cloneRange()
  const startScope = findHighlightScope(range.startContainer)
  const endScope = findHighlightScope(range.endContainer)
  if (!startScope || startScope !== endScope) return null
  if (isForbiddenNode(range.startContainer) || isForbiddenNode(range.endContainer)) return null
  // 不允许跨输入框等
  const common = range.commonAncestorContainer
  if (isForbiddenNode(common)) return null
  const rect = range.getBoundingClientRect()
  if (!rect || (rect.width === 0 && rect.height === 0)) return null
  return { text, range, scope: startScope, rect }
}

function unwrapMark(mark: HTMLElement) {
  const parent = mark.parentNode
  if (!parent) return
  while (mark.firstChild) parent.insertBefore(mark.firstChild, mark)
  parent.removeChild(mark)
  parent.normalize()
}

export function marksIntersectingRange(range: Range, scope: HTMLElement): HTMLElement[] {
  const marks = [...scope.querySelectorAll<HTMLElement>(`mark.${HL_CLASS}[${HL_ATTR}]`)]
  return marks.filter((m) => {
    try {
      const r = document.createRange()
      r.selectNodeContents(m)
      // overlap if not fully before/after
      return !(
        range.compareBoundaryPoints(Range.END_TO_START, r) <= 0 ||
        range.compareBoundaryPoints(Range.START_TO_END, r) >= 0
      )
    } catch {
      return false
    }
  })
}

export function applyHighlight(range: Range, level: HighlightLevel = 1): boolean {
  const scope = findHighlightScope(range.commonAncestorContainer)
  if (!scope) return false
  // 先拆掉选区内旧高亮，再统一包一层
  marksIntersectingRange(range, scope).forEach(unwrapMark)

  const mark = document.createElement('mark')
  mark.className = `${HL_CLASS} ${HL_CLASS}-${level}`
  mark.setAttribute(HL_ATTR, String(level))

  try {
    range.surroundContents(mark)
  } catch {
    const frag = range.extractContents()
    mark.appendChild(frag)
    range.insertNode(mark)
  }
  if (!(mark.textContent || '').trim()) {
    unwrapMark(mark)
    return false
  }
  window.getSelection()?.removeAllRanges()
  return true
}

export function removeHighlightsInRange(range: Range, scope: HTMLElement): boolean {
  const marks = marksIntersectingRange(range, scope)
  if (!marks.length) return false
  marks.forEach(unwrapMark)
  window.getSelection()?.removeAllRanges()
  return true
}

export function clearHighlightsInScope(scope: HTMLElement) {
  scope.querySelectorAll<HTMLElement>(`mark.${HL_CLASS}[${HL_ATTR}]`).forEach(unwrapMark)
}
