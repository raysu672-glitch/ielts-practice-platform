import bank from '../data/writing-theme-bank.json' with { type: 'json' }
import { writingTopics } from './writingTopics'

export interface WritingRefItem {
  zh: string
  en: string
}

type ThemeBank = {
  phrases: Record<string, WritingRefItem[]>
  sentences: Record<string, WritingRefItem[]>
}

const DATA = bank as ThemeBank

export function writingReferenceFor(sId?: number) {
  const topic = writingTopics().find((row) => row.id === sId)
  const themes = topic?.themes || []
  const vocab: WritingRefItem[] = []
  const sentences: WritingRefItem[] = []
  const seenVocab = new Set<string>()
  const seenSent = new Set<string>()
  for (const theme of themes) {
    for (const item of DATA.phrases[theme] || []) {
      const key = `${item.en}::${item.zh}`
      if (seenVocab.has(key)) continue
      seenVocab.add(key)
      vocab.push(item)
    }
    for (const item of DATA.sentences[theme] || []) {
      if (seenSent.has(item.zh)) continue
      seenSent.add(item.zh)
      sentences.push(item)
    }
  }
  return { themes, vocab: vocab.slice(0, 24), sentences: sentences.slice(0, 12) }
}
