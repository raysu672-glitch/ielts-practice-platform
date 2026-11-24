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

function markFromNode(node: Node | null): HTMLElement | null {
  if (!node) return null
  const el = node instanceof Element ? node : node.parentElement
  return el?.closest?.(`mark.${HL_CLASS}[${HL_ATTR}]`) as HTMLElement | null
}

export function getSelectionInfo(): {
  text: string
  range: Range
  scope: HTMLElement
  rect: DOMRect
  canHighlight: boolean
  canRemove: boolean
} | null {
  const sel = window.getSelection()
  if (!sel || sel.rangeCount === 0) return null
  const range = sel.getRangeAt(0).cloneRange()
  const startScope = findHighlightScope(range.startContainer)
  const endScope = findHighlightScope(range.endContainer)
  if (!startScope || startScope !== endScope) return null
  if (isForbiddenNode(range.startContainer) || isForbiddenNode(range.endContainer)) return null
  const common = range.commonAncestorContainer
  if (isForbiddenNode(common)) return null

  // 光标点在已有高亮内：只开「取消」
  if (sel.isCollapsed) {
    const mark = markFromNode(range.startContainer)
    if (!mark || !startScope.contains(mark)) return null
    const rect = mark.getBoundingClientRect()
    if (!rect || (rect.width === 0 && rect.height === 0)) return null
    const markRange = document.createRange()
    markRange.selectNodeContents(mark)
    return {
      text: (mark.textContent || '').trim(),
      range: markRange,
      scope: startScope,
      rect,
      canHighlight: false,
      canRemove: true,
    }
  }

  const text = sel.toString().replace(/\s+/g, ' ').trim()
  if (!text || text.length > MAX_CHARS) return null
  const rect = range.getBoundingClientRect()
  if (!rect || (rect.width === 0 && rect.height === 0)) return null
  const canRemove = marksIntersectingRange(range, startScope).length > 0
  return {
    text,
    range,
    scope: startScope,
    rect,
    canHighlight: true,
    canRemove,
  }
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
      // 用 intersectsNode：compareBoundaryPoints 的 START/END 方向易写反，
      // 选区与 mark 完全重合时旧逻辑会误判为不相交，导致「取消」无效。
      if (typeof range.intersectsNode === 'function') {
        return range.intersectsNode(m)
      }
      const r = document.createRange()
      r.selectNodeContents(m)
      return !(
        range.compareBoundaryPoints(Range.START_TO_END, r) <= 0 ||
        range.compareBoundaryPoints(Range.END_TO_START, r) >= 0
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
