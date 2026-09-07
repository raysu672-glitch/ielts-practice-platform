import { useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getBookId } from '../lib/data'
import type { Subject } from '../types'

/** Old result page: redirect to on-paper review (same as assignment). */
export default function Result() {
  const { subject = 'listening', sId = '' } = useParams()
  const navigate = useNavigate()
  const id = Number(sId)
  const bookId = getBookId()
  const sub = subject as Subject
  const reviewTo = `/exam/${bookId}/${sub}/${id}?review=1&from=overview`

  useEffect(() => {
    if (!id) return
    navigate(reviewTo, { replace: true })
  }, [id, navigate, reviewTo])

  return (
    <div className="result-shell result-loading">
      <p>正在打开原卷比对…</p>
      <Link className="btn-link" to={reviewTo}>
        若未跳转请点此进入
      </Link>
    </div>
  )
}
