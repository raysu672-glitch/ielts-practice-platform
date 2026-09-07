import { gradePart, type GradeResult } from './grade'
import type { PartData, Subject } from '../types'
import {
  answersKey,
  getBookId,
  loadAnswerKey,
  loadAnswers,
  loadPart,
  parseTestNo,
} from './data'

export interface StoredResult {
  subject: Subject
  sId: number
  label: string
  testNo: number
  sPart: number
  correct: number
  total: number
  wrong: number
  blank: number
  pct: number
  submittedAt: string
}

function resultsKey(bookId = getBookId()) {
  return `mock-results:c${bookId}:v1`
}

function resultId(subject: Subject, sId: number) {
  return `${subject}:${sId}`
}

export function loadAllLocalStoredResults(): (StoredResult & {
  bookId: number
  answers: Record<string, string>
})[] {
  const out: (StoredResult & { bookId: number; answers: Record<string, string> })[] = []
  try {
    for (const storageKey of Object.keys(localStorage)) {
      const match = storageKey.match(/^mock-results:c(\d+):v1$/)
      if (!match) continue
      const bookId = Number(match[1])
      const raw = localStorage.getItem(storageKey)
      if (!raw) continue
      const map = JSON.parse(raw) as Record<string, StoredResult>
      for (const item of Object.values(map)) {
        if (!item || !item.subject || !item.sId) continue
        out.push({
          ...item,
          bookId,
          answers: loadAnswers(item.subject, item.sId, bookId),
        })
      }
    }
  } catch {
    /* ignore broken local results */
  }
  out.sort((a, b) => String(b.submittedAt || '').localeCompare(String(a.submittedAt || '')))
  return out
}

export function loadLocalModuleResults(
  subject: Subject,
  sPart: number,
): (StoredResult & { bookId: number; answers: Record<string, string> })[] {
  return loadAllLocalStoredResults().filter(
    (item) => item.subject === subject && Number(item.sPart) === sPart,
  )
}

export function loadAllResults(bookId = getBookId()): StoredResult[] {
  try {
    const raw = localStorage.getItem(resultsKey(bookId))
    if (!raw) return []
    const map = JSON.parse(raw) as Record<string, StoredResult>
    return Object.values(map).sort((a, b) => {
      if (a.subject !== b.subject) return a.subject.localeCompare(b.subject)
      if (a.testNo !== b.testNo) return a.testNo - b.testNo
      return a.sPart - b.sPart
    })
  } catch {
    return []
  }
}

export function loadResult(subject: Subject, sId: number, bookId = getBookId()): StoredResult | null {
  try {
    const raw = localStorage.getItem(resultsKey(bookId))
    if (!raw) return null
    const map = JSON.parse(raw) as Record<string, StoredResult>
    return map[resultId(subject, sId)] || null
  } catch {
    return null
  }
}

export function saveStoredResult(
  subject: Subject,
  part: PartData,
  graded: GradeResult,
  bookId = getBookId(),
): StoredResult {
  const raw = localStorage.getItem(resultsKey(bookId))
  const map: Record<string, StoredResult> = raw ? JSON.parse(raw) : {}
  const entry: StoredResult = {
    subject,
    sId: part.sId,
    label: part.sName.replace(/^【听力】|【阅读】/, '').trim(),
    testNo: parseTestNo(part.sName),
    sPart: part.sPart,
    correct: graded.correct,
    total: graded.total,
    wrong: graded.wrong,
    blank: graded.blank,
    pct: graded.total ? Math.round((graded.correct / graded.total) * 100) : 0,
    submittedAt: new Date().toISOString(),
  }
  map[resultId(subject, part.sId)] = entry
  localStorage.setItem(resultsKey(bookId), JSON.stringify(map))
  return entry
}

export function clearPartAttempt(subject: Subject, sId: number, bookId = getBookId()) {
  localStorage.removeItem(answersKey(subject, sId, bookId))
  const raw = localStorage.getItem(resultsKey(bookId))
  if (!raw) return
  const map = JSON.parse(raw) as Record<string, StoredResult>
  delete map[resultId(subject, sId)]
  localStorage.setItem(resultsKey(bookId), JSON.stringify(map))
}

export function clearAllAttempts(bookId = getBookId()) {
  const prefix = `mock-answers:c${bookId}:`
  for (const key of Object.keys(localStorage)) {
    if (key.startsWith(prefix)) localStorage.removeItem(key)
  }
  localStorage.removeItem(resultsKey(bookId))
}

export async function submitCurrentAnswers(
  subject: Subject,
  sId: number,
  bookId = getBookId(),
) {
  const [part, key] = await Promise.all([
    loadPart(subject, sId, bookId),
    loadAnswerKey(subject, sId, bookId),
  ])
  const answers = loadAnswers(subject, sId, bookId)
  const graded = gradePart(part, answers, key)
  const stored = saveStoredResult(subject, part, graded, bookId)
  return { part, graded, stored }
}
