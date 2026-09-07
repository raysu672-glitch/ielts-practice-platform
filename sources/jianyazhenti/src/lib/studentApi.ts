export type StudentApiError = Error & { status?: number }

type Envelope<T> = {
  data?: T
  error?: { message?: string }
}

function asError(status: number, message: string) {
  const err = new Error(message) as StudentApiError
  err.status = status
  return err
}

export function isAuthError(err: unknown) {
  if (!err || typeof err !== 'object') return false
  const status = (err as StudentApiError).status
  const message = err instanceof Error ? err.message : ''
  return status === 401 || /需要学生登录|请先登录/.test(message)
}

export async function studentRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers || {})
  if (init?.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  let response: Response
  try {
    response = await fetch(path, {
      credentials: 'include',
      ...init,
      headers,
    })
  } catch {
    throw asError(0, '网络异常，成绩未能写入服务器，请检查网络后重试')
  }
  const body = (await response.json().catch(() => ({}))) as Envelope<T>
  if (!response.ok || body.error) {
    throw asError(
      response.status,
      body.error?.message || (response.status === 401 ? '请先登录，成绩才能记入历史' : '保存失败，请重试'),
    )
  }
  return body.data as T
}

export async function postStudentJson<T>(path: string, payload: unknown) {
  return studentRequest<T>(path, { method: 'POST', body: JSON.stringify(payload) })
}

export type ProgressPayload = {
  test_records?: Record<string, unknown>[]
  study_sessions?: Record<string, unknown>[]
}

/** Teacher embed: ?teacher_view=1&student_id=2025001 */
export function teacherViewStudentId(): string {
  try {
    const params = new URLSearchParams(window.location.search)
    if (params.get('teacher_view') !== '1') return ''
    return String(params.get('student_id') || '').trim()
  } catch {
    return ''
  }
}

export function isTeacherViewingStudent() {
  return !!teacherViewStudentId()
}

/** Keep teacher_view + student_id (+ embed) when navigating inside jianyazhenti. */
export function withTeacherViewParams(search: URLSearchParams | string = '') {
  const q = new URLSearchParams(typeof search === 'string' ? search : search.toString())
  const sid = teacherViewStudentId()
  if (sid) {
    q.set('teacher_view', '1')
    q.set('student_id', sid)
  }
  if (typeof window !== 'undefined') {
    try {
      const cur = new URLSearchParams(window.location.search)
      if (cur.get('embed') === '1') q.set('embed', '1')
    } catch {
      /* ignore */
    }
  }
  return q
}

export async function loadStudentProgress() {
  const sid = teacherViewStudentId()
  if (sid) {
    return studentRequest<ProgressPayload>(
      `/api/teacher/student-detail?student_id=${encodeURIComponent(sid)}`,
    )
  }
  return studentRequest<ProgressPayload>('/api/student/progress')
}
