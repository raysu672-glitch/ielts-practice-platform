/** 规范化原站题干 HTML，兼容听力单选/多选与阅读判断题。 */
export const NORMALIZE_VERSION = 4

function stripLayoutStyles(root: Element) {
  root.querySelectorAll('[style]').forEach((node) => {
    const el = node as HTMLElement
    const pos = el.style.position
    if (pos === 'absolute' || pos === 'fixed') {
      el.style.removeProperty('position')
      el.style.removeProperty('top')
      el.style.removeProperty('left')
      el.style.removeProperty('right')
      el.style.removeProperty('bottom')
    }
    if (el.style.width === '100%') el.style.removeProperty('width')
  })

  root.querySelectorAll('#canvas_test').forEach((canvas) => {
    canvas.removeAttribute('style')
    canvas.removeAttribute('v-else')
    canvas.classList.add('paper-body')
    const parent = canvas.parentElement
    if (!parent) return
    while (canvas.firstChild) parent.insertBefore(canvas.firstChild, canvas)
    canvas.remove()
  })

  root.querySelectorAll('*').forEach((n) => {
    ;[...n.attributes].forEach((attr) => {
      const name = attr.name
      if (name.startsWith('v-') || name.startsWith(':') || name.startsWith('@')) {
        n.removeAttribute(name)
      }
    })
  })
}

function groupPaperSections(root: Element) {
  const doc = root.ownerDocument
  const blocks = [...root.children]
  root.innerHTML = ''

  let section: HTMLElement | null = null

  const flushSection = () => {
    if (section) {
      root.appendChild(section)
      section = null
    }
  }

  blocks.forEach((node) => {
    if (node.classList.contains('st-c2')) {
      flushSection()
      section = doc.createElement('div')
      section.className = 'paper-section'
      section.appendChild(node)
      return
    }

    if (
      section &&
      (node.classList.contains('st-c') || node.classList.contains('qt-a'))
    ) {
      section.appendChild(node)
      return
    }

    flushSection()
    root.appendChild(node)
  })

  flushSection()
}

function optionRows(block: Element): Element[] {
  const direct = [...block.querySelectorAll(':scope > .qt-c')]
  if (direct.length) return direct
  // 阅读题常把 .qt-c 包在 display:flex 容器里
  return [...block.querySelectorAll('.qt-c')].filter(
    (row) => row.querySelector('input[type="radio"], input[type="checkbox"]'),
  )
}

function optionText(row: Element): string {
  let text = ''
  row.querySelectorAll(':scope > div').forEach((d) => {
    if (
      d.classList.contains('answer-radio') ||
      d.classList.contains('answer-checkbox') ||
      d.querySelector('input')
    ) {
      return
    }
    const t = d.textContent?.trim() || ''
    if (t) text = t
  })
  if (text) return text
  // 兜底：去掉控件与字母后的剩余文案
  const clone = row.cloneNode(true) as Element
  clone.querySelectorAll('input, .answer-radio, .answer-checkbox, strong, img').forEach((n) => n.remove())
  return clone.textContent?.replace(/\s+/g, ' ').trim() || ''
}

export function normalizePaperHtml(html: string): string {
  const doc = new DOMParser().parseFromString(`<div id="root">${html}</div>`, 'text/html')
  const root = doc.getElementById('root')
  if (!root) return html

  root.querySelectorAll('.qt-a').forEach((block) => {
    const stem = block.querySelector('.qt-b')
    const rows = optionRows(block)
    const embedded = rows.filter((row) =>
      row.querySelector('input[type="radio"], input[type="checkbox"]'),
    )

    // 听力 / 阅读：选项行内部自带 input + 字母/文案
    if (embedded.length) {
      const shortLabels = embedded.every((row) => {
        const t = optionText(row)
        return !t || /^(TRUE|FALSE|NOT GIVEN|T|F|NG)$/i.test(t)
      })
      const opts = doc.createElement('div')
      opts.className = shortLabels ? 'opt-row' : 'opt-list'

      embedded.forEach((row) => {
        const input = row.querySelector<HTMLInputElement>(
          'input[type="radio"], input[type="checkbox"]',
        )
        if (!input) return
        const letter =
          row.querySelector(':scope > strong')?.textContent?.trim() ||
          row.querySelector('strong')?.textContent?.trim() ||
          ''
        const text = optionText(row) || letter || input.value || ''
        const label = doc.createElement('label')
        label.className = shortLabels ? 'opt-label' : 'opt-label opt-block'
        const clone = input.cloneNode(true) as HTMLInputElement
        clone.removeAttribute('style')
        const countEl = row.querySelector('[data-count]')
        const count = countEl?.getAttribute('data-count')
        if (count) label.dataset.count = count
        if (stem) {
          const m = stem.textContent?.match(/(\d+)\s*[-–]\s*(\d+)/)
          if (m) {
            label.dataset.qStart = m[1]
            label.dataset.qEnd = m[2]
          }
        }
        label.appendChild(clone)
        if (shortLabels) {
          label.append(` ${text}`)
        } else {
          const cap = doc.createElement('span')
          cap.className = 'opt-cap'
          cap.textContent = letter || input.value || ''
          label.appendChild(cap)
          const body = doc.createElement('span')
          body.className = 'opt-text'
          body.textContent = text
          label.appendChild(body)
        }
        opts.appendChild(label)
      })

      const stemClone = stem ? (stem.cloneNode(true) as HTMLElement) : null
      block.innerHTML = ''
      if (stemClone) block.appendChild(stemClone)
      block.appendChild(opts)
      return
    }

    // 旧阅读结构：.qt-c 文案在前，.answer-radio 在后
    const radios = [...block.querySelectorAll<HTMLInputElement>('input[type="radio"]')]
    if (!radios.length) return
    const opts = doc.createElement('div')
    opts.className = 'opt-row'
    radios.forEach((radio) => {
      const wrap = radio.closest('.answer-radio') || radio.parentElement
      let labelText = radio.value || ''
      const prev = wrap?.previousElementSibling
      if (prev && prev.classList.contains('qt-c')) {
        labelText = prev.textContent?.trim() || labelText
        prev.remove()
      }
      const label = doc.createElement('label')
      label.className = 'opt-label'
      const clone = radio.cloneNode(true) as HTMLInputElement
      clone.removeAttribute('style')
      label.appendChild(clone)
      label.append(` ${labelText}`)
      opts.appendChild(label)
      wrap?.remove()
    })
    ;[...block.querySelectorAll('.answer-radio, .qt-c')].forEach((n) => n.remove())
    const stemNode = stem ? (stem.cloneNode(true) as HTMLElement) : null
    block.innerHTML = ''
    if (stemNode) block.appendChild(stemNode)
    block.appendChild(opts)
  })

  root.querySelectorAll<HTMLInputElement>('input.answer, input[data-question-num]').forEach((inp) => {
    inp.removeAttribute('readonly')
    inp.removeAttribute('disabled')
  })

  root.querySelectorAll('.answer-radio > div:empty, .answer-checkbox > img').forEach((n) => n.remove())

  stripLayoutStyles(root)
  groupPaperSections(root)

  return root.innerHTML
}
