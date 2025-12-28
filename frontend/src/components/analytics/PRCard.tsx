import { format } from 'date-fns'
import type { PR } from '../../services/analytics.service'

interface PRCardProps {
  pr: PR
  isLatest?: boolean
}

export default function PRCard({ pr, isLatest = false }: PRCardProps) {
  const formattedDate = format(new Date(pr.date), 'dd.MM.yyyy')

  return (
    <div
      className={`bg-white p-4 rounded-lg shadow ${
        isLatest ? 'border-2 border-yellow-400' : ''
      }`}
    >
      {isLatest && (
        <div className="mb-2">
          <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-semibold px-2 py-1 rounded">
            Последний PR
          </span>
        </div>
      )}
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{pr.exercise_name}</h3>
      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-3xl font-bold text-purple-600">{pr.weight}</span>
        <span className="text-gray-600">кг</span>
        <span className="text-gray-500">× {pr.reps} повторений</span>
      </div>
      <p className="text-sm text-gray-500">{formattedDate}</p>
    </div>
  )
}

