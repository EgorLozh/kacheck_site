import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { trainingService } from '../services/training.service'
import { templateService } from '../services/template.service'
import type { Training, TrainingTemplate } from '../types'
import { formatTrainingName } from '../utils/dateFormatter'

export default function TrainingsPage() {
  const navigate = useNavigate()
  const [trainings, setTrainings] = useState<Training[]>([])
  const [templates, setTemplates] = useState<TrainingTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [showTemplateModal, setShowTemplateModal] = useState(false)

  useEffect(() => {
    loadTrainings()
    loadTemplates()
  }, [])

  const loadTrainings = async () => {
    try {
      setLoading(true)
      const data = await trainingService.getTrainings()
      setTrainings(data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки тренировок')
    } finally {
      setLoading(false)
    }
  }

  const loadTemplates = async () => {
    try {
      const data = await templateService.getTemplates(true)
      setTemplates(data)
    } catch (err) {
      console.error('Ошибка загрузки шаблонов:', err)
    }
  }

  const handleStartNewTraining = async () => {
    try {
      setError('')
      const newTraining = await trainingService.createTraining({
        date_time: new Date().toISOString(),
        status: 'in_progress',
      })
      navigate(`/trainings/active/${newTraining.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания тренировки')
    }
  }

  const handleStartFromTemplate = async (templateId: number) => {
    try {
      setError('')
      const newTraining = await trainingService.createTrainingFromTemplate(
        templateId,
        new Date().toISOString()
      )
      // Обновляем статус на in_progress
      await trainingService.updateTraining(newTraining.id, {
        status: 'in_progress',
      })
      navigate(`/trainings/active/${newTraining.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания тренировки из шаблона')
    }
  }

  const handleContinueTraining = (trainingId: number) => {
    navigate(`/trainings/active/${trainingId}`)
  }

  const handleDeleteTraining = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту тренировку?')) return
    
    try {
      await trainingService.deleteTraining(id)
      loadTrainings()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления тренировки')
    }
  }

  const handleCreateTemplateFromTraining = async (training: Training) => {
    if (!confirm('Создать шаблон из этой тренировки?')) return

    try {
      // Convert training implementations to template implementations
      const implementation_templates = training.implementations.map((impl) => ({
        exercise_id: impl.exercise_id,
        order_index: impl.order_index,
        set_templates: impl.sets.map((set) => ({
          order_index: set.order_index,
          weight: set.weight,
          reps: set.reps,
        })),
      }))

      await templateService.createTemplate({
        name: `Тренировка от ${formatDate(training.date_time)}`,
        description: `Создано из тренировки #${training.id}`,
        implementation_templates,
      })

      alert('Шаблон успешно создан!')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания шаблона')
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800'
      case 'skipped':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Завершена'
      case 'in_progress':
        return 'В процессе'
      case 'skipped':
        return 'Пропущена'
      default:
        return 'Запланирована'
    }
  }

  const activeTrainings = trainings.filter((t) => t.status === 'in_progress')
  const completedTrainings = trainings.filter((t) => t.status === 'completed')
  const otherTrainings = trainings.filter(
    (t) => t.status !== 'in_progress' && t.status !== 'completed'
  )

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Тренировки</h1>
        <div className="flex gap-3">
          <button
            onClick={() => setShowTemplateModal(true)}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-colors"
          >
            Из шаблона
          </button>
          <button
            onClick={handleStartNewTraining}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            + Начать новую тренировку
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {loading ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Загрузка...</p>
        </div>
      ) : (
        <>
          {/* Активные тренировки */}
          {activeTrainings.length > 0 && (
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Активные тренировки</h2>
              <div className="grid gap-4">
                {activeTrainings.map((training) => (
                  <div
                    key={training.id}
                    className="bg-yellow-50 border-2 border-yellow-300 p-6 rounded-lg shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatTrainingName(training.date_time)}
                          </h3>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                              training.status
                            )}`}
                          >
                            {getStatusText(training.status)}
                          </span>
                        </div>
                        {training.implementations && training.implementations.length > 0 && (
                          <p className="text-sm text-gray-500">
                            Упражнений: {training.implementations.length}
                          </p>
                        )}
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleContinueTraining(training.id)}
                          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                          Продолжить
                        </button>
                        <button
                          onClick={() => handleDeleteTraining(training.id)}
                          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                        >
                          Удалить
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Завершенные тренировки */}
          {completedTrainings.length > 0 && (
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Завершенные тренировки</h2>
              <div className="grid gap-4">
                {completedTrainings.map((training) => (
                  <div
                    key={training.id}
                    className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatTrainingName(training.date_time)}
                          </h3>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                              training.status
                            )}`}
                          >
                            {getStatusText(training.status)}
                          </span>
                        </div>
                        {training.duration && (
                          <p className="text-sm text-gray-500">
                            Длительность: {Math.floor(training.duration / 60)} мин
                          </p>
                        )}
                        {training.implementations && training.implementations.length > 0 && (
                          <p className="text-sm text-gray-500 mt-1">
                            Упражнений: {training.implementations.length}
                          </p>
                        )}
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => navigate(`/trainings/completed/${training.id}`)}
                          className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
                        >
                          Просмотреть
                        </button>
                        <button
                          onClick={() => handleCreateTemplateFromTraining(training)}
                          className="px-3 py-1 text-sm text-purple-600 hover:text-purple-800 hover:bg-purple-50 rounded transition-colors"
                        >
                          Создать шаблон
                        </button>
                        <button
                          onClick={() => handleDeleteTraining(training.id)}
                          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                        >
                          Удалить
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Другие тренировки */}
          {otherTrainings.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Другие тренировки</h2>
              <div className="grid gap-4">
                {otherTrainings.map((training) => (
                  <div
                    key={training.id}
                    className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatTrainingName(training.date_time)}
                          </h3>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                              training.status
                            )}`}
                          >
                            {getStatusText(training.status)}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDeleteTraining(training.id)}
                        className="ml-4 px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                      >
                        Удалить
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {trainings.length === 0 && (
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-600 text-center py-8">
                У вас пока нет тренировок. Начните первую тренировку!
              </p>
            </div>
          )}
        </>
      )}

      {/* Модальное окно выбора шаблона */}
      {showTemplateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Выберите шаблон</h2>
            
            {templates.length === 0 ? (
              <p className="text-gray-600 mb-4">Нет доступных шаблонов</p>
            ) : (
              <div className="space-y-2 mb-4">
                {templates.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => {
                      handleStartFromTemplate(template.id)
                      setShowTemplateModal(false)
                    }}
                    className="w-full text-left px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="font-medium text-gray-900">{template.name}</div>
                    {template.description && (
                      <div className="text-sm text-gray-600 mt-1">{template.description}</div>
                    )}
                    {template.implementation_templates &&
                      template.implementation_templates.length > 0 && (
                        <div className="text-xs text-gray-500 mt-1">
                          Упражнений: {template.implementation_templates.length}
                        </div>
                      )}
                  </button>
                ))}
              </div>
            )}

            <button
              onClick={() => setShowTemplateModal(false)}
              className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Отмена
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
