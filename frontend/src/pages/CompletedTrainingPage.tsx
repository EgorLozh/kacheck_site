import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { trainingService } from '../services/training.service'
import { exerciseService } from '../services/exercise.service'
import type { Training, Exercise, Implementation, Set } from '../types'
import ExerciseCard from '../components/training/ExerciseCard'
import { SetData } from '../components/training/SetInput'
import { formatTrainingName } from '../utils/dateFormatter'
import ShareButton from '../components/training/ShareButton'
import ReactionList from '../components/social/ReactionList'
import CommentSection from '../components/social/CommentSection'

export default function CompletedTrainingPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [training, setTraining] = useState<Training | null>(null)
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [isSaving, setIsSaving] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const [showAddExerciseModal, setShowAddExerciseModal] = useState(false)
  const [showChangeExerciseModal, setShowChangeExerciseModal] = useState(false)
  const [changingExerciseIndex, setChangingExerciseIndex] = useState<number | null>(null)
  const savingTrainingRef = useRef<Training | null>(null)

  useEffect(() => {
    if (id) {
      loadTraining()
      loadExercises()
    }
  }, [id])

  const loadTraining = async () => {
    try {
      setLoading(true)
      const data = await trainingService.getTrainingById(Number(id))
      setTraining(data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки тренировки')
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

  const saveTraining = useCallback(
    async (updatedTraining: Training) => {
      if (!id) return

      savingTrainingRef.current = updatedTraining
      setIsSaving(true)
      try {
        const implementations = updatedTraining.implementations.map((impl) => ({
          exercise_id: impl.exercise_id,
          order_index: impl.order_index,
          sets: impl.sets.map((set) => ({
            order_index: set.order_index,
            weight: set.weight,
            reps: set.reps,
            rest_time: set.rest_time,
            duration: set.duration,
            rpe: set.rpe,
          })),
        }))

        const saved = await trainingService.updateTraining(Number(id), {
          implementations,
          status: 'completed',
        })

        setTraining(saved)
        savingTrainingRef.current = null
        setLastSaved(new Date())
        setError('')
      } catch (err: any) {
        savingTrainingRef.current = null
        setError(err.response?.data?.detail || 'Ошибка сохранения')
      } finally {
        setIsSaving(false)
      }
    },
    [id]
  )

  const handleAddExercise = async (exerciseId: number) => {
    if (!training) return

    const newImplementation: Implementation = {
      exercise_id: exerciseId,
      order_index: training.implementations.length + 1,
      sets: [],
    }

    const updatedTraining: Training = {
      ...training,
      implementations: [...training.implementations, newImplementation],
    }

    setTraining(updatedTraining)
    await saveTraining(updatedTraining)
    setShowAddExerciseModal(false)
  }

  const handleDeleteExercise = async (index: number) => {
    if (!training) return

    if (!confirm('Вы уверены, что хотите удалить это упражнение? Все подходы будут удалены.')) {
      return
    }

    const updatedImplementations = training.implementations.filter((_, i) => i !== index)
    const reordered = updatedImplementations.map((impl, i) => ({
      ...impl,
      order_index: i + 1,
    }))

    const updatedTraining: Training = {
      ...training,
      implementations: reordered,
    }

    setTraining(updatedTraining)
    await saveTraining(updatedTraining)
  }

  const handleChangeExercise = async (exerciseId: number) => {
    if (!training || changingExerciseIndex === null) return

    const updatedImplementations = [...training.implementations]
    updatedImplementations[changingExerciseIndex] = {
      ...updatedImplementations[changingExerciseIndex],
      exercise_id: exerciseId,
    }

    const updatedTraining: Training = {
      ...training,
      implementations: updatedImplementations,
    }

    setTraining(updatedTraining)
    await saveTraining(updatedTraining)
    setShowChangeExerciseModal(false)
    setChangingExerciseIndex(null)
  }

  const handleAddSet = (implIndex: number, setData: SetData) => {
    if (!training) return

    const updatedImplementations = [...training.implementations]
    const newSet: Set = {
      order_index: updatedImplementations[implIndex].sets.length + 1,
      weight: setData.weight,
      reps: setData.reps,
      rest_time: setData.rest_time,
      rpe: setData.rpe,
    }

    updatedImplementations[implIndex] = {
      ...updatedImplementations[implIndex],
      sets: [...updatedImplementations[implIndex].sets, newSet],
    }

    const updatedTraining: Training = {
      ...training,
      implementations: updatedImplementations,
    }

    setTraining(updatedTraining)
    saveTraining(updatedTraining)
  }

  const handleUpdateSet = (implIndex: number, setIndex: number, setData: SetData) => {
    if (!training) return

    const updatedImplementations = [...training.implementations]
    const updatedSets = [...updatedImplementations[implIndex].sets]
    updatedSets[setIndex] = {
      ...updatedSets[setIndex],
      weight: setData.weight,
      reps: setData.reps,
      rest_time: setData.rest_time,
      rpe: setData.rpe,
    }

    updatedImplementations[implIndex] = {
      ...updatedImplementations[implIndex],
      sets: updatedSets,
    }

    const updatedTraining: Training = {
      ...training,
      implementations: updatedImplementations,
    }

    setTraining(updatedTraining)
    saveTraining(updatedTraining)
  }

  const handleDeleteSet = (implIndex: number, setIndex: number) => {
    if (!training) return

    const updatedImplementations = [...training.implementations]
    const updatedSets = updatedImplementations[implIndex].sets.filter((_, i) => i !== setIndex)
    const reorderedSets = updatedSets.map((set, i) => ({
      ...set,
      order_index: i + 1,
    }))

    updatedImplementations[implIndex] = {
      ...updatedImplementations[implIndex],
      sets: reorderedSets,
    }

    const updatedTraining: Training = {
      ...training,
      implementations: updatedImplementations,
    }

    setTraining(updatedTraining)
    saveTraining(updatedTraining)
  }

  const getExerciseById = (exerciseId: number) => {
    return exercises.find((e) => e.id === exerciseId)
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Загрузка тренировки...</p>
      </div>
    )
  }

  if (!training) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">Тренировка не найдена</p>
          <button
            onClick={() => navigate('/trainings')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Вернуться к тренировкам
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Заголовок */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{formatTrainingName(training.date_time)}</h1>
            {training.duration && (
              <p className="text-sm text-gray-500 mt-1">
                Длительность: {Math.floor(training.duration / 60)} мин
              </p>
            )}
          </div>
          <div className="flex items-center gap-4">
            {isEditing && (
              <div className="text-sm text-gray-600">
                {isSaving ? (
                  <span className="text-blue-600">Сохранение...</span>
                ) : lastSaved ? (
                  <span className="text-green-600">
                    Сохранено {lastSaved.toLocaleTimeString()}
                  </span>
                ) : (
                  <span>Не сохранено</span>
                )}
              </div>
            )}
            {!isEditing && <ShareButton training={training} onUpdate={setTraining} />}
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Редактировать
              </button>
            ) : (
              <button
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Завершить редактирование
              </button>
            )}
            <button
              onClick={() => navigate('/trainings')}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-3">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Основной контент */}
      <div className="p-6">
        {training.implementations.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-600 mb-4">Нет упражнений.</p>
            {isEditing && (
              <button
                onClick={() => setShowAddExerciseModal(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                + Добавить упражнение
              </button>
            )}
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
                  onUpdateExercise={
                    isEditing
                      ? () => {
                          setChangingExerciseIndex(index)
                          setShowChangeExerciseModal(true)
                        }
                      : undefined
                  }
                  onAddSet={isEditing ? (setData) => handleAddSet(index, setData) : undefined}
                  onUpdateSet={
                    isEditing
                      ? (setIndex, setData) => handleUpdateSet(index, setIndex, setData)
                      : undefined
                  }
                  onDeleteSet={isEditing ? (setIndex) => handleDeleteSet(index, setIndex) : undefined}
                  onDeleteExercise={isEditing ? () => handleDeleteExercise(index) : undefined}
                />
              )
            })}

            {/* Кнопка добавить упражнение */}
            {isEditing && (
              <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8 flex items-center justify-center">
                <button
                  onClick={() => setShowAddExerciseModal(true)}
                  className="text-gray-600 hover:text-gray-800 text-center"
                >
                  <div className="text-4xl mb-2">+</div>
                  <div className="text-sm font-medium">Добавить упражнение</div>
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Модальное окно добавления упражнения */}
      {showAddExerciseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Выберите упражнение</h2>
            <div className="max-h-96 overflow-y-auto space-y-2">
              {exercises.map((exercise) => (
                <button
                  key={exercise.id}
                  onClick={() => handleAddExercise(exercise.id)}
                  className="w-full text-left px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                >
                  {exercise.name}
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowAddExerciseModal(false)}
              className="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Отмена
            </button>
          </div>
        </div>
      )}

      {/* Модальное окно изменения упражнения */}
      {showChangeExerciseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Выберите новое упражнение</h2>
            <div className="max-h-96 overflow-y-auto space-y-2">
              {exercises.map((exercise) => (
                <button
                  key={exercise.id}
                  onClick={() => handleChangeExercise(exercise.id)}
                  className="w-full text-left px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                >
                  {exercise.name}
                </button>
              ))}
            </div>
            <button
              onClick={() => {
                setShowChangeExerciseModal(false)
                setChangingExerciseIndex(null)
              }}
              className="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Отмена
            </button>
          </div>
        </div>
      )}

      {/* Reactions and Comments */}
      {!isEditing && (
        <div className="p-6 bg-white rounded-lg shadow mt-6">
          <ReactionList trainingId={training.id} />
          <CommentSection trainingId={training.id} />
        </div>
      )}
    </div>
  )
}


