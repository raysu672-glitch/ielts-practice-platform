import type { PartRef } from './assignments'
import catalog from '../data/writing-topics.json' with { type: 'json' }

export const WRITING_BOOK_ID = 100

export type WritingTask = 'task1' | 'task2'

export interface WritingTopic {
  id: number
  lesson: number
  lessonTitle: string
  pattern: string
  task: WritingTask
  questionType: string
  title: string
  examMeta: string
  prompt: string
  tips?: string
  themes?: string[]
}

type Catalog = {
  bookId?: number
  topics: WritingTopic[]
}

const DATA = catalog as Catalog

export function writingTopics(): WritingTopic[] {
  return Array.isArray(DATA.topics) ? DATA.topics : []
}

export function writingLessons() {
  const map = new Map<number, { lesson: number; title: string; topics: WritingTopic[] }>()
  for (const topic of writingTopics()) {
    const row = map.get(topic.lesson) || {
      lesson: topic.lesson,
      title: topic.lessonTitle || `第${topic.lesson}课`,
      topics: [],
    }
    row.topics.push(topic)
    map.set(topic.lesson, row)
  }
  return [...map.values()].sort((a, b) => a.lesson - b.lesson)
}

export function writingTaskLabel(task: string) {
  return task === 'task1' ? 'Task 1' : 'Task 2'
}

export function writingTipsFor(part: Pick<PartRef, 'sId'> & { tips?: string } | null | undefined) {
  const own = String(part?.tips || '').trim()
  if (own) return own
  if (!part?.sId) return ''
  const topic = writingTopics().find((row) => row.id === part.sId)
  return String(topic?.tips || '').trim()
}

export function topicToPart(topic: WritingTopic): PartRef {
  return {
    bookId: WRITING_BOOK_ID,
    subject: 'writing',
    sId: topic.id,
    testNo: topic.lesson,
    sPart: topic.task === 'task1' ? 1 : 2,
    label: topic.title,
    questionCount: 1,
    prompt: topic.prompt,
    task: topic.task,
    lesson: topic.lesson,
    pattern: topic.pattern,
    examMeta: topic.examMeta,
    tips: topic.tips,
  }
}
