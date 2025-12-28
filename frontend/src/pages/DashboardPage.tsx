import { useState, useEffect } from 'react'
import { trainingService } from '../services/training.service'
import { userProfileService } from '../services/user-profile.service'
import { analyticsService } from '../services/analytics.service'
import WeightHeightInput from '../components/WeightHeightInput'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { format, subDays } from 'date-fns'
import type { Training } from '../types'

interface ChartData {
  date: string
  value: number
}

export default function DashboardPage() {
  const [stats, setStats] = useState({
    today: 0,
    total: 0,
    totalVolume: 0,
  })
  const [profile, setProfile] = useState<{ weight?: number; height?: number }>({})
  const [trainingFrequency, setTrainingFrequency] = useState<ChartData[]>([])
  const [totalVolume, setTotalVolume] = useState<ChartData[]>([])
  const [weightProgress, setWeightProgress] = useState<ChartData[]>([])
  const [showWeightInput, setShowWeightInput] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
    loadProfile()
    loadCharts()
  }, [])

  const loadStats = async () => {
    try {
      const trainings = await trainingService.getTrainings()
      
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const todayTrainings = trainings.filter((training) => {
        const trainingDate = new Date(training.date_time)
        trainingDate.setHours(0, 0, 0, 0)
        return trainingDate.getTime() === today.getTime()
      })

      let totalVolume = 0
      trainings.forEach((training) => {
        training.implementations?.forEach((impl) => {
          impl.sets?.forEach((set) => {
            totalVolume += set.weight * set.reps
          })
        })
      })

      setStats({
        today: todayTrainings.length,
        total: trainings.length,
        totalVolume: Math.round(totalVolume),
      })
    } catch (err) {
      console.error('Ошибка загрузки статистики:', err)
    }
  }

  const loadProfile = async () => {
    try {
      const userProfile = await userProfileService.getProfile()
      setProfile({
        weight: userProfile.weight,
        height: userProfile.height,
      })
    } catch (err) {
      console.error('Ошибка загрузки профиля:', err)
    }
  }

  const loadCharts = async () => {
    try {
      const endDate = format(new Date(), 'yyyy-MM-dd')
      const startDate = format(subDays(new Date(), 14), 'yyyy-MM-dd')

      const frequencyData = await analyticsService.getTrainingFrequency(startDate, endDate)
      const frequencyChart = Object.entries(frequencyData.frequency).map(([date, count]) => ({
        date: format(new Date(date), 'dd.MM'),
        value: count,
      }))
      setTrainingFrequency(frequencyChart)

      const volumeData = await analyticsService.getTotalVolume(startDate, endDate)
      const volumeChart = Object.entries(volumeData.volume).map(([date, volume]) => ({
        date: format(new Date(date), 'dd.MM'),
        value: Math.round(volume),
      }))
      setTotalVolume(volumeChart)

      // Load weight progress (last 30 days for more history)
      try {
        const weightStartDate = format(subDays(new Date(), 30), 'yyyy-MM-dd')
        const weightData = await analyticsService.getUserWeightProgress(weightStartDate, endDate)
        const weightChart = Object.entries(weightData.progress).map(([date, weight]) => ({
          date: format(new Date(date), 'dd.MM'),
          value: weight,
        }))
        setWeightProgress(weightChart)
      } catch (err) {
        console.error('Ошибка загрузки истории веса:', err)
        setWeightProgress([])
      }
    } catch (err) {
      console.error('Ошибка загрузки графиков:', err)
    } finally {
      setLoading(false)
    }
  }

  const calculateBMI = (weight?: number, height?: number): number | null => {
    if (!weight || !height || height <= 0) return null
    const heightM = height / 100
    return weight / (heightM * heightM)
  }

  const bmi = calculateBMI(profile.weight, profile.height)
  const getBMICategory = (bmi: number): string => {
    if (bmi < 18.5) return 'Недостаточный вес'
    if (bmi < 25) return 'Норма'
    if (bmi < 30) return 'Избыточный вес'
    return 'Ожирение'
  }

  const handleWeightInputSuccess = () => {
    setShowWeightInput(false)
    loadProfile()
    loadCharts()
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Дашборд</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Тренировок сегодня</h2>
          {loading ? (
            <p className="text-3xl font-bold text-blue-600">...</p>
          ) : (
            <p className="text-3xl font-bold text-blue-600">{stats.today}</p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Всего тренировок</h2>
          {loading ? (
            <p className="text-3xl font-bold text-green-600">...</p>
          ) : (
            <p className="text-3xl font-bold text-green-600">{stats.total}</p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Общий объем</h2>
          {loading ? (
            <p className="text-3xl font-bold text-purple-600">...</p>
          ) : (
            <p className="text-3xl font-bold text-purple-600">{stats.totalVolume} кг</p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex justify-between items-start mb-2">
            <h2 className="text-lg font-semibold text-gray-700">Мои данные</h2>
            <button
              onClick={() => setShowWeightInput(true)}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Добавить
            </button>
          </div>
          {profile.weight && (
            <p className="text-sm text-gray-600">Вес: {profile.weight} кг</p>
          )}
          {profile.height && (
            <p className="text-sm text-gray-600">Рост: {profile.height} см</p>
          )}
          {bmi && (
            <>
              <p className="text-2xl font-bold text-indigo-600 mt-2">{bmi.toFixed(1)}</p>
              <p className="text-xs text-gray-500">{getBMICategory(bmi)}</p>
            </>
          )}
          {!profile.weight && !profile.height && (
            <p className="text-sm text-gray-500">Добавьте вес и рост</p>
          )}
          {weightProgress.length > 0 && (
            <a
              href="/analytics"
              className="text-xs text-blue-600 hover:text-blue-800 mt-2 inline-block"
            >
              История изменений →
            </a>
          )}
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Training Frequency Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Частота тренировок (14 дней)</h2>
          {trainingFrequency.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={trainingFrequency}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">Нет данных</p>
          )}
        </div>

        {/* Total Volume Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Общий объем (14 дней)</h2>
          {totalVolume.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={totalVolume}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">Нет данных</p>
          )}
        </div>
      </div>

      {/* Weight Progress Chart */}
      {weightProgress.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800">История изменения веса (30 дней)</h2>
            <a
              href="/analytics"
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Подробнее →
            </a>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weightProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} name="Вес (кг)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {showWeightInput && (
        <WeightHeightInput
          onSuccess={handleWeightInputSuccess}
          onCancel={() => setShowWeightInput(false)}
        />
      )}
    </div>
  )
}
