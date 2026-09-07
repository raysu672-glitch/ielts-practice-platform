export type Subject = 'listening' | 'reading'

export interface ManifestPart {
  sId: number
  sName: string
  sPart: number
  questionCount: number
  hasAudio?: boolean
  hasPassageApi?: boolean
  hasPassage?: boolean
  files: {
    html: string
    json: string
    passageHtml?: string
  }
  error?: string
}

export interface Manifest {
  bookId: number
  label: string
  source: string
  scrapedAt: string
  hasCookie: boolean
  parts: {
    listening: ManifestPart[]
    reading: ManifestPart[]
  }
}

export interface Question {
  number: number
  stem: string
  type: 'single_choice' | 'gap_fill' | 'unknown' | string
  options: { value: string; label: string }[]
  questionId: string | null
  answerId: string | null
}

export interface PassageBlock {
  lId: number | null
  title: string | null
  subtitle: string | null
  paragraphs: {
    name?: string | null
    html?: string | null
    text?: string | null
  }[]
}

export interface PartData {
  sId: number
  sName: string
  sSubjects: number
  sPart: number
  subject: Subject
  bindLId?: string
  instructions: string[]
  questions: Question[]
  audioUrl?: string | null
  audioLocal?: string | null
  paperHtml?: string
  passage?: { passages: PassageBlock[] }
}
