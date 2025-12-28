import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { templateService } from '../services/template.service'
import { trainingService } from '../services/training.service'
import { exerciseService } from '../services/exercise.service'
import type { TrainingTemplate, Exercise, ImplementationTemplate, SetTemplate } from '../types'

export default function TemplatesPage() {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<TrainingTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showAddExerciseModal, setShowAddExerciseModal] = useState(false)
  const [exerciseSearchQuery, setExerciseSearchQuery] = useState('')
  const [editingTemplate, setEditingTemplate] = useState<TrainingTemplate | null>(null)
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [newTemplate, setNewTemplate] = useState({
    name: '',
    description: '',
  })

  useEffect(() => {
    loadTemplates()
    loadExercises()
  }, [])

  const loadExercises = async () => {
    try {
      const data = await exerciseService.getExercises(true)
      setExercises(data)
    } catch (err) {
      console.error('Ошибка загрузки упражнений:', err)
    }
  }

  const loadTemplates = async () => {
    try {
      setLoading(true)
      const data = await templateService.getTemplates(true)
      setTemplates(data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки шаблонов')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTemplate = async () => {
    if (!newTemplate.name.trim()) {
      setError('Название шаблона обязательно')
      return
    }

    try {
      await templateService.createTemplate({
        name: newTemplate.name,
        description: newTemplate.description || undefined,
        implementation_templates: [], // Пустой шаблон, можно будет редактировать позже
      })
      setShowCreateModal(false)
      setNewTemplate({ name: '', description: '' })
      loadTemplates()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания шаблона')
    }
  }

  const handleDeleteTemplate = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить этот шаблон?')) return
    
    try {
      await templateService.deleteTemplate(id)
      loadTemplates()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления шаблона')
    }
  }

  const handleStartTraining = async (templateId: number) => {
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

  const handleUpdateTemplate = async () => {
    if (!editingTemplate) return

    try {
      await templateService.updateTemplate(editingTemplate.id, {
        name: editingTemplate.name,
        description: editingTemplate.description,
        implementation_templates: editingTemplate.implementation_templates,
      })
      setShowEditModal(false)
      setEditingTemplate(null)
      loadTemplates()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка обновления шаблона')
    }
  }

  const handleAddExerciseToTemplate = (exerciseId: number) => {
    if (!editingTemplate) return

    const newImpl: ImplementationTemplate = {
      exercise_id: exerciseId,
      order_index: editingTemplate.implementation_templates.length + 1,
      set_templates: [],
    }

    setEditingTemplate({
      ...editingTemplate,
      implementation_templates: [...editingTemplate.implementation_templates, newImpl],
    })
  }

  const handleRemoveExerciseFromTemplate = (index: number) => {
    if (!editingTemplate) return

    const updated = editingTemplate.implementation_templates.filter((_, i) => i !== index)
    const reordered = updated.map((impl, i) => ({
      ...impl,
      order_index: i + 1,
    }))

    setEditingTemplate({
      ...editingTemplate,
      implementation_templates: reordered,
    })
  }

  const handleAddSetToTemplate = (implIndex: number) => {
    if (!editingTemplate) return

    const impl = editingTemplate.implementation_templates[implIndex]
    const newSet: SetTemplate = {
      order_index: impl.set_templates.length + 1,
      weight: undefined,
      reps: undefined,
    }

    const updated = [...editingTemplate.implementation_templates]
    updated[implIndex] = {
      ...impl,
      set_templates: [...impl.set_templates, newSet],
    }

    setEditingTemplate({
      ...editingTemplate,
      implementation_templates: updated,
    })
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Шаблоны тренировок</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          + Создать шаблон
        </button>
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
      ) : templates.length === 0 ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600 text-center py-8">
            У вас пока нет шаблонов. Создайте первый шаблон тренировки!
          </p>
        </div>
      ) : (
        <div className="grid gap-4">
          {templates.map((template) => (
            <div
              key={template.id}
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {template.name}
                    </h3>
                    {!template.user_id && (
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        Системный
                      </span>
                    )}
                  </div>
                  {template.description && (
                    <p className="text-sm text-gray-700 mb-2">{template.description}</p>
                  )}
                  {template.implementation_templates &&
                    template.implementation_templates.length > 0 && (
                      <p className="text-sm text-gray-500 mt-2">
                        Упражнений: {template.implementation_templates.length}
                      </p>
                    )}
                  {(!template.implementation_templates ||
                    template.implementation_templates.length === 0) && (
                    <p className="text-sm text-gray-400 italic mt-2">
                      Шаблон пуст (добавьте упражнения)
                    </p>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleStartTraining(template.id)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Начать тренировку
                  </button>
                  {template.user_id && (
                    <>
                      <button
                        onClick={() => {
                          setEditingTemplate(template)
                          setShowEditModal(true)
                        }}
                        className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
                      >
                        Редактировать
                      </button>
                      <button
                        onClick={() => handleDeleteTemplate(template.id)}
                        className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                      >
                        Удалить
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Создать шаблон</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Название <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={newTemplate.name}
                  onChange={(e) =>
                    setNewTemplate({ ...newTemplate, name: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Например: Тренировка груди"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Описание (необязательно)
                </label>
                <textarea
                  value={newTemplate.description}
                  onChange={(e) =>
                    setNewTemplate({ ...newTemplate, description: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Добавьте описание шаблона..."
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleCreateTemplate}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Создать
              </button>
              <button
                onClick={() => {
                  setShowCreateModal(false)
                  setNewTemplate({ name: '', description: '' })
                }}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Modal */}
      {showEditModal && editingTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Редактировать шаблон</h2>
            
            <div className="space-y-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Название <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={editingTemplate.name}
                  onChange={(e) =>
                    setEditingTemplate({ ...editingTemplate, name: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Описание
                </label>
                <textarea
                  value={editingTemplate.description || ''}
                  onChange={(e) =>
                    setEditingTemplate({ ...editingTemplate, description: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Упражнения
                </label>
                <div className="space-y-2">
                  {editingTemplate.implementation_templates.map((impl, implIndex) => {
                    const exercise = exercises.find((e) => e.id === impl.exercise_id)
                    return (
                      <div key={implIndex} className="border border-gray-300 rounded p-3">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-medium">
                            {exercise?.name || `Упражнение #${impl.exercise_id}`}
                          </span>
                          <button
                            onClick={() => handleRemoveExerciseFromTemplate(implIndex)}
                            className="text-red-600 hover:text-red-800 text-sm"
                          >
                            Удалить
                          </button>
                        </div>
                        <div className="text-sm text-gray-600">
                          Подходов: {impl.set_templates.length}
                        </div>
                      </div>
                    )
                  })}
                  <button
                    onClick={() => setShowAddExerciseModal(true)}
                    className="w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded text-gray-600 hover:border-gray-400"
                  >
                    + Добавить упражнение
                  </button>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleUpdateTemplate}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Сохранить
              </button>
              <button
                onClick={() => {
                  setShowEditModal(false)
                  setEditingTemplate(null)
                }}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Exercise to Template Modal */}
      {showAddExerciseModal && editingTemplate && (
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
                      handleAddExerciseToTemplate(exercise.id)
                      setShowAddExerciseModal(false)
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
    </div>
  )
}
