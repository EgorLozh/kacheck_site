import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { trainingService } from '../services/training.service'
import { exerciseService } from '../services/exercise.service'
import type { Training, Exercise, Implementation, Set } from '../types'
import ExerciseCard from '../components/training/ExerciseCard'
import { SetData } from '../components/training/SetInput'

export default function ActiveTrainingPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [training, setTraining] = useState<Training | null>(null)
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [isSaving, setIsSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const [showAddExerciseModal, setShowAddExerciseModal] = useState(false)
  const [showChangeExerciseModal, setShowChangeExerciseModal] = useState(false)
  const [changingExerciseIndex, setChangingExerciseIndex] = useState<number | null>(null)
  const [startTime] = useState(new Date())
  const savingTrainingRef = useRef<Training | null>(null)
  const [previousResults, setPreviousResults] = useState<Record<number, Set[]>>({})
  const [exerciseSearchQuery, setExerciseSearchQuery] = useState('')
  const [changeExerciseSearchQuery, setChangeExerciseSearchQuery] = useState('')

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
      // Load previous results for all exercises
      await loadPreviousResults(data.implementations)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки тренировки')
    } finally {
      setLoading(false)
    }
  }

  const loadPreviousResults = async (implementations: Implementation[]) => {
    const results: Record<number, Set[]> = {}
    for (const impl of implementations) {
      try {
        const lastImpl = await trainingService.getLastExerciseImplementation(impl.exercise_id)
        if (lastImpl) {
          results[impl.exercise_id] = lastImpl.sets
        }
      } catch (err) {
        console.error(`Ошибка загрузки предыдущих результатов для упражнения ${impl.exercise_id}:`, err)
      }
    }
    setPreviousResults(results)
  }

  const loadExercises = async () => {
    try {
      const data = await exerciseService.getExercises(true)
      setExercises(data)
    } catch (err) {
      console.error('Ошибка загрузки упражнений:', err)
    }
  }

  // Автосохранение с debounce
  const saveTraining = useCallback(
    async (updatedTraining: Training) => {
      if (!id) return

      // Store what we're saving to compare later
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
          status: 'in_progress',
        })
        
        // Only update training state if current state matches what we saved
        // This prevents overwriting user's new changes with stale saved data
        setTraining((current) => {
          if (!current) return saved
          
          // Check if current state matches what we were saving
          if (savingTrainingRef.current) {
            const savedImplCount = savingTrainingRef.current.implementations.length
            const currentImplCount = current.implementations.length
            const savedResponseCount = saved.implementations.length
            
            // Only update if:
            // 1. Current state has same number of implementations as what we saved
            // 2. Saved response has same number as what we saved
            // This means no changes were made while we were saving
            if (currentImplCount === savedImplCount && 
                savedResponseCount === savedImplCount &&
                currentImplCount > 0) {
              // Additional check: compare exercise_ids and order_index to ensure they match exactly
              const currentImpls = current.implementations
                .map(impl => ({ exercise_id: impl.exercise_id, order_index: impl.order_index }))
                .sort((a, b) => a.order_index - b.order_index)
              const savedImpls = savingTrainingRef.current.implementations
                .map(impl => ({ exercise_id: impl.exercise_id, order_index: impl.order_index }))
                .sort((a, b) => a.order_index - b.order_index)
              
              const currentStr = JSON.stringify(currentImpls)
              const savedStr = JSON.stringify(savedImpls)
              
              if (currentStr === savedStr) {
                // Current state matches what we saved, safe to update with server response
                return saved
              }
            }
            // Special case: if we saved empty list and current is also empty, update
            if (savedImplCount === 0 && currentImplCount === 0 && savedResponseCount === 0) {
              return saved
            }
          }
          
          // Keep current state if it differs from what we saved
          // This means user made changes while we were saving
          return current
        })
        
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

  // Debounced save
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const debouncedSave = useCallback(
    (updatedTraining: Training) => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current)
      }
      saveTimeoutRef.current = setTimeout(() => {
        saveTraining(updatedTraining)
      }, 2000)
    },
    [saveTraining]
  )

  // Immediate save (for critical operations like delete)
  const immediateSave = useCallback(
    async (updatedTraining: Training) => {
      // Clear any pending debounced saves to prevent race conditions
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current)
        saveTimeoutRef.current = null
      }
      // Save immediately - this will update savingTrainingRef
      await saveTraining(updatedTraining)
      // After immediate save, ensure no pending saves can overwrite
      // by clearing the timeout again (in case something was scheduled)
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current)
        saveTimeoutRef.current = null
      }
    },
    [saveTraining]
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
    debouncedSave(updatedTraining)
    setShowAddExerciseModal(false)
    
    // Load previous results for the new exercise
    try {
      const lastImpl = await trainingService.getLastExerciseImplementation(exerciseId)
      if (lastImpl) {
        setPreviousResults((prev) => ({
          ...prev,
          [exerciseId]: lastImpl.sets,
        }))
      }
    } catch (err) {
      console.error(`Ошибка загрузки предыдущих результатов для упражнения ${exerciseId}:`, err)
    }
  }

  const handleDeleteExercise = async (index: number) => {
    if (!training) return

    if (!confirm('Вы уверены, что хотите удалить это упражнение? Все подходы будут удалены.')) {
      return
    }

    const updatedImplementations = training.implementations.filter((_, i) => i !== index)
    // Пересчитываем order_index
    const reordered = updatedImplementations.map((impl, i) => ({
      ...impl,
      order_index: i + 1,
    }))

    const updatedTraining: Training = {
      ...training,
      implementations: reordered,
    }

    setTraining(updatedTraining)
    // Save immediately for delete operations to avoid race conditions
    await immediateSave(updatedTraining)
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
    debouncedSave(updatedTraining)
    setShowChangeExerciseModal(false)
    setChangingExerciseIndex(null)
    
    // Load previous results for the changed exercise
    try {
      const lastImpl = await trainingService.getLastExerciseImplementation(exerciseId)
      if (lastImpl) {
        setPreviousResults((prev) => ({
          ...prev,
          [exerciseId]: lastImpl.sets,
        }))
      }
    } catch (err) {
      console.error(`Ошибка загрузки предыдущих результатов для упражнения ${exerciseId}:`, err)
    }
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
    debouncedSave(updatedTraining)
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
    debouncedSave(updatedTraining)
  }

  const handleDeleteSet = (implIndex: number, setIndex: number) => {
    if (!training) return

    const updatedImplementations = [...training.implementations]
    const updatedSets = updatedImplementations[implIndex].sets.filter((_, i) => i !== setIndex)
    // Пересчитываем order_index
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
    debouncedSave(updatedTraining)
  }

  const handleFinishTraining = async () => {
    if (!training || !id) return

    if (!confirm('Завершить тренировку? Тренировка будет сохранена как завершенная.')) {
      return
    }

    try {
      const duration = Math.floor((new Date().getTime() - startTime.getTime()) / 1000)
      await trainingService.updateTraining(Number(id), {
        status: 'completed',
        duration,
      })
      navigate('/trainings')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка завершения тренировки')
    }
  }

  const handleManualSave = async () => {
    if (!training) return
    await saveTraining(training)
  }

  const getExerciseById = (exerciseId: number) => {
    return exercises.find((e) => e.id === exerciseId)
  }

  const getElapsedTime = () => {
    const elapsed = Math.floor((new Date().getTime() - startTime.getTime()) / 1000)
    const hours = Math.floor(elapsed / 3600)
    const minutes = Math.floor((elapsed % 3600) / 60)
    const seconds = elapsed % 60
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
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
            <h1 className="text-2xl font-bold text-gray-900">Активная тренировка</h1>
            <p className="text-sm text-gray-600 mt-1">
              Время тренировки: {getElapsedTime()}
            </p>
          </div>
          <div className="flex items-center gap-4">
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
            <button
              onClick={handleManualSave}
              disabled={isSaving}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50"
            >
              Сохранить
            </button>
            <button
              onClick={handleFinishTraining}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Завершить тренировку
            </button>
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
            <p className="text-gray-600 mb-4">Нет упражнений. Добавьте первое упражнение!</p>
            <button
              onClick={() => setShowAddExerciseModal(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              + Добавить упражнение
            </button>
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
                  onUpdateExercise={() => {
                    setChangingExerciseIndex(index)
                    setShowChangeExerciseModal(true)
                  }}
                  onAddSet={(setData) => handleAddSet(index, setData)}
                  onUpdateSet={(setIndex, setData) => handleUpdateSet(index, setIndex, setData)}
                  onDeleteSet={(setIndex) => handleDeleteSet(index, setIndex)}
                  onDeleteExercise={() => handleDeleteExercise(index)}
                  previousSets={previousResults[impl.exercise_id]}
                />
              )
            })}

            {/* Кнопка добавить упражнение */}
            <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8 flex items-center justify-center">
              <button
                onClick={() => setShowAddExerciseModal(true)}
                className="text-gray-600 hover:text-gray-800 text-center"
              >
                <div className="text-4xl mb-2">+</div>
                <div className="text-sm font-medium">Добавить упражнение</div>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Модальное окно добавления упражнения */}
      {showAddExerciseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Выберите упражнение</h2>
            <input
              type="text"
              value={exerciseSearchQuery}
              onChange={(e) => setExerciseSearchQuery(e.target.value)}
              placeholder="Поиск упражнения..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="max-h-96 overflow-y-auto space-y-2">
              {exercises
                .filter((exercise) =>
                  exercise.name.toLowerCase().includes(exerciseSearchQuery.toLowerCase())
                )
                .map((exercise) => (
                  <button
                    key={exercise.id}
                    onClick={() => {
                      handleAddExercise(exercise.id)
                      setExerciseSearchQuery('')
                    }}
                    className="w-full text-left px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                  >
                    {exercise.name}
                  </button>
                ))}
            </div>
            <button
              onClick={() => {
                setShowAddExerciseModal(false)
                setExerciseSearchQuery('')
              }}
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
            <input
              type="text"
              value={changeExerciseSearchQuery}
              onChange={(e) => setChangeExerciseSearchQuery(e.target.value)}
              placeholder="Поиск упражнения..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="max-h-96 overflow-y-auto space-y-2">
              {exercises
                .filter((exercise) =>
                  exercise.name.toLowerCase().includes(changeExerciseSearchQuery.toLowerCase())
                )
                .map((exercise) => (
                  <button
                    key={exercise.id}
                    onClick={() => {
                      handleChangeExercise(exercise.id)
                      setChangeExerciseSearchQuery('')
                    }}
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
                setChangeExerciseSearchQuery('')
              }}
              className="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Отмена
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

