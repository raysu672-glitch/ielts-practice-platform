import { useEffect, useRef, useState } from 'react'
import {
  TOOLBAR_ATTR,
  applyHighlight,
  getSelectionInfo,
  removeHighlightsInRange,
  type HighlightLevel,
} from '../lib/textHighlight'

type ToolbarState = {
  left: number
  top: number
  canHighlight: boolean
  canRemove: boolean
}

/**
 * 全局划词高亮层：在带 data-highlight-scope 的区域内选中文字后弹出工具条。
 * 挂一次即可覆盖阅读文章、阅读题干、听力题干。
 */
export default function TextHighlightLayer({ enabled = true }: { enabled?: boolean }) {
  const [bar, setBar] = useState<ToolbarState | null>(null)
  const rangeRef = useRef<Range | null>(null)
  const scopeRef = useRef<HTMLElement | null>(null)
  const rootRef = useRef<HTMLDivElement>(null)

  const hide = () => {
    setBar(null)
    rangeRef.current = null
    scopeRef.current = null
  }

  useEffect(() => {
    if (!enabled) {
      hide()
      return
    }

    const onPointerUp = (e: Event) => {
      const t = e.target as Node | null
      if (t instanceof Element && t.closest(`[${TOOLBAR_ATTR}]`)) return
      // 等浏览器写完 selection
      // 略延迟，避开 Edge/Chrome 划词迷你菜单常贴在选区上方正中
      window.setTimeout(() => {
        const info = getSelectionInfo()
        if (!info) {
          hide()
          return
        }
        rangeRef.current = info.range
        scopeRef.current = info.scope
        const pad = 14
        const tw = info.canHighlight ? 168 : 72
        const th = 40
        // 默认放选区下方偏左，躲开浏览器自带划词条
        let left = info.rect.left
        let top = info.rect.bottom + pad
        if (top + th > window.innerHeight - 8) {
          top = Math.max(8, info.rect.top - th - pad)
        }
        // 仍与选区中心重叠时，再往右让开一截
        const selCenterX = info.rect.left + info.rect.width / 2
        if (Math.abs(left + tw / 2 - selCenterX) < 36) {
          left = selCenterX + 28
        }
        left = Math.max(8, Math.min(left, window.innerWidth - tw - 8))
        setBar({
          left,
          top,
          canHighlight: info.canHighlight,
          canRemove: info.canRemove,
        })
      }, 30)
    }

    const onScroll = () => hide()
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') hide()
    }

    document.addEventListener('mouseup', onPointerUp)
    document.addEventListener('touchend', onPointerUp, { passive: true })
    window.addEventListener('scroll', onScroll, true)
    window.addEventListener('resize', onScroll)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mouseup', onPointerUp)
      document.removeEventListener('touchend', onPointerUp)
      window.removeEventListener('scroll', onScroll, true)
      window.removeEventListener('resize', onScroll)
      document.removeEventListener('keydown', onKey)
    }
  }, [enabled])

  const runHighlight = (level: HighlightLevel = 1) => {
    const range = rangeRef.current
    if (!range) return
    applyHighlight(range, level)
    hide()
  }

  const runRemove = () => {
    const range = rangeRef.current
    const scope = scopeRef.current
    if (!range || !scope) return
    removeHighlightsInRange(range, scope)
    hide()
  }

  if (!enabled || !bar) return null

  return (
    <div
      ref={rootRef}
      className="jianya-hl-toolbar"
      style={{ left: bar.left, top: bar.top }}
      data-jianya-hl-toolbar="true"
      role="toolbar"
      aria-label="划词高亮"
      onMouseDown={(e) => e.preventDefault()}
    >
      {bar.canHighlight && (
        <>
          <button type="button" className="jianya-hl-btn" onClick={() => runHighlight(1)} title="高亮">
            <span className="jianya-hl-swatch jianya-hl-swatch-1" />
            高亮
          </button>
          <button
            type="button"
            className="jianya-hl-btn"
            onClick={() => runHighlight(2)}
            title="换色高亮"
          >
            <span className="jianya-hl-swatch jianya-hl-swatch-2" />
            换色
          </button>
        </>
      )}
      {bar.canRemove && (
        <button type="button" className="jianya-hl-btn jianya-hl-btn-muted" onClick={runRemove} title="取消高亮">
          取消
        </button>
      )}
    </div>
  )
}
