import type { PartData } from '../types'

export type GradeStatus = 'correct' | 'wrong' | 'blank'

export interface GradeItem {
  number: number
  user: string
  correct: string
  status: GradeStatus
}

export interface GradeResult {
  total: number
  correct: number
  wrong: number
  blank: number
  score: number
  items: GradeItem[]
}

export interface AnswerKey {
  sId: number
  label?: string
  answers: Record<string, string>
}

function norm(value: string) {
  return value.trim().replace(/\s+/g, ' ').toLowerCase()
}

const ALIASES: Record<string, string[]> = {
  '30': ['30', 'thirty', '£30', '£ 30'],
  thirty: ['30', 'thirty'],
  '10': ['10', 'ten'],
  ten: ['10', 'ten'],
  '125': ['125', 'one hundred and twenty-five', 'one hundred twenty-five'],
  '75': ['75', 'seventy-five', 'seventy five'],
  '239': ['239', 'two hundred and thirty-nine', 'two hundred thirty-nine'],
  '250': ['250', 'two hundred and fifty', 'two hundred fifty'],
  '2.30': ['2.30', '2:30', 'two thirty'],
  '48': ['48', 'forty-eight', 'forty eight'],
  '67.50': ['67.50', '67.5', 'sixty-seven fifty'],
  "king's": ['king\'s', 'kings', "king's"],
  photos: ['photos', 'photographs', 'pictures'],
  chefs: ['chefs', 'cooks'],
  journalists: ['journalists', 'reporters'],
  colour: ['colour', 'color'],
  behaviour: ['behaviour', 'behavior'],
  jewellery: ['jewellery', 'jewelry'],
  cafe: ['cafe', 'café'],
  café: ['cafe', 'café'],
  metals: ['metals', 'metal'],
  metal: ['metals', 'metal'],
  holidays: ['holidays', 'holiday'],
  holiday: ['holidays', 'holiday'],
  wifi: ['wifi', 'wi-fi', 'wi fi'],
  fermentation: ['fermentation', 'fermentation process'],
  '13 january': ['13 january', '13th january', '13th of january', '13.01', '13.1', '13/01'],
  '6 april': ['6 april', '6th april', '6th of april', '06.04', '6.4', '06/04'],
  police: ['police', 'Police'],
}

function matchAnswer(user: string, correct: string) {
  const u = norm(user)
  if (!u) return false
  const alts = correct
    .split(/\s*[/|]\s*/)
    .map((x) => x.trim())
    .filter(Boolean)
  const candidates = alts.length ? alts : [correct]
  return candidates.some((ans) => {
    const c = norm(ans)
    if (u === c) return true
    const uAliases = ALIASES[u] || ALIASES[c] || [u]
    const cAliases = ALIASES[c] || ALIASES[u] || [c]
    return uAliases.some((a) => cAliases.includes(a)) || cAliases.includes(u)
  })
}

export function gradePart(
  part: PartData,
  userAnswers: Record<string, string>,
  key: AnswerKey,
): GradeResult {
  const items: GradeItem[] = part.questions.map((q) => {
    const num = String(q.number)
    const user = (userAnswers[num] || '').trim()
    const correct = (key.answers[num] || '').trim()
    let status: GradeStatus = 'blank'
    if (!user) status = 'blank'
    else if (matchAnswer(user, correct)) status = 'correct'
    else status = 'wrong'
    return { number: q.number, user, correct, status }
  })

  const correct = items.filter((i) => i.status === 'correct').length
  const wrong = items.filter((i) => i.status === 'wrong').length
  const blank = items.filter((i) => i.status === 'blank').length

  return {
    total: items.length,
    correct,
    wrong,
    blank,
    score: correct,
    items,
  }
}

/** Keep existing marking; fill unanswered paper questions as blank. */
export function padItemsToPaper(
  part: PartData,
  items: GradeItem[],
  answers: Record<string, string> = {},
): GradeItem[] {
  const byNum = new Map((items || []).map((it) => [Number(it.number), it]))
  return (part.questions || []).map((q) => {
    const existing = byNum.get(q.number)
    if (existing) return existing
    const user = String(answers[String(q.number)] || '').trim()
    return {
      number: q.number,
      user,
      correct: '',
      status: user ? ('wrong' as const) : ('blank' as const),
    }
  })
}

export function recountGrade(items: GradeItem[]) {
  const correct = items.filter((i) => i.status === 'correct').length
  const wrong = items.filter((i) => i.status === 'wrong').length
  const blank = items.filter((i) => i.status === 'blank').length
  return { total: items.length, correct, wrong, blank, score: correct }
}
