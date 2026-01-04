import { useState, useEffect } from 'react'
import { socialService } from '../../services/social.service'

interface FollowButtonProps {
  userId: number
  isFollowing: boolean
  onToggle?: (isFollowing: boolean) => void
  className?: string
}

export default function FollowButton({ userId, isFollowing: initialIsFollowing, onToggle, className }: FollowButtonProps) {
  const [isFollowing, setIsFollowing] = useState(initialIsFollowing)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsFollowing(initialIsFollowing)
  }, [initialIsFollowing])

  const handleToggle = async () => {
    setIsLoading(true)
    try {
      if (isFollowing) {
        await socialService.unfollowUser(userId)
        setIsFollowing(false)
        onToggle?.(false)
      } else {
        await socialService.followUser(userId)
        setIsFollowing(true)
        onToggle?.(true)
      }
    } catch (error) {
      console.error('Ошибка при изменении подписки:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleToggle}
      disabled={isLoading}
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
        isFollowing
          ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          : 'bg-blue-600 text-white hover:bg-blue-700'
      } disabled:opacity-50 disabled:cursor-not-allowed ${className || ''}`}
    >
      {isLoading ? 'Загрузка...' : isFollowing ? 'Отписаться' : 'Подписаться'}
    </button>
  )
}

