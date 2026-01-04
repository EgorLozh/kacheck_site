import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { trainingService } from '../services/training.service'
import { exerciseService } from '../services/exercise.service'
import { socialService } from '../services/social.service'
import { useAuth } from '../contexts/AuthContext'
import type { Training, Exercise } from '../types'
import ExerciseCard from '../components/training/ExerciseCard'
import { formatTrainingName } from '../utils/dateFormatter'

export default function SharedTrainingPage() {
  const { token } = useParams<{ token: string }>()
  const navigate = useNavigate()
  const { user: currentUser, isAuthenticated } = useAuth()
  const [training, setTraining] = useState<Training | null>(null)
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [followStatus, setFollowStatus] = useState<'none' | 'pending' | 'approved'>('none')

  useEffect(() => {
    if (token) {
      loadSharedTraining()
      loadExercises()
    }
  }, [token])

  useEffect(() => {
    if (training && isAuthenticated && currentUser && training.user_id !== currentUser.id) {
      checkFollowStatus()
    }
  }, [training, isAuthenticated, currentUser])

  const loadSharedTraining = async () => {
    try {
      setLoading(true)
      const data = await trainingService.getSharedTraining(token!)
      setTraining(data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Тренировка не найдена или доступ закрыт')
    } finally {
      setLoading(false)
    }
  }

  const loadExercises = async () => {
    try {
      const data = await exerciseService.getExercises(true)
      setExercises(data)
    } catch (err) {
      console.error('Ошибка загрузки упражнений:', err)
    }
  }

  const getExerciseById = (exerciseId: number) => {
    return exercises.find((e) => e.id === exerciseId)
  }

  const checkFollowStatus = async () => {
    if (!training || !currentUser) return
    
    try {
      const following = await socialService.getFollowing()
      const follow = following.find(f => f.following_id === training.user_id)
      if (follow) {
        setFollowStatus(follow.status === 'approved' ? 'approved' : 'pending')
      } else {
        setFollowStatus('none')
      }
    } catch (err) {
      console.error('Ошибка проверки статуса подписки:', err)
    }
  }

  const handleFollow = async () => {
    if (!training || !currentUser) return
    
    try {
      await socialService.followUser(training.user_id)
      setFollowStatus('pending')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось отправить запрос на подписку')
    }
  }

  const handleViewProfile = () => {
    if (training) {
      navigate(`/users/${training.user_id}`)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Загрузка тренировки...</p>
      </div>
    )
  }

  if (error || !training) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Тренировка не найдена'}</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            На главную
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Заголовок */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900">{formatTrainingName(training.date_time)}</h1>
            <p className="text-sm text-gray-500 mt-1">Публичная тренировка</p>
            {training.duration && (
              <p className="text-sm text-gray-500 mt-1">
                Длительность: {Math.floor(training.duration / 60)} мин
              </p>
            )}
            {training.username && (
              <div className="mt-2">
                <span className="text-sm text-gray-600">Автор: </span>
                {isAuthenticated && currentUser && training.user_id !== currentUser.id ? (
                  <button
                    onClick={handleViewProfile}
                    className="text-sm text-blue-600 hover:text-blue-800 underline"
                  >
                    {training.username}
                  </button>
                ) : (
                  <span className="text-sm text-gray-900">{training.username}</span>
                )}
              </div>
            )}
            {isAuthenticated && currentUser && training.user_id !== currentUser.id && followStatus === 'none' && (
              <button
                onClick={handleFollow}
                className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              >
                Отправить запрос на подписку
              </button>
            )}
            {isAuthenticated && currentUser && training.user_id !== currentUser.id && followStatus === 'pending' && (
              <div className="mt-3 px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg text-sm inline-block">
                Запрос отправлен
              </div>
            )}
            {isAuthenticated && currentUser && training.user_id !== currentUser.id && followStatus === 'approved' && (
              <div className="mt-3 px-4 py-2 bg-green-100 text-green-800 rounded-lg text-sm inline-block">
                Вы подписаны
              </div>
            )}
          </div>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 ml-4"
          >
            Закрыть
          </button>
        </div>
      </div>

      {/* Основной контент */}
      <div className="p-6">
        {training.implementations.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-600">Нет упражнений в этой тренировке.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {training.implementations.map((impl, index) => {
              const exercise = getExerciseById(impl.exercise_id)
              if (!exercise) return null

              return (
                <ExerciseCard
                  key={index}
                  exercise={exercise}
                  implementation={impl}
                  exercises={exercises}
                  onUpdateExercise={undefined}
                  onAddSet={undefined}
                  onUpdateSet={undefined}
                  onDeleteSet={undefined}
                  onDeleteExercise={undefined}
                />
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}


