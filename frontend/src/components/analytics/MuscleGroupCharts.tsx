import { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsService } from '../../services/analytics.service'

interface MuscleGroupChartsProps {
  dateRange: { start: string; end: string }
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']

export default function MuscleGroupCharts({ dateRange }: MuscleGroupChartsProps) {
  const [volumeData, setVolumeData] = useState<Array<{ name: string; value: number }>>([])
  const [frequencyData, setFrequencyData] = useState<Array<{ name: string; value: number }>>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [dateRange])

  const loadData = async () => {
    try {
      setLoading(true)

      // Load volume data
      const volumeResponse = await analyticsService.getMuscleGroupVolume(dateRange.start, dateRange.end)
      const volumeChart = volumeResponse.volume_by_group.map((item) => ({
        name: item.muscle_group_name,
        value: Math.round(item.volume),
      }))
      setVolumeData(volumeChart)

      // Load frequency data
      const frequencyResponse = await analyticsService.getMuscleGroupFrequency(dateRange.start, dateRange.end)
      const frequencyChart = frequencyResponse.frequency_by_group.map((item) => ({
        name: item.muscle_group_name,
        value: item.frequency,
      }))
      setFrequencyData(frequencyChart)
    } catch (err) {
      console.error('Ошибка загрузки данных по группам мышц:', err)
    } finally {
      setLoading(false)
    }
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
      {/* Volume Distribution */}
      {volumeData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Распределение объема по группам мышц (кг)</h3>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={volumeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {volumeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => `${value} кг`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Frequency Distribution */}
      {frequencyData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Частота тренировок по группам мышц</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={frequencyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#3b82f6" name="Количество тренировок" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {volumeData.length === 0 && frequencyData.length === 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-500 text-center py-8">Нет данных за выбранный период</p>
        </div>
      )}
    </div>
  )
}

