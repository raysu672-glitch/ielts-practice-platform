import type { Manifest, PartData, Subject } from '../types'

const BOOK_KEY = 'mock-book:v1'
export const DEFAULT_BOOK_ID = 21

export interface BookInfo {
  bookId: number
  folder: string
  label: string
  scrapedAt?: string
}

export function getBookId(): number {
  try {
    const raw = localStorage.getItem(BOOK_KEY)
    const n = raw ? Number(raw) : DEFAULT_BOOK_ID
    return Number.isFinite(n) && n > 0 ? n : DEFAULT_BOOK_ID
  } catch {
    return DEFAULT_BOOK_ID
  }
}

export function setBookId(bookId: number) {
  localStorage.setItem(BOOK_KEY, String(bookId))
}

export function bookFolder(bookId = getBookId()) {
  return `academic${bookId}`
}

export function dataBase(bookId = getBookId()) {
  return `/exam-data/${bookFolder(bookId)}`
}

let catalogCache: Promise<BookInfo[]> | null = null
const manifestCache = new Map<number, Promise<Manifest>>()

function friendlyFetchError(fallback: string, err: unknown) {
  const message = err instanceof Error ? err.message : ''
  if (/failed to fetch|networkerror|load failed/i.test(message)) {
    return fallback
  }
  return message || fallback
}

async function fetchJson<T>(url: string, errorMessage: string): Promise<T> {
  let last: unknown
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const r = await fetch(url)
      if (!r.ok) throw new Error(errorMessage)
      return (await r.json()) as T
    } catch (err) {
      last = err
      if (attempt < 2) {
        await new Promise((resolve) => window.setTimeout(resolve, 250 * (attempt + 1)))
      }
    }
  }
  throw new Error(friendlyFetchError(errorMessage, last))
}

export async function loadCatalog(): Promise<BookInfo[]> {
  if (!catalogCache) {
    catalogCache = fetchJson<{ books?: BookInfo[] }>('/exam-data/catalog.json', '无法加载题库目录').then(
      (data) => data.books || [],
    )
    catalogCache.catch(() => {
      catalogCache = null
    })
  }
  return catalogCache
}

export async function loadManifest(bookId = getBookId()): Promise<Manifest> {
  const id = bookId
  const cached = manifestCache.get(id)
  if (cached) return cached
  const pending = fetchJson<Manifest>(`${dataBase(id)}/manifest.json`, `无法加载题库索引（C${id}）`)
  manifestCache.set(id, pending)
  pending.catch(() => {
    manifestCache.delete(id)
  })
  return pending
}

export async function loadPart(
  subject: Subject,
  sId: number,
  bookId = getBookId(),
): Promise<PartData> {
  return fetchJson<PartData>(
    `${dataBase(bookId)}/${subject}/${sId}.json`,
    `无法加载 Part ${sId}`,
  )
}

export function audioSrc(part: PartData, bookId = getBookId()): string | null {
  if (part.audioLocal) return `${dataBase(bookId)}/${part.audioLocal}`
  return part.audioUrl || null
}

export function parseTestNo(sName: string): number {
  const m = sName.match(/Test\s*(\d+)/i)
  return m ? Number(m[1]) : 0
}

export function groupByTest<
  T extends { sId: number; sName: string; sPart: number; questionCount: number },
>(parts: T[]) {
  const map = new Map<number, T[]>()
  for (const p of parts) {
    const t = parseTestNo(p.sName)
    if (!map.has(t)) map.set(t, [])
    map.get(t)!.push(p)
  }
  for (const list of map.values()) {
    list.sort((a, b) => a.sPart - b.sPart)
  }
  return [...map.entries()].sort((a, b) => a[0] - b[0])
}

export function answersKey(subject: Subject, sId: number, bookId = getBookId()) {
  return `mock-answers:c${bookId}:${subject}:${sId}`
}

export function loadAnswers(
  subject: Subject,
  sId: number,
  bookId = getBookId(),
): Record<string, string> {
  try {
    const raw = localStorage.getItem(answersKey(subject, sId, bookId))
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

export function saveAnswers(
  subject: Subject,
  sId: number,
  answers: Record<string, string>,
  bookId = getBookId(),
) {
  localStorage.setItem(answersKey(subject, sId, bookId), JSON.stringify(answers))
}

export async function loadAnswerKey(subject: Subject, sId: number, bookId = getBookId()) {
  const url = `${dataBase(bookId)}/keys/${subject}/${sId}.json`
  const r = await fetch(url)
  const ct = r.headers.get('content-type') || ''
  if (!r.ok) {
    throw new Error(`本题暂无标准答案（keys/${subject}/${sId}.json）`)
  }
  if (!ct.includes('json')) {
    throw new Error(`本题暂无标准答案（keys/${subject}/${sId}.json）`)
  }
  try {
    return (await r.json()) as { sId: number; label?: string; answers: Record<string, string> }
  } catch {
    throw new Error(`标准答案文件格式错误（keys/${subject}/${sId}.json）`)
  }
}
