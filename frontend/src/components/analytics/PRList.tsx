import { useState, useEffect } from 'react'
import { analyticsService, type PR } from '../../services/analytics.service'
import PRCard from './PRCard'

interface PRListProps {
  limit?: number
  showLatest?: boolean
}

export default function PRList({ limit = 5, showLatest = true }: PRListProps) {
  const [prs, setPRs] = useState<PR[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPRs()
  }, [limit])

  const loadPRs = async () => {
    try {
      setLoading(true)
      const data = await analyticsService.getAllPRs(limit)
      setPRs(data.prs)
    } catch (err) {
      console.error('Ошибка загрузки PR:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Загрузка рекордов...</p>
      </div>
    )
  }

  if (prs.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Пока нет личных рекордов</p>
        <p className="text-sm text-gray-400 mt-2">Начните тренироваться, чтобы установить свой первый PR!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {prs.map((pr, index) => (
        <PRCard key={pr.exercise_id} pr={pr} isLatest={showLatest && index === 0} />
      ))}
    </div>
  )
}



