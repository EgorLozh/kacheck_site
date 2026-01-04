import { socialService, type Comment } from '../../services/social.service'
import { useAuth } from '../../contexts/AuthContext'

interface CommentItemProps {
  comment: Comment
  onDelete: (commentId: number) => void
}

export default function CommentItem({ comment, onDelete }: CommentItemProps) {
  const { user } = useAuth()
  const canDelete = user && user.id === comment.user_id

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

  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <div className="flex justify-between items-start mb-2">
        <div>
          <p className="font-semibold text-gray-900">{comment.username || `Пользователь #${comment.user_id}`}</p>
          <p className="text-xs text-gray-500">{formatDate(comment.created_at)}</p>
        </div>
        {canDelete && (
          <button
            onClick={() => onDelete(comment.id)}
            className="text-red-600 hover:text-red-800 text-sm"
          >
            Удалить
          </button>
        )}
      </div>
      <p className="text-gray-700 whitespace-pre-wrap">{comment.text}</p>
    </div>
  )
}


