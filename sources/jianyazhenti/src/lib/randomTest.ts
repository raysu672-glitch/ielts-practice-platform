import { loadCatalog, loadManifest } from './data'
import type { StoredResult } from './results'
import type { Subject } from '../types'

export type PaperRef = {
  bookId: number
  subject: Subject
  sId: number
  sPart: number
  label: string
}

export function paperKey(bookId: number, subject: string, sId: number) {
  return `${bookId}:${subject}:${sId}`
}

export async function listPartsForFilter(
  subject: Subject,
  sPart: number,
  opts?: { bookMin?: number; bookMax?: number },
): Promise<PaperRef[]> {
  const books = (await loadCatalog()).filter((book) => {
    if (opts?.bookMin != null && book.bookId < opts.bookMin) return false
    if (opts?.bookMax != null && book.bookId > opts.bookMax) return false
    return true
  })
  const nested = await Promise.all(
    books.map(async (book) => {
      try {
        const manifest = await loadManifest(book.bookId)
        return (manifest.parts[subject] || [])
          .filter((p) => !p.error && p.sPart === sPart)
          .map((p) => ({
            bookId: book.bookId,
            subject,
            sId: p.sId,
            sPart: p.sPart,
            label: p.sName,
          }))
      } catch {
        return [] as PaperRef[]
      }
    }),
  )
  return nested.flat()
}

export function loadLocalDoneKeys(): Set<string> {
  const keys = new Set<string>()
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
        keys.add(paperKey(bookId, item.subject, item.sId))
      }
    }
  } catch {
    /* ignore broken local results */
  }
  return keys
}

function addDetailKeys(keys: Set<string>, details: unknown) {
  const items = Array.isArray(details) ? details : details ? [details] : []
  for (const item of items) {
    if (!item || typeof item !== 'object') continue
    const row = item as {
      kind?: string
      bookId?: number
      subject?: string
      sId?: number
      parts?: { bookId?: number; subject?: string; sId?: number }[]
    }
    if (row.kind === 'jianya_mock' && Array.isArray(row.parts)) {
      for (const part of row.parts) {
        if (!part?.bookId || !part?.subject || !part?.sId) continue
        keys.add(paperKey(Number(part.bookId), String(part.subject), Number(part.sId)))
      }
      continue
    }
    if (!row.bookId || !row.subject || !row.sId) continue
    keys.add(paperKey(Number(row.bookId), String(row.subject), Number(row.sId)))
  }
}

export async function loadServerDoneKeys(moduleType: string): Promise<Set<string>> {
  const keys = new Set<string>()
  try {
    const r = await fetch('/api/student/test-records', { credentials: 'include' })
    const body = (await r.json()) as { data?: { module_type?: string; details?: unknown }[] }
    for (const rec of body.data || []) {
      const module = String(rec.module_type || '')
      const isMockSet = module === 'mock_reading' || module === 'mock_listening'
      if (moduleType && module && module !== moduleType && !isMockSet) continue
      addDetailKeys(keys, rec.details)
    }
  } catch {
    /* student API unavailable in standalone SPA */
  }
  return keys
}

export async function loadAllDoneKeys(): Promise<Set<string>> {
  const keys = loadLocalDoneKeys()
  try {
    const r = await fetch('/api/student/progress', { credentials: 'include' })
    const body = (await r.json()) as {
      data?: { test_records?: { details?: unknown }[]; study_sessions?: { details?: unknown }[] }
    }
    for (const rec of [...(body.data?.test_records || []), ...(body.data?.study_sessions || [])]) {
      addDetailKeys(keys, rec.details)
    }
  } catch {
    const extra = await loadServerDoneKeys('')
    extra.forEach((k) => keys.add(k))
  }
  return keys
}

export function pickRandomUnused(pool: PaperRef[], done: Set<string>): PaperRef | null {
  if (!pool.length) return null
  const unused = pool.filter((p) => !done.has(paperKey(p.bookId, p.subject, p.sId)))
  const source = unused.length ? unused : pool
  return source[Math.floor(Math.random() * source.length)]
}
