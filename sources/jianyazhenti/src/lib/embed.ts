export function isEmbedded() {
  try {
    return window.self !== window.top
  } catch {
    return true
  }
}

export function markEmbedded() {
  const params = new URLSearchParams(window.location.search)
  const studentId = params.get('student_id')
  if (studentId) {
    sessionStorage.setItem('jianya-student-id', studentId)
  }
  if (isEmbedded()) {
    document.documentElement.classList.add('embedded')
  }
}

export function currentMockStudentId() {
  try {
    return sessionStorage.getItem('jianya-student-id') || 'local'
  } catch {
    return 'local'
  }
}

export const APP_BASE = (import.meta.env.BASE_URL || '/').replace(/\/$/, '')

export function absoluteAppUrl(path: string) {
  const suffix = path.startsWith('/') ? path : `/${path}`
  return `${window.location.origin}${APP_BASE}${suffix}`
}
