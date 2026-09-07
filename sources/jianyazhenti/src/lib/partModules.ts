export const PART_MODULE_NAMES: Record<string, string> = {
  reading_p1: '阅读Part1',
  reading_p2: '阅读Part2',
  reading_p3: '阅读Part3',
  listening_p1: '听力Part1',
  listening_p2: '听力Part2',
  listening_p3: '听力Part3',
  listening_p4: '听力Part4',
}

export function moduleTypeForPart(subject: string, sPart: number): string {
  if (subject === 'reading' && sPart >= 1 && sPart <= 3) return `reading_p${sPart}`
  if (subject === 'listening' && sPart >= 1 && sPart <= 4) return `listening_p${sPart}`
  return ''
}

export function parsePartModule(moduleType: string): { subject: 'reading' | 'listening'; sPart: number } | null {
  const match = String(moduleType || '').match(/^(reading|listening)_p([1-4])$/)
  if (!match) return null
  const subject = match[1] as 'reading' | 'listening'
  const sPart = Number(match[2])
  if (subject === 'reading' && sPart > 3) return null
  return { subject, sPart }
}
