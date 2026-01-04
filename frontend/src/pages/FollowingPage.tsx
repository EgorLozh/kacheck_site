import { useState, useEffect } from 'react'
import { socialService, Follow } from '../services/social.service'
import UsersList, { UserListItem } from '../components/social/UsersList'

export default function FollowingPage() {
  const [users, setUsers] = useState<UserListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    loadFollowing()
  }, [])

  const loadFollowing = async () => {
    try {
      setLoading(true)
      setError('')
      const follows: Follow[] = await socialService.getFollowing()
      
      // Convert Follow objects to UserListItem
      const userList: UserListItem[] = follows.map((follow) => ({
        id: follow.following_id,
        username: follow.following_username || `User #${follow.following_id}`,
        isFollowing: true, // Все пользователи в этом списке - это те, на кого мы подписаны
      }))
      
      setUsers(userList)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки подписок')
      console.error('Ошибка загрузки подписок:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFollowToggle = async (userId: number, isFollowing: boolean) => {
    // Update local state optimistically
    setUsers((prevUsers) =>
      isFollowing
        ? prevUsers // If following, keep in list
        : prevUsers.filter((u) => u.id !== userId) // If unfollowed, remove from list
    )
    
    // Reload to ensure consistency
    await loadFollowing()
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600">Загрузка подписок...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Подписки</h1>
        <p className="text-gray-500 mt-1">
          {users.length} {users.length === 1 ? 'подписка' : users.length < 5 ? 'подписки' : 'подписок'}
        </p>
      </div>
      <UsersList
        users={users}
        onFollowToggle={handleFollowToggle}
        emptyMessage="Вы ни на кого не подписаны"
      />
    </div>
  )
}

