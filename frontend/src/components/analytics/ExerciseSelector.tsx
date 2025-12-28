import { useState, useEffect, useMemo } from 'react'
import { exerciseService } from '../../services/exercise.service'
import type { Exercise } from '../../types'

interface ExerciseSelectorProps {
  selectedExerciseId: number | null
  onExerciseChange: (exerciseId: number | null) => void
}

export default function ExerciseSelector({ selectedExerciseId, onExerciseChange }: ExerciseSelectorProps) {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    loadExercises()
  }, [])

  const loadExercises = async () => {
    try {
      setLoading(true)
      const data = await exerciseService.getExercises(true)
      setExercises(data)
    } catch (err) {
      console.error('Ошибка загрузки упражнений:', err)
    } finally {
      setLoading(false)
    }
  }

  const filteredExercises = useMemo(() => {
    if (!searchQuery.trim()) {
      return exercises
    }
    const query = searchQuery.toLowerCase()
    return exercises.filter((exercise) => exercise.name.toLowerCase().includes(query))
  }, [exercises, searchQuery])

  if (loading) {
    return <div className="text-gray-500">Загрузка упражнений...</div>
  }

  return (
    <div className="space-y-4">
      <div>
        <label htmlFor="exercise-search" className="block text-sm font-medium text-gray-700 mb-2">
          Поиск упражнения
        </label>
        <input
          id="exercise-search"
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Введите название упражнения..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div>
        <label htmlFor="exercise-select" className="block text-sm font-medium text-gray-700 mb-2">
          Выберите упражнение
        </label>
        <select
          id="exercise-select"
          value={selectedExerciseId || ''}
          onChange={(e) => onExerciseChange(e.target.value ? parseInt(e.target.value) : null)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">-- Выберите упражнение --</option>
          {filteredExercises.map((exercise) => (
            <option key={exercise.id} value={exercise.id}>
              {exercise.name}
            </option>
          ))}
        </select>
        {searchQuery && filteredExercises.length === 0 && (
          <p className="mt-2 text-sm text-gray-500">Упражнения не найдены</p>
        )}
      </div>
    </div>
  )
}

