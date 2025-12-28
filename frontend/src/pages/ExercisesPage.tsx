import { useState, useEffect } from 'react'
import { exerciseService } from '../services/exercise.service'
import { muscleGroupService } from '../services/muscle-group.service'
import type { Exercise, MuscleGroup } from '../types'

export default function ExercisesPage() {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [muscleGroups, setMuscleGroups] = useState<MuscleGroup[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newExercise, setNewExercise] = useState({
    name: '',
    description: '',
    muscle_group_ids: [] as number[],
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError('')
      const [exercisesData, muscleGroupsData] = await Promise.all([
        exerciseService.getExercises(true),
        muscleGroupService.getMuscleGroups(true),
      ])
      setExercises(exercisesData)
      setMuscleGroups(muscleGroupsData)
    } catch (err: any) {
      console.error('Ошибка загрузки данных:', err)
      const errorMessage = err.response?.data?.detail || err.message || 'Ошибка загрузки упражнений'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateExercise = async () => {
    if (!newExercise.name.trim()) {
      setError('Название упражнения обязательно')
      return
    }

    if (newExercise.muscle_group_ids.length === 0) {
      setError('Выберите хотя бы одну группу мышц')
      return
    }

    try {
      await exerciseService.createExercise({
        name: newExercise.name,
        description: newExercise.description || undefined,
        muscle_group_ids: newExercise.muscle_group_ids,
      })
      setShowCreateModal(false)
      setNewExercise({ name: '', description: '', muscle_group_ids: [] })
      loadData()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания упражнения')
    }
  }

  const handleDeleteExercise = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить это упражнение?')) return
    
    try {
      await exerciseService.deleteExercise(id)
      loadData()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления упражнения')
    }
  }

  const toggleMuscleGroup = (groupId: number) => {
    setNewExercise((prev) => ({
      ...prev,
      muscle_group_ids: prev.muscle_group_ids.includes(groupId)
        ? prev.muscle_group_ids.filter((id) => id !== groupId)
        : [...prev.muscle_group_ids, groupId],
    }))
  }

  const getMuscleGroupNames = (muscleGroupIds: number[]): string => {
    return muscleGroupIds
      .map((id) => muscleGroups.find((mg) => mg.id === id)?.name)
      .filter(Boolean)
      .join(', ')
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Упражнения</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          + Создать упражнение
        </button>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          <p className="font-medium">Ошибка:</p>
          <p>{error}</p>
          <button
            onClick={loadData}
            className="mt-2 text-sm underline hover:no-underline"
          >
            Попробовать снова
          </button>
        </div>
      )}

      {loading ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Загрузка...</p>
        </div>
      ) : exercises.length === 0 ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600 text-center py-8">
            Упражнения не найдены. Создайте первое упражнение!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {exercises.map((exercise) => (
            <div
              key={exercise.id}
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-900">{exercise.name}</h3>
                {!exercise.is_custom && (
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    Системное
                  </span>
                )}
              </div>
              
              {exercise.description && (
                <p className="text-sm text-gray-700 mb-3">{exercise.description}</p>
              )}
              
              {exercise.muscle_group_ids && exercise.muscle_group_ids.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-gray-500 mb-1">Группы мышц:</p>
                  <div className="flex flex-wrap gap-1">
                    {exercise.muscle_group_ids.map((groupId) => {
                      const muscleGroup = muscleGroups.find((mg) => mg.id === groupId)
                      return muscleGroup ? (
                        <span
                          key={groupId}
                          className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800"
                        >
                          {muscleGroup.name}
                        </span>
                      ) : null
                    })}
                  </div>
                </div>
              )}

              {exercise.image_path && (
                <div className="mb-3">
                  <img
                    src={exercise.image_path}
                    alt={exercise.name}
                    className="w-full h-32 object-cover rounded"
                  />
                </div>
              )}

              {exercise.is_custom && (
                <button
                  onClick={() => handleDeleteExercise(exercise.id)}
                  className="mt-2 px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                >
                  Удалить
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Создать упражнение</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Название <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={newExercise.name}
                  onChange={(e) =>
                    setNewExercise({ ...newExercise, name: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Например: Жим штанги лежа"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Описание (необязательно)
                </label>
                <textarea
                  value={newExercise.description}
                  onChange={(e) =>
                    setNewExercise({ ...newExercise, description: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Добавьте описание упражнения..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Группы мышц <span className="text-red-500">*</span>
                </label>
                <div className="border border-gray-300 rounded-md p-3 max-h-48 overflow-y-auto">
                  {muscleGroups.length === 0 ? (
                    <p className="text-sm text-gray-500">Загрузка групп мышц...</p>
                  ) : (
                    <div className="space-y-2">
                      {muscleGroups.map((muscleGroup) => (
                        <label
                          key={muscleGroup.id}
                          className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
                        >
                          <input
                            type="checkbox"
                            checked={newExercise.muscle_group_ids.includes(muscleGroup.id)}
                            onChange={() => toggleMuscleGroup(muscleGroup.id)}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">{muscleGroup.name}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
                {newExercise.muscle_group_ids.length > 0 && (
                  <p className="mt-2 text-xs text-gray-500">
                    Выбрано: {newExercise.muscle_group_ids.length}
                  </p>
                )}
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleCreateExercise}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Создать
              </button>
              <button
                onClick={() => {
                  setShowCreateModal(false)
                  setNewExercise({ name: '', description: '', muscle_group_ids: [] })
                }}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
