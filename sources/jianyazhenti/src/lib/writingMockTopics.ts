import bank from '../data/writing-mock-topics.json' with { type: 'json' }

export interface MockWritingTopic {
  id: number
  title: string
  qType: string
  task: 'task1' | 'task2'
  /** Task2 的话题分类（教育类/环境类/生活类等） */
  topic?: string
  prompt: string
  /** 展示用的题型/话题说明 */
  examMeta: string
  /** Task1 图表图片的本地路径（相对 /exam-data/jijing/） */
  image?: string
}

type RawTask1 = { id: number; name: string; qType: string; prompt: string }
type RawTask2 = { id: number; name: string; qType: string; topic: string; prompt: string }

type MockBank = {
  source?: string
  task1: RawTask1[]
  task2: RawTask2[]
}

const DATA = bank as MockBank

/** Task1 图表图本地文件名（含扩展名）。 */
const TASK1_IMAGES: Record<number, string> = {
  1255: '1255.png',
  1240: '1240.png',
  1196: '1196.jpg',
  1171: '1171.jpg',
  1106: '1106.png',
  1082: '1082.png',
  1063: '1063.png',
  1057: '1057.png',
  1055: '1055.png',
  1048: '1048.png',
  1046: '1046.png',
  1039: '1039.png',
  1037: '1037.png',
  1007: '1007.png',
  1005: '1005.png',
  960: '960.png',
  958: '958.png',
  956: '956.png',
  954: '954.png',
}

function imageUrl(id: number): string | undefined {
  const fn = TASK1_IMAGES[id]
  return fn ? `/exam-data/jijing/${fn}` : undefined
}

function task1Pool(): MockWritingTopic[] {
  return (DATA.task1 || []).map((row) => ({
    id: row.id,
    title: row.name,
    qType: row.qType,
    task: 'task1' as const,
    prompt: row.prompt,
    examMeta: row.qType,
    image: imageUrl(row.id),
  }))
}

function task2Pool(): MockWritingTopic[] {
  return (DATA.task2 || []).map((row) => ({
    id: row.id,
    title: row.name,
    qType: row.qType,
    topic: row.topic,
    task: 'task2' as const,
    prompt: row.prompt,
    examMeta: [row.qType, row.topic].filter(Boolean).join(' · '),
  }))
}

/** 从当季真题中随机抽一篇小作文/大作文。 */
export function pickMockWritingTopic(task: 'task1' | 'task2'): MockWritingTopic | null {
  const pool = task === 'task1' ? task1Pool() : task2Pool()
  if (!pool.length) return null
  return pool[Math.floor(Math.random() * pool.length)]
}

/** 列出当季真题全部题目（Task1 在前，Task2 在后）。 */
export function listMockWritingTopics(): MockWritingTopic[] {
  return [...task1Pool(), ...task2Pool()]
}