import { useState, useEffect } from 'react'
import { analyticsService, type NewRecord } from '../../services/analytics.service'

export default function NewRecordsCard() {
  const [newRecords, setNewRecords] = useState<NewRecord[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNewRecords()
  }, [])

  const loadNewRecords = async () => {
    try {
      setLoading(true)
      const data = await analyticsService.getNewRecords()
      setNewRecords(data.new_records)
    } catch (err) {
      console.error('Ошибка загрузки новых рекордов:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Новые рекорды</h2>
        <p className="text-gray-600">Загрузка...</p>
      </div>
    )
  }

  if (newRecords.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Новые рекорды</h2>
        <p className="text-gray-500 text-center py-4">Пока нет новых рекордов</p>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Новые рекорды</h2>
      <div className="space-y-3">
        {newRecords.map((record, index) => (
          <div
            key={`${record.exercise_id}-${index}`}
            className={`p-4 rounded-lg border-l-4 ${
              record.type === 'first_time'
                ? 'bg-blue-50 border-blue-500'
                : 'bg-green-50 border-green-500'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${
                      record.type === 'first_time'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {record.type === 'first_time' ? '🎯 Первое выполнение' : '🏆 Новый PR'}
                  </span>
                  <span className="font-semibold text-gray-900">{record.exercise_name}</span>
                </div>
                <p className="text-sm text-gray-600">
                  {record.weight} кг × {record.reps} повторений
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(record.date).toLocaleDateString('ru-RU')}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


