import type { PartData } from '../types'
import type { GradeItem, GradeStatus } from './grade'

const RANGE_RE = /questions?\s*(\d+)\s*[-–—~至到]+\s*(\d+)/i

export type TypeStat = { correct: number; total: number; wrong: number; blank: number }

export interface HistoryGradeItem extends GradeItem {
  qType: string
}

function classifyInstruction(text: string): string {
  const t = String(text || '')
    .replace(/\s+/g, ' ')
    .toLowerCase()
  if (!t.trim()) return ''
  if (/do the following statements agree/.test(t)) {
    return /yes/.test(t) ? '判断题（Y/N/NG）' : '判断题（T/F/NG）'
  }
  if (/true[\s/,-]*false[\s/,-]*not given/.test(t) || (/true/.test(t) && /false/.test(t) && /not given/.test(t))) {
    return '判断题（T/F/NG）'
  }
  if (/yes[\s/,-]*no[\s/,-]*not given/.test(t) || (/yes/.test(t) && /no/.test(t) && /not given/.test(t))) {
    return '判断题（Y/N/NG）'
  }
  if (/which paragraph contains|which section contains/.test(t)) return '段落信息匹配'
  if (/heading/.test(t)) return '标题匹配'
  if (/complete the summary|summary below/.test(t)) return '摘要填空'
  if (/complete the notes|complete the table|complete the flow-?chart|complete the diagram/.test(t)) {
    return '图表填空'
  }
  if (/label (the )?(map|diagram|plan)/.test(t) || /labell?ing/.test(t)) return '标注题'
  if (/complete the sentences/.test(t)) return '完成句子'
  if (/choose.*(letter|correct letter|correct answer)|multiple choice/.test(t)) return '选择题'
  if (/match /.test(t) || /matching/.test(t)) return '匹配题'
  if (/answer the questions|short.?answer/.test(t)) return '简答题'
  if (/choose.*word|one word|no more than/.test(t) && /complete|write/.test(t)) return '填空题'
  return ''
}

function fallbackType(qType: string): string {
  if (qType === 'single_choice') return '选择题'
  if (qType === 'gap_fill') return '填空题'
  return '其他'
}

export function typesForPart(part: PartData): Record<number, string> {
  const ranges: { start: number; end: number; label: string }[] = []
  const ins = part.instructions || []
  for (let i = 0; i < ins.length; i++) {
    const compact = String(ins[i] || '').replace(/\s+/g, ' ')
    const match = compact.match(RANGE_RE)
    if (!match) continue
    const start = Number(match[1])
    const end = Number(match[2])
    let label = ''
    for (let j = i + 1; j < ins.length; j++) {
      const next = String(ins[j] || '').replace(/\s+/g, ' ')
      if (RANGE_RE.test(next)) break
      label = classifyInstruction(ins[j]) || label
      if (label) break
    }
    ranges.push({ start, end, label })
  }

  const out: Record<number, string> = {}
  for (const q of part.questions || []) {
    const hit = ranges.find((r) => q.number >= r.start && q.number <= r.end && r.label)
    out[q.number] = hit?.label || fallbackType(q.type)
  }
  return out
}

export function attachQuestionTypes(part: PartData, items: GradeItem[]): HistoryGradeItem[] {
  const map = typesForPart(part)
  return items.map((it) => ({
    ...it,
    qType: map[it.number] || '其他',
  }))
}

export function buildTypeStats(items: { qType?: string; status: GradeStatus }[]): Record<string, TypeStat> {
  const stats: Record<string, TypeStat> = {}
  for (const item of items) {
    const key = item.qType || '其他'
    if (!stats[key]) stats[key] = { correct: 0, total: 0, wrong: 0, blank: 0 }
    stats[key].total += 1
    if (item.status === 'correct') stats[key].correct += 1
    else if (item.status === 'wrong') stats[key].wrong += 1
    else stats[key].blank += 1
  }
  return stats
}

export function hasTypeStats(stats: Record<string, TypeStat> | undefined): boolean {
  return Object.values(stats || {}).some((row) => (row?.total || 0) > 0)
}

/** 试卷上各题型题量。没有逐题对错时，正确数记 0、空白记为全部。 */
export function typeStatsFromPart(part: PartData): Record<string, TypeStat> {
  const map = typesForPart(part)
  const stats: Record<string, TypeStat> = {}
  for (const q of part.questions || []) {
    const key = map[q.number] || fallbackType(q.type)
    if (!stats[key]) stats[key] = { correct: 0, total: 0, wrong: 0, blank: 0 }
    stats[key].total += 1
    stats[key].blank += 1
  }
  return stats
}
