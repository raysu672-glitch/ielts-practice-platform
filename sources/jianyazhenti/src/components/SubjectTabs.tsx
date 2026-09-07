import { PACK_SUBJECT_TABS, type PackSubject } from '../lib/packSubjects'

export default function SubjectTabs({
  value,
  onChange,
}: {
  value: PackSubject
  onChange: (subject: PackSubject) => void
}) {
  return (
    <div className="tabs pack-subject-tabs" role="tablist" aria-label="作业科目">
      {PACK_SUBJECT_TABS.map((tab) => (
        <button
          key={tab.id}
          type="button"
          className={`tab ${value === tab.id ? 'active' : ''}`}
          onClick={() => onChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}
