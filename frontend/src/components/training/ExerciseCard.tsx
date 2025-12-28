import { useState } from 'react'
import type { Exercise, Set, Implementation } from '../../types'
import RestTimer from './RestTimer'
import SetInput, { SetData } from './SetInput'

interface ExerciseCardProps {
  exercise: Exercise
  implementation: Implementation
  exercises: Exercise[]
  onUpdateExercise: (exerciseId: number) => void
  onAddSet: (setData: SetData) => void
  onUpdateSet: (setIndex: number, setData: SetData) => void
  onDeleteSet: (setIndex: number) => void
  onDeleteExercise: () => void
  restTime?: number
}

export default function ExerciseCard({
  exercise,
  implementation,
  exercises,
  onUpdateExercise,
  onAddSet,
  onUpdateSet,
  onDeleteSet,
  onDeleteExercise,
  restTime,
}: ExerciseCardProps) {
  const [showAddSet, setShowAddSet] = useState(false)
  const [editingSetIndex, setEditingSetIndex] = useState<number | null>(null)

  const handleAddSet = (setData: SetData) => {
    onAddSet(setData)
    setShowAddSet(false)
  }

  const handleUpdateSet = (setIndex: number, setData: SetData) => {
    onUpdateSet(setIndex, setData)
    setEditingSetIndex(null)
  }

  const getLastSetRestTime = () => {
    if (implementation.sets.length === 0) return undefined
    const lastSet = implementation.sets[implementation.sets.length - 1]
    return lastSet.rest_time || restTime
  }

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-4 h-fit">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{exercise.name}</h3>
          <button
            onClick={() => onUpdateExercise(exercise.id)}
            className="text-xs text-blue-600 hover:text-blue-800"
          >
            Изменить упражнение
          </button>
        </div>
        <button
          onClick={onDeleteExercise}
          className="text-red-600 hover:text-red-800 text-sm"
          title="Удалить упражнение"
        >
          ✕
        </button>
      </div>

      {/* Подходы */}
      <div className="space-y-2 mb-3">
        {implementation.sets.map((set, index) => (
          <div key={index}>
            {editingSetIndex === index ? (
              <SetInput
                setIndex={index + 1}
                initialData={{
                  weight: set.weight,
                  reps: set.reps,
                  rest_time: set.rest_time,
                  rpe: set.rpe,
                }}
                onSave={(data) => handleUpdateSet(index, data)}
                onCancel={() => setEditingSetIndex(null)}
              />
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded p-2">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    Подход {set.order_index}
                  </span>
                  <div className="flex gap-1">
                    <button
                      onClick={() => setEditingSetIndex(index)}
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      Изменить
                    </button>
                    <button
                      onClick={() => onDeleteSet(index)}
                      className="text-xs text-red-600 hover:text-red-800"
                    >
                      Удалить
                    </button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-600">Вес: </span>
                    <span className="font-medium">{set.weight} кг</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Повторения: </span>
                    <span className="font-medium">{set.reps}</span>
                  </div>
                  {set.rest_time && (
                    <div>
                      <span className="text-gray-600">Отдых: </span>
                      <span className="font-medium">{set.rest_time} сек</span>
                    </div>
                  )}
                  {set.rpe && (
                    <div>
                      <span className="text-gray-600">RPE: </span>
                      <span className="font-medium">{set.rpe}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {showAddSet && (
          <SetInput
            setIndex={implementation.sets.length + 1}
            onSave={handleAddSet}
            onCancel={() => setShowAddSet(false)}
          />
        )}
      </div>

      {/* Таймер отдыха */}
      {getLastSetRestTime() && (
        <div className="mb-3">
          <RestTimer
            duration={getLastSetRestTime()!}
            autoStart={implementation.sets.length > 0}
          />
        </div>
      )}

      {/* Кнопка добавить подход */}
      {!showAddSet && (
        <button
          onClick={() => setShowAddSet(true)}
          className="w-full px-3 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
        >
          + Добавить подход
        </button>
      )}
    </div>
  )
}

