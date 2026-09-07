import { useMemo, useState } from 'react'
import type { TeacherStudent } from '../lib/assignments'

export default function StudentPicker({
  students,
  selected,
  onChange,
  excludeIds,
  emptyHint = '暂无学生',
}: {
  students: TeacherStudent[]
  selected: Record<string, boolean>
  onChange: (next: Record<string, boolean>) => void
  excludeIds?: Set<string>
  emptyHint?: string
}) {
  const [query, setQuery] = useState('')

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase()
    return students.filter((s) => {
      if (excludeIds?.has(s.student_id)) return false
      if (!q) return true
      return (
        s.student_id.toLowerCase().includes(q) ||
        (s.name || '').toLowerCase().includes(q)
      )
    })
  }, [students, query, excludeIds])

  const pickedCount = Object.values(selected).filter(Boolean).length
  const allVisibleSelected =
    visible.length > 0 && visible.every((s) => selected[s.student_id])

  const toggle = (id: string) => {
    onChange({ ...selected, [id]: !selected[id] })
  }

  const toggleAllVisible = () => {
    const next = { ...selected }
    const turnOn = !allVisibleSelected
    for (const s of visible) next[s.student_id] = turnOn
    onChange(next)
  }

  return (
    <div className="student-picker">
      <div className="student-picker-toolbar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索姓名或学号"
        />
        <button type="button" className="btn-text" onClick={toggleAllVisible} disabled={!visible.length}>
          {allVisibleSelected ? '取消全选' : '全选当前'}
        </button>
        <span>已选 {pickedCount} 人</span>
      </div>
      {visible.length === 0 ? (
        <p className="empty-hint">{students.length ? '没有匹配的学生' : emptyHint}</p>
      ) : (
        <ul className="student-picker-list">
          {visible.map((s) => (
            <li key={s.student_id}>
              <label>
                <input
                  type="checkbox"
                  checked={Boolean(selected[s.student_id])}
                  onChange={() => toggle(s.student_id)}
                />
                <strong>{s.name || s.student_id}</strong>
                <span>{s.student_id}</span>
              </label>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export function selectedIds(selected: Record<string, boolean>) {
  return Object.entries(selected)
    .filter(([, on]) => on)
    .map(([id]) => id)
}
