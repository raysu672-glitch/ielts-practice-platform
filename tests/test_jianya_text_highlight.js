/**
 * Node + jsdom smoke for jianyazhenti text highlight helpers.
 * Run via: node --experimental-vm-modules or plain node with dynamic import after build.
 * Here we inline the core wrap logic to avoid TS compile dependency.
 */
const assert = require('assert')
let JSDOM
try {
  JSDOM = require('jsdom').JSDOM
} catch {
  // jsdom 仅在 sources/jianyazhenti 依赖里；根目录跑全量前端测时跳过
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

function applyHighlight(range, level = 1) {
  let scope = range.commonAncestorContainer
  while (scope && !(scope instanceof (range.commonAncestorContainer.ownerDocument.defaultView.HTMLElement))) {
    scope = scope.parentNode
  }
  while (scope && !scope.hasAttribute?.(SCOPE_ATTR)) scope = scope.parentNode
  if (!scope) return false

  const marks = [...scope.querySelectorAll(`mark.${HL_CLASS}[${HL_ATTR}]`)]
  marks.forEach((m) => {
    try {
      const r = scope.ownerDocument.createRange()
      r.selectNodeContents(m)
      const overlap = !(
        range.compareBoundaryPoints(Range.END_TO_START, r) <= 0 ||
        range.compareBoundaryPoints(Range.START_TO_END, r) >= 0
      )
      if (overlap) unwrapMark(m)
    } catch {
      /* ignore */
    }
  })

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

const dom = new JSDOM(`<!doctype html><div ${SCOPE_ATTR}="p"><p id="t">The arid valleys of Peru</p></div>`)
const { document, Range } = dom.window
global.Range = Range
const p = document.getElementById('t')
const range = document.createRange()
range.setStart(p.firstChild, 4)
range.setEnd(p.firstChild, 8) // "arid"
assert.equal(applyHighlight(range, 1), true)
const mark = p.querySelector('mark.jianya-hl-1')
assert.ok(mark)
assert.equal(mark.textContent, 'arid')
assert.equal(mark.getAttribute(HL_ATTR), '1')
console.log('test_jianya_text_highlight.js ok')
