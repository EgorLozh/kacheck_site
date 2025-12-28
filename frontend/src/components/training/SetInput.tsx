import { useState } from 'react'

export interface SetData {
  weight: number
  reps: number
  rest_time?: number
  rpe?: number
}

interface SetInputProps {
  setIndex: number
  initialData?: SetData
  onSave: (data: SetData) => void
  onCancel?: () => void
  previousResult?: { weight: number; reps: number }
  previousSetWeight?: number
}

export default function SetInput({ setIndex, initialData, onSave, onCancel, previousResult, previousSetWeight }: SetInputProps) {
  // Auto-fill weight from previous set if this is a new set (setIndex > 1) and no initial data
  const initialWeight = initialData?.weight || (setIndex > 1 && previousSetWeight !== undefined ? previousSetWeight : 0)
  const [weight, setWeight] = useState(initialWeight)
  const [reps, setReps] = useState(initialData?.reps || 0)
  const [restTime, setRestTime] = useState(initialData?.rest_time || undefined)
  const [rpe, setRpe] = useState(initialData?.rpe || undefined)

  const handleSave = () => {
    if (weight >= 0 && reps > 0) {
      onSave({
        weight,
        reps,
        rest_time: restTime || undefined,
        rpe: rpe || undefined,
      })
    }
  }

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-3 space-y-2">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">Подход {setIndex}</span>
        {previousResult && (
          <span className="text-xs text-gray-400 opacity-50">
            Последний раз: {previousResult.weight} кг × {previousResult.reps}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs text-gray-600 mb-1">Вес (кг)</label>
          <input
            type="number"
            min="0"
            step="0.5"
            value={weight || ''}
            onChange={(e) => setWeight(Number(e.target.value))}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
            placeholder="0"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Повторения</label>
          <input
            type="number"
            min="0"
            value={reps || ''}
            onChange={(e) => setReps(Number(e.target.value))}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
            placeholder="0"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs text-gray-600 mb-1">Отдых (сек)</label>
          <input
            type="number"
            min="0"
            value={restTime || ''}
            onChange={(e) => setRestTime(e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
            placeholder="Опционально"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">RPE</label>
          <input
            type="number"
            min="1"
            max="10"
            value={rpe || ''}
            onChange={(e) => setRpe(e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
            placeholder="1-10"
          />
        </div>
      </div>

      <div className="flex gap-2 pt-2">
        <button
          onClick={handleSave}
          disabled={weight < 0 || reps <= 0}
          className="flex-1 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Сохранить
        </button>
        {onCancel && (
          <button
            onClick={onCancel}
            className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
          >
            Отмена
          </button>
        )}
      </div>
    </div>
  )
}

