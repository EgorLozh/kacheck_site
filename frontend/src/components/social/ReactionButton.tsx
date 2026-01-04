import { useState, useEffect } from 'react'
import { socialService, type Reaction } from '../../services/social.service'
import { useAuth } from '../../contexts/AuthContext'

interface ReactionButtonProps {
  trainingId: number
  reactionType: 'LIKE' | 'LOVE' | 'FIRE' | 'MUSCLE' | 'TARGET'
  onUpdate?: () => void
}

const REACTION_EMOJIS: Record<string, string> = {
  LIKE: '👍',
  LOVE: '❤️',
  FIRE: '🔥',
  MUSCLE: '💪',
  TARGET: '🎯',
}

export default function ReactionButton({ trainingId, reactionType, onUpdate }: ReactionButtonProps) {
  const { user } = useAuth()
  const [reactions, setReactions] = useState<Reaction[]>([])
  const [loading, setLoading] = useState(false)
  const [userReaction, setUserReaction] = useState<Reaction | null>(null)

  useEffect(() => {
    loadReactions()
  }, [trainingId])

  const loadReactions = async () => {
    try {
      const data = await socialService.getTrainingReactions(trainingId)
      setReactions(data)
      if (user) {
        const myReaction = data.find((r) => r.user_id === user.id)
        setUserReaction(myReaction || null)
      }
    } catch (err) {
      console.error('Ошибка загрузки реакций:', err)
    }
  }

  const handleClick = async () => {
    if (!user) return

    try {
      setLoading(true)
      if (userReaction && userReaction.reaction_type === reactionType) {
        // Remove reaction
        await socialService.removeReaction(trainingId)
        setUserReaction(null)
      } else {
        // Add or change reaction
        await socialService.addReaction(trainingId, reactionType)
        const updated = await socialService.getTrainingReactions(trainingId)
        const myReaction = updated.find((r) => r.user_id === user.id)
        setUserReaction(myReaction || null)
      }
      await loadReactions()
      onUpdate?.()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка при добавлении реакции')
    } finally {
      setLoading(false)
    }
  }

  const count = reactions.filter((r) => r.reaction_type === reactionType).length
  const isActive = userReaction?.reaction_type === reactionType

  return (
    <button
      onClick={handleClick}
      disabled={loading || !user}
      className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
        isActive
          ? 'bg-blue-100 text-blue-700 border-2 border-blue-500'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border-2 border-transparent'
      } disabled:opacity-50`}
      title={REACTION_EMOJIS[reactionType]}
    >
      <span className="text-lg mr-1">{REACTION_EMOJIS[reactionType]}</span>
      {count > 0 && <span className="text-xs">{count}</span>}
    </button>
  )
}


