/**
 * Node + jsdom smoke for jianyazhenti text highlight helpers.
 */
const assert = require('assert')
let JSDOM
try {
  JSDOM = require('jsdom').JSDOM
} catch {
  try {
    JSDOM = require('../sources/jianyazhenti/node_modules/jsdom').JSDOM
  } catch {
    console.log('test_jianya_text_highlight.js skip (no jsdom)')
    process.exit(0)
  }
}

const HL_ATTR = 'data-jianya-hl'
const HL_CLASS = 'jianya-hl'
const SCOPE_ATTR = 'data-highlight-scope'

function unwrapMark(mark) {
  const parent = mark.parentNode
  if (!parent) return
  while (mark.firstChild) parent.insertBefore(mark.firstChild, mark)
  parent.removeChild(mark)
  parent.normalize()
}

function marksIntersectingRange(range, scope) {
  const marks = [...scope.querySelectorAll(`mark.${HL_CLASS}[${HL_ATTR}]`)]
  return marks.filter((m) => {
    try {
      if (typeof range.intersectsNode === 'function') return range.intersectsNode(m)
      const r = scope.ownerDocument.createRange()
      r.selectNodeContents(m)
      return !(
        range.compareBoundaryPoints(scope.ownerDocument.defaultView.Range.START_TO_END, r) <= 0 ||
        range.compareBoundaryPoints(scope.ownerDocument.defaultView.Range.END_TO_START, r) >= 0
      )
    } catch {
      return false
    }
  })
}

function applyHighlight(range, level = 1) {
  let scope = range.commonAncestorContainer
  while (scope && !(scope.nodeType === 1 && scope.hasAttribute?.(SCOPE_ATTR))) {
    scope = scope.parentNode
  }
  if (!scope) return false

  marksIntersectingRange(range, scope).forEach(unwrapMark)

  const mark = scope.ownerDocument.createElement('mark')
  mark.className = `${HL_CLASS} ${HL_CLASS}-${level}`
  mark.setAttribute(HL_ATTR, String(level))
  try {
    range.surroundContents(mark)
  } catch {
    const frag = range.extractContents()
    mark.appendChild(frag)
    range.insertNode(mark)
  }
  return !!(mark.textContent || '').trim()
}

function removeHighlightsInRange(range, scope) {
  const marks = marksIntersectingRange(range, scope)
  if (!marks.length) return false
  marks.forEach(unwrapMark)
  return true
}

const dom = new JSDOM(`<!doctype html><div ${SCOPE_ATTR}="p"><p id="t">The arid valleys of Peru</p></div>`)
const { document, Range } = dom.window
global.Range = Range
const p = document.getElementById('t')
const scope = p.parentElement

const range = document.createRange()
range.setStart(p.firstChild, 4)
range.setEnd(p.firstChild, 8) // "arid"
assert.equal(applyHighlight(range, 1), true)
const mark = p.querySelector('mark.jianya-hl-1')
assert.ok(mark)
assert.equal(mark.textContent, 'arid')
assert.equal(mark.getAttribute(HL_ATTR), '1')

// 选中 mark 全文后应能取消（旧 compare 逻辑在完全重合时会误判）
const sel = document.createRange()
sel.selectNodeContents(mark)
assert.equal(marksIntersectingRange(sel, scope).length, 1)
assert.equal(removeHighlightsInRange(sel, scope), true)
assert.equal(p.querySelector('mark.jianya-hl'), null)
assert.equal(p.textContent, 'The arid valleys of Peru')

console.log('test_jianya_text_highlight.js ok')
