import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsService } from '../services/analytics.service'
import { format, subDays } from 'date-fns'

interface ChartData {
  date: string
  value: number
}

export default function AnalyticsPage() {
  const [trainingFrequency, setTrainingFrequency] = useState<ChartData[]>([])
  const [totalVolume, setTotalVolume] = useState<ChartData[]>([])
  const [weightProgress, setWeightProgress] = useState<ChartData[]>([])
  const [bmiProgress, setBmiProgress] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)
  const [dateRange, setDateRange] = useState({
    start: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
    end: format(new Date(), 'yyyy-MM-dd'),
  })

  useEffect(() => {
    loadAnalytics()
  }, [dateRange])

  const loadAnalytics = async () => {
    try {
      setLoading(true)

      // Load training frequency
      const frequencyData = await analyticsService.getTrainingFrequency(dateRange.start, dateRange.end)
      const frequencyChart = Object.entries(frequencyData.frequency).map(([date, count]) => ({
        date: format(new Date(date), 'dd.MM'),
        value: count,
      }))
      setTrainingFrequency(frequencyChart)

      // Load total volume
      const volumeData = await analyticsService.getTotalVolume(dateRange.start, dateRange.end)
      const volumeChart = Object.entries(volumeData.volume).map(([date, volume]) => ({
        date: format(new Date(date), 'dd.MM'),
        value: Math.round(volume),
      }))
      setTotalVolume(volumeChart)

      // Load weight progress
      try {
        const weightData = await analyticsService.getUserWeightProgress(dateRange.start, dateRange.end)
        const weightChart = Object.entries(weightData.progress).map(([date, weight]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: weight,
        }))
        setWeightProgress(weightChart)
      } catch (err) {
        console.error('Ошибка загрузки веса:', err)
        setWeightProgress([])
      }

      // Load BMI progress
      try {
        const bmiData = await analyticsService.getUserBMIProgress(dateRange.start, dateRange.end)
        const bmiChart = Object.entries(bmiData.progress).map(([date, bmi]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: bmi,
        }))
        setBmiProgress(bmiChart)
      } catch (err) {
        console.error('Ошибка загрузки ИМТ:', err)
        setBmiProgress([])
      }
    } catch (err) {
      console.error('Ошибка загрузки аналитики:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Аналитика</h1>
        <div className="flex gap-4">
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
            className="px-3 py-2 border border-gray-300 rounded-md"
          />
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
            className="px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Загрузка данных...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Training Frequency Chart */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Частота тренировок</h2>
            {trainingFrequency.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trainingFrequency}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#3b82f6" name="Количество тренировок" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500 text-center py-8">Нет данных за выбранный период</p>
            )}
          </div>

          {/* Total Volume Chart */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Общий объем (кг)</h2>
            {totalVolume.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={totalVolume}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#10b981" name="Объем (кг)" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500 text-center py-8">Нет данных за выбранный период</p>
            )}
          </div>

          {/* Weight Progress Chart */}
          {weightProgress.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Изменение веса (кг)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={weightProgress}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#8b5cf6" name="Вес (кг)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* BMI Progress Chart */}
          {bmiProgress.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Индекс массы тела (ИМТ)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={bmiProgress}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#f59e0b" name="ИМТ" />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 text-sm text-gray-600">
                <p>Норма: 18.5 - 24.9 | Избыточный вес: 25 - 29.9 | Ожирение: ≥ 30</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
