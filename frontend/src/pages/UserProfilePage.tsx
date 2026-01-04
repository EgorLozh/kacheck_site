import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { socialService } from '../services/social.service'
import { trainingService } from '../services/training.service'
import { useAuth } from '../contexts/AuthContext'
import type { User, Training } from '../types'
import { formatTrainingName } from '../utils/dateFormatter'

export default function UserProfilePage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user: currentUser } = useAuth()
  const [profile, setProfile] = useState<User | null>(null)
  const [trainings, setTrainings] = useState<Training[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [followStatus, setFollowStatus] = useState<'none' | 'pending' | 'approved'>('none')

  const userId = id ? parseInt(id) : null

  useEffect(() => {
    if (userId) {
      loadProfile()
      loadTrainings()
      checkFollowStatus()
    }
  }, [userId])

  const loadProfile = async () => {
    if (!userId) return
    
    try {
      setLoading(true)
      setError('')
      const data = await socialService.getUserProfile(userId)
      setProfile(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось загрузить профиль пользователя')
    } finally {
      setLoading(false)
    }
  }

  const loadTrainings = async () => {
    if (!userId) return
    
    try {
      const data = await socialService.getUserTrainings(userId)
      setTrainings(data)
    } catch (err: any) {
      console.error('Ошибка загрузки тренировок:', err)
      // Не показываем ошибку, просто не загружаем тренировки
    }
  }

  const checkFollowStatus = async () => {
    if (!userId || !currentUser) return
    
    try {
      const following = await socialService.getFollowing()
      const follow = following.find(f => f.following_id === userId)
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
    if (!userId) return
    
    try {
      await socialService.followUser(userId)
      setFollowStatus('pending')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось отправить запрос на подписку')
    }
  }

  const handleTrainingClick = (trainingId: number) => {
    navigate(`/trainings/completed/${trainingId}`)
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600">Загрузка профиля...</p>
        </div>
      </div>
    )
  }

  if (error && !profile) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            На главную
          </button>
        </div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="p-6">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600">Профиль не найден</p>
        </div>
      </div>
    )
  }

  const isOwnProfile = currentUser?.id === userId

  return (
    <div className="p-6">
      {/* Профиль */}
      <div className="bg-white rounded-lg shadow mb-6 p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{profile.username}</h1>
            {profile.weight && (
              <p className="text-gray-600 mt-2">Вес: {profile.weight} кг</p>
            )}
            {profile.height && (
              <p className="text-gray-600">Рост: {profile.height} см</p>
            )}
          </div>
          {!isOwnProfile && (
            <div>
              {followStatus === 'none' && (
                <button
                  onClick={handleFollow}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Отправить запрос на подписку
                </button>
              )}
              {followStatus === 'pending' && (
                <div className="px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg">
                  Запрос отправлен
                </div>
              )}
              {followStatus === 'approved' && (
                <div className="px-4 py-2 bg-green-100 text-green-800 rounded-lg">
                  Вы подписаны
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Тренировки */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-yellow-800">{error}</p>
        </div>
      )}

      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Тренировки</h2>
        <p className="text-gray-500 mt-1">
          {trainings.length} {trainings.length === 1 ? 'тренировка' : trainings.length < 5 ? 'тренировки' : 'тренировок'}
        </p>
      </div>

      {trainings.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600">Нет доступных тренировок</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {trainings.map((training) => (
            <div
              key={training.id}
              onClick={() => handleTrainingClick(training.id)}
              className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-md transition-shadow"
            >
              <h3 className="font-semibold text-gray-900 mb-2">
                {formatTrainingName(training.date_time)}
              </h3>
              {training.duration && (
                <p className="text-sm text-gray-600">
                  Длительность: {Math.floor(training.duration / 60)} мин
                </p>
              )}
              <p className="text-sm text-gray-600 mt-1">
                Упражнений: {training.implementations.length}
              </p>
              <p className="text-sm text-gray-500 mt-2 capitalize">
                {training.status === 'in_progress' ? 'В процессе' : 
                 training.status === 'completed' ? 'Завершена' :
                 training.status === 'planned' ? 'Запланирована' : 'Пропущена'}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

