import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsService } from '../../services/analytics.service'
import { format, subDays } from 'date-fns'

interface ExerciseProgressProps {
  exerciseId: number | null
  dateRange: { start: string; end: string }
}

export default function ExerciseProgress({ exerciseId, dateRange }: ExerciseProgressProps) {
  const [weightProgress, setWeightProgress] = useState<Array<{ date: string; value: number }>>([])
  const [volumeProgress, setVolumeProgress] = useState<Array<{ date: string; value: number }>>([])
  const [oneRMProgress, setOneRMProgress] = useState<Array<{ date: string; value: number }>>([])
  const [loading, setLoading] = useState(false)
  const [formula, setFormula] = useState('brzycki')

  useEffect(() => {
    if (exerciseId) {
      loadProgress()
    } else {
      setWeightProgress([])
      setVolumeProgress([])
      setOneRMProgress([])
    }
  }, [exerciseId, dateRange, formula])

  const loadProgress = async () => {
    if (!exerciseId) return

    try {
      setLoading(true)

      // Load weight progress
      const weightData = await analyticsService.getWeightProgress(exerciseId, dateRange.start, dateRange.end)
      const weightChart = Object.entries(weightData.progress)
        .sort(([dateA], [dateB]) => new Date(dateA).getTime() - new Date(dateB).getTime())
        .map(([date, weight]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: weight,
        }))
      setWeightProgress(weightChart)

      // Load volume progress
      const volumeData = await analyticsService.getVolumeProgress(exerciseId, dateRange.start, dateRange.end)
      const volumeChart = Object.entries(volumeData.progress)
        .sort(([dateA], [dateB]) => new Date(dateA).getTime() - new Date(dateB).getTime())
        .map(([date, volume]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: Math.round(volume),
        }))
      setVolumeProgress(volumeChart)

      // Load 1RM progress
      const oneRMData = await analyticsService.getExercise1RMProgress(
        exerciseId,
        dateRange.start,
        dateRange.end,
        formula
      )
      const oneRMChart = Object.entries(oneRMData.progress)
        .sort(([dateA], [dateB]) => new Date(dateA).getTime() - new Date(dateB).getTime())
        .map(([date, oneRM]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: Math.round(oneRM * 10) / 10, // Round to 1 decimal
        }))
      setOneRMProgress(oneRMChart)
    } catch (err) {
      console.error('Ошибка загрузки прогресса:', err)
    } finally {
      setLoading(false)
    }
  }

  if (!exerciseId) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-500 text-center py-8">Выберите упражнение для просмотра прогресса</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-500 text-center py-8">Загрузка данных...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* 1RM Formula Selector */}
      <div className="bg-white p-4 rounded-lg shadow">
        <label htmlFor="formula-select" className="block text-sm font-medium text-gray-700 mb-2">
          Формула расчета 1RM
        </label>
        <select
          id="formula-select"
          value={formula}
          onChange={(e) => setFormula(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="brzycki">Brzycki</option>
          <option value="epley">Epley</option>
          <option value="lombardi">Lombardi</option>
        </select>
      </div>

      {/* Weight Progress */}
      {weightProgress.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Прогресс веса (кг)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weightProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} name="Вес (кг)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Volume Progress */}
      {volumeProgress.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Прогресс объема (кг)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={volumeProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} name="Объем (кг)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* 1RM Progress */}
      {oneRMProgress.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Прогресс 1RM (кг) - {formula}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={oneRMProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={2} name="1RM (кг)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {weightProgress.length === 0 && volumeProgress.length === 0 && oneRMProgress.length === 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-500 text-center py-8">Нет данных за выбранный период</p>
        </div>
      )}
    </div>
  )
}

