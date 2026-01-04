import { useState, useEffect } from 'react'
import { socialService, type Comment } from '../../services/social.service'
import { useAuth } from '../../contexts/AuthContext'
import CommentItem from './CommentItem'

interface CommentSectionProps {
  trainingId: number
}

export default function CommentSection({ trainingId }: CommentSectionProps) {
  const { user } = useAuth()
  const [comments, setComments] = useState<Comment[]>([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadComments()
  }, [trainingId])

  const loadComments = async () => {
    try {
      setLoading(true)
      const data = await socialService.getTrainingComments(trainingId)
      setComments(data)
    } catch (err) {
      console.error('Ошибка загрузки комментариев:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComment.trim() || !user) return

    try {
      setSubmitting(true)
      await socialService.addComment(trainingId, newComment.trim())
      setNewComment('')
      await loadComments()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка при добавлении комментария')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (commentId: number) => {
    if (!confirm('Удалить комментарий?')) return

    try {
      await socialService.deleteComment(trainingId, commentId)
      await loadComments()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка при удалении комментария')
    }
  }

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Комментарии ({comments.length})</h3>

      {/* Add comment form */}
      {user && (
        <form onSubmit={handleSubmit} className="mb-4">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Написать комментарий..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2"
            rows={3}
          />
          <button
            type="submit"
            disabled={submitting || !newComment.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {submitting ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
      )}

      {/* Comments list */}
      {loading ? (
        <p className="text-gray-600">Загрузка комментариев...</p>
      ) : comments.length === 0 ? (
        <p className="text-gray-500">Пока нет комментариев</p>
      ) : (
        <div className="space-y-4">
          {comments.map((comment) => (
            <CommentItem
              key={comment.id}
              comment={comment}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}


