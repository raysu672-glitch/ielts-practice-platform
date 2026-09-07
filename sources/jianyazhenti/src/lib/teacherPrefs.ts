import {
  DEFAULT_PACK_SUBJECT,
  isPackSubject,
  type PackSubject,
} from './packSubjects'

type TeacherMe = {
  data?: {
    role?: string
    teacher?: {
      teacher_id?: string
      jianya_last_subject?: string
    }
  }
}

function storageKey(teacherId: string) {
  return `jianya-last-subject:${teacherId}`
}

const SHARED_KEY = 'jianya-last-subject'

export function peekLocalPackSubject(): PackSubject {
  try {
    const raw = localStorage.getItem(SHARED_KEY) || ''
    if (isPackSubject(raw)) return raw
  } catch {
    /* ignore */
  }
  return DEFAULT_PACK_SUBJECT
}

export async function loadTeacherPackSubject(): Promise<{
  teacherId: string
  subject: PackSubject
}> {
  let teacherId = ''
  let subject = DEFAULT_PACK_SUBJECT
  try {
    const response = await fetch('/api/auth/me?role=teacher', { credentials: 'include' })
    const body = (await response.json()) as TeacherMe
    teacherId = String(body.data?.teacher?.teacher_id || '')
    const server = String(body.data?.teacher?.jianya_last_subject || '')
    if (isPackSubject(server)) subject = server
  } catch {
    /* 未登录时用默认科目 */
  }
  if (teacherId && subject === DEFAULT_PACK_SUBJECT) {
    try {
      const local = localStorage.getItem(storageKey(teacherId)) || ''
      if (isPackSubject(local)) subject = local
    } catch {
      /* ignore */
    }
  }
  return { teacherId, subject }
}

export async function saveTeacherPackSubject(teacherId: string, subject: PackSubject) {
  if (teacherId) {
    try {
      localStorage.setItem(storageKey(teacherId), subject)
      localStorage.setItem(SHARED_KEY, subject)
    } catch {
      /* ignore */
    }
  } else {
    try {
      localStorage.setItem(SHARED_KEY, subject)
    } catch {
      /* ignore */
    }
  }
  await fetch('/api/jianya/prefs', {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lastSubject: subject }),
  }).catch(() => undefined)
}
