import type { Subject } from '../types'
import type { GradeResult } from './grade'

export const DEFAULT_STUDENT_ID = 'local'

export interface PartRef {
  bookId: number
  subject: Subject
  sId: number
  testNo: number
  sPart: number
  label: string
  questionCount: number
}

export interface AssignmentPack {
  id: string
  title: string
  subject: Subject
  description?: string
  parts: PartRef[]
  builtin?: boolean
  createdAt?: string
}

export interface Assignment {
  id: string
  title: string
  subject: Subject
  parts: PartRef[]
  createdAt: string
  packId?: string
}

export interface AssignmentSubmission {
  assignmentId: string
  studentId: string
  bookId: number
  subject: Subject
  sId: number
  status: 'submitted'
  answers: Record<string, string>
  correct: number
  total: number
  wrong: number
  blank: number
  pct: number
  submittedAt: string
}

type ApiEnvelope<T> = { data?: T; error?: { message?: string } | null }

async function api<T>(url: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers || {})
  if (init?.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  const r = await fetch(url, {
    credentials: 'include',
    ...init,
    headers,
  })
  const body = (await r.json().catch(() => ({}))) as ApiEnvelope<T>
  if (!r.ok || body.error) {
    throw new Error((body.error && body.error.message) || `请求失败 ${r.status}`)
  }
  return body.data as T
}

function partKey(bookId: number, subject: Subject, sId: number) {
  return `${bookId}:${subject}:${sId}`
}

export async function loadBuiltinPacks(): Promise<AssignmentPack[]> {
  const packs = await listAllPacks()
  return packs.filter((p) => p.builtin)
}

export async function listAllPacks(): Promise<AssignmentPack[]> {
  return api<AssignmentPack[]>('/api/jianya/packs')
}

export async function getPack(id: string): Promise<AssignmentPack | null> {
  const packs = await listAllPacks()
  return packs.find((p) => p.id === id) || null
}

export async function createPack(input: {
  title: string
  subject: Subject
  description?: string
  parts: PartRef[]
}): Promise<AssignmentPack> {
  return api<AssignmentPack>('/api/jianya/packs', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export async function deletePack(id: string): Promise<void> {
  await api<{ ok: boolean }>(`/api/jianya/packs/${encodeURIComponent(id)}`, { method: 'DELETE' })
}

export function packQuestionCount(pack: AssignmentPack) {
  return pack.parts.reduce((s, p) => s + (p.questionCount || 0), 0)
}

export async function listAssignments(): Promise<Assignment[]> {
  return api<Assignment[]>('/api/jianya/assignments')
}

export async function listMySubmissions(): Promise<
  (AssignmentSubmission & { assignmentTitle?: string; sPart?: number; label?: string })[]
> {
  try {
    return await api<
      (AssignmentSubmission & { assignmentTitle?: string; sPart?: number; label?: string })[]
    >('/api/jianya/me/submissions')
  } catch {
    const assignments = await listAssignments().catch(() => [])
    const nested = await Promise.all(
      assignments.map(async (assignment) => {
        const rows = await listSubmissions(assignment.id).catch(() => [])
        return rows.map((row) => {
          const part = assignment.parts.find(
            (p) => p.bookId === row.bookId && p.subject === row.subject && p.sId === row.sId,
          )
          return {
            ...row,
            assignmentTitle: assignment.title,
            sPart: part?.sPart || 0,
            label: part?.label || '',
          }
        })
      }),
    )
    return nested.flat()
  }
}

export async function getAssignment(id: string): Promise<Assignment | null> {
  try {
    return await api<Assignment>(`/api/jianya/assignments/${encodeURIComponent(id)}`)
  } catch {
    return null
  }
}

export async function createAssignment(input: {
  title: string
  subject: Subject
  parts: PartRef[]
  packId?: string
}): Promise<Assignment> {
  return api<Assignment>('/api/jianya/assignments', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export async function publishFromPacks(
  packs: AssignmentPack[],
  titlePrefix = '',
): Promise<Assignment[]> {
  if (!packs.length) throw new Error('请至少选择一个作业包')
  return api<Assignment[]>('/api/jianya/assignments/publish-packs', {
    method: 'POST',
    body: JSON.stringify({
      packIds: packs.map((p) => p.id),
      titlePrefix,
    }),
  })
}

export async function deleteAssignment(id: string): Promise<void> {
  await api<{ ok: boolean }>(`/api/jianya/assignments/${encodeURIComponent(id)}`, {
    method: 'DELETE',
  })
}

export async function loadAssignmentAnswers(
  assignmentId: string,
  bookId: number,
  subject: Subject,
  sId: number,
): Promise<Record<string, string>> {
  const q = new URLSearchParams({
    assignment_id: assignmentId,
    book_id: String(bookId),
    subject,
    s_id: String(sId),
  })
  return api<Record<string, string>>(`/api/jianya/drafts?${q.toString()}`)
}

export async function saveAssignmentAnswers(
  assignmentId: string,
  bookId: number,
  subject: Subject,
  sId: number,
  answers: Record<string, string>,
): Promise<void> {
  await api<Record<string, string>>('/api/jianya/drafts', {
    method: 'PUT',
    body: JSON.stringify({
      assignmentId,
      bookId,
      subject,
      sId,
      answers,
    }),
  })
}

export async function getSubmission(
  assignmentId: string,
  bookId: number,
  subject: Subject,
  sId: number,
): Promise<AssignmentSubmission | null> {
  const list = await listSubmissions(assignmentId)
  return (
    list.find(
      (s) => s.bookId === bookId && s.subject === subject && s.sId === sId,
    ) || null
  )
}

export async function listSubmissions(
  assignmentId: string,
  studentId?: string,
): Promise<AssignmentSubmission[]> {
  const q = studentId ? `?student_id=${encodeURIComponent(studentId)}` : ''
  return api<AssignmentSubmission[]>(
    `/api/jianya/assignments/${encodeURIComponent(assignmentId)}/submissions${q}`,
  )
}

export function isPartSubmitted(
  submissions: AssignmentSubmission[],
  bookId: number,
  subject: Subject,
  sId: number,
) {
  return submissions.some((s) => s.bookId === bookId && s.subject === subject && s.sId === sId)
}

export async function saveSubmission(input: {
  assignmentId: string
  bookId: number
  subject: Subject
  sId: number
  answers: Record<string, string>
  graded: GradeResult
}): Promise<AssignmentSubmission> {
  const pct = input.graded.total
    ? Math.round((input.graded.correct / input.graded.total) * 100)
    : 0
  return api<AssignmentSubmission>('/api/jianya/submissions', {
    method: 'POST',
    body: JSON.stringify({
      assignmentId: input.assignmentId,
      bookId: input.bookId,
      subject: input.subject,
      sId: input.sId,
      answers: input.answers,
      graded: input.graded,
      pct,
    }),
  })
}

export function assignmentPartPath(
  assignmentId: string,
  part: Pick<PartRef, 'bookId' | 'subject' | 'sId'>,
  review = false,
) {
  const q = new URLSearchParams({ assignment: assignmentId })
  if (review) q.set('review', '1')
  return `/exam/${part.bookId}/${part.subject}/${part.sId}?${q.toString()}`
}

export function partRefId(part: Pick<PartRef, 'bookId' | 'subject' | 'sId'>) {
  return partKey(part.bookId, part.subject, part.sId)
}
