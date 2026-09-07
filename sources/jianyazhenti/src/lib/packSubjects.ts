export type ExamSubject = 'listening' | 'reading'
export type PackSubject = ExamSubject | 'writing' | 'speaking'

export const PACK_SUBJECT_TABS: { id: PackSubject; label: string }[] = [
  { id: 'listening', label: '听力' },
  { id: 'reading', label: '阅读' },
  { id: 'writing', label: '写作' },
  { id: 'speaking', label: '口语' },
]

export const DEFAULT_PACK_SUBJECT: PackSubject = 'listening'

export function isPackSubject(value: string): value is PackSubject {
  return PACK_SUBJECT_TABS.some((tab) => tab.id === value)
}

export function isExamSubject(value: string): value is ExamSubject {
  return value === 'listening' || value === 'reading'
}

export function subjectLabel(subject: string) {
  const tab = PACK_SUBJECT_TABS.find((item) => item.id === subject)
  return tab ? tab.label : '作业'
}
