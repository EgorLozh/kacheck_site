import { useState } from 'react'
import { userProfileService } from '../services/user-profile.service'

interface WeightHeightInputProps {
  onSuccess?: () => void
  onCancel?: () => void
}

export default function WeightHeightInput({ onSuccess, onCancel }: WeightHeightInputProps) {
  const [weight, setWeight] = useState<string>('')
  const [height, setHeight] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!weight && !height) {
      setError('Укажите хотя бы вес или рост')
      return
    }

    try {
      setLoading(true)
      await userProfileService.createBodyMetric({
        weight: weight ? parseFloat(weight) : undefined,
        height: height ? parseFloat(height) : undefined,
      })
      
      setWeight('')
      setHeight('')
      onSuccess?.()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при сохранении данных')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Добавить измерение</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="weight" className="block text-sm font-medium text-gray-700 mb-1">
                Вес (кг)
              </label>
              <input
                type="number"
                id="weight"
                step="0.1"
                min="0"
                max="500"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Введите вес"
              />
            </div>

            <div>
              <label htmlFor="height" className="block text-sm font-medium text-gray-700 mb-1">
                Рост (см)
              </label>
              <input
                type="number"
                id="height"
                step="0.1"
                min="0"
                max="300"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Введите рост"
              />
            </div>

            {error && (
              <div className="text-red-600 text-sm">{error}</div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Сохранение...' : 'Сохранить'}
              </button>
              {onCancel && (
                <button
                  type="button"
                  onClick={onCancel}
                  className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-300"
                >
                  Отмена
                </button>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}


