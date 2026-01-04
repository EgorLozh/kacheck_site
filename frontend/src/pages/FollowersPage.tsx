import { useState, useEffect } from 'react'
import { socialService, Follow } from '../services/social.service'
import UsersList, { UserListItem } from '../components/social/UsersList'
import type { User } from '../types'

export default function FollowersPage() {
  const [users, setUsers] = useState<UserListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<UserListItem[]>([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [showSearch, setShowSearch] = useState(false)

  useEffect(() => {
    loadFollowers()
  }, [])

  useEffect(() => {
    if (searchQuery.trim().length >= 2) {
      const timeoutId = setTimeout(() => {
        performSearch(searchQuery)
      }, 300) // Debounce 300ms

      return () => clearTimeout(timeoutId)
    } else {
      setSearchResults([])
    }
  }, [searchQuery])

  const loadFollowers = async () => {
    try {
      setLoading(true)
      setError('')
      const follows: Follow[] = await socialService.getFollowers()
      
      // Convert Follow objects to UserListItem with status
      const userList: FollowerWithStatus[] = follows.map((follow) => ({
        id: follow.follower_id,
        username: follow.follower_username || `User #${follow.follower_id}`,
        isFollowing: follow.status === 'approved',
        status: follow.status,
      }))
      
      setUsers(userList)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки подписчиков')
      console.error('Ошибка загрузки подписчиков:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (userId: number) => {
    try {
      await socialService.approveFollowRequest(userId)
      await loadFollowers() // Reload to update status
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось подтвердить запрос')
    }
  }

  const handleReject = async (userId: number) => {
    try {
      await socialService.rejectFollowRequest(userId)
      await loadFollowers() // Reload to update status
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось отклонить запрос')
    }
  }

  const performSearch = async (query: string) => {
    try {
      setSearchLoading(true)
      const foundUsers: User[] = await socialService.searchUsers(query)
      
      // Get list of following IDs to check if we're already following
      const following: Follow[] = await socialService.getFollowing()
      const followingIds = new Set(following.map(f => f.following_id))
      
      const userList: UserListItem[] = foundUsers.map((user) => ({
        id: user.id,
        username: user.username,
        isFollowing: followingIds.has(user.id),
      }))
      
      setSearchResults(userList)
    } catch (err: any) {
      console.error('Ошибка поиска пользователей:', err)
      setSearchResults([])
    } finally {
      setSearchLoading(false)
    }
  }

  const handleFollowToggle = async (userId: number, isFollowing: boolean) => {
    // Update local state optimistically
    setUsers((prevUsers) =>
      prevUsers.map((u) => (u.id === userId ? { ...u, isFollowing } : u))
    )
    
    // Also update search results if user is in search results
    setSearchResults((prevResults) =>
      prevResults.map((u) => (u.id === userId ? { ...u, isFollowing } : u))
    )
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600">Загрузка подписчиков...</p>
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
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Подписчики</h1>
            <p className="text-gray-500 mt-1">
              {users.length} {users.length === 1 ? 'подписчик' : users.length < 5 ? 'подписчика' : 'подписчиков'}
            </p>
          </div>
          <button
            onClick={() => setShowSearch(!showSearch)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {showSearch ? 'Скрыть поиск' : 'Найти пользователей'}
          </button>
        </div>

        {showSearch && (
          <div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="Поиск пользователей по username..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {searchLoading && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {showSearch && searchQuery.trim().length >= 2 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Результаты поиска</h2>
          {searchLoading ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-600">Поиск...</p>
            </div>
          ) : searchResults.length > 0 ? (
            <UsersList
              users={searchResults}
              onFollowToggle={handleFollowToggle}
              emptyMessage=""
            />
          ) : (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500">Пользователи не найдены</p>
            </div>
          )}
        </div>
      )}

      {(!showSearch || searchQuery.trim().length < 2) && (
        <>
          {/* Запросы на подписку (pending) */}
          {users.filter(u => u.status === 'pending').length > 0 && (
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Запросы на подписку</h2>
              <div className="space-y-4">
                {users
                  .filter(u => u.status === 'pending')
                  .map((user) => (
                    <div key={user.id} className="bg-white rounded-lg shadow p-4 flex items-center justify-between hover:shadow-md transition-shadow">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-lg">
                            {user.username.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h3 
                            className="font-medium text-gray-900 cursor-pointer hover:text-blue-600"
                            onClick={() => window.location.href = `/users/${user.id}`}
                          >
                            {user.username}
                          </h3>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleApprove(user.id)}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                        >
                          Принять
                        </button>
                        <button
                          onClick={() => handleReject(user.id)}
                          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                        >
                          Отклонить
                        </button>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Подтвержденные подписчики (approved) */}
          <div className={users.filter(u => u.status === 'pending').length > 0 ? 'mt-6' : ''}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Подписчики</h2>
            {users.filter(u => u.status === 'approved').length > 0 ? (
              <div className="space-y-4">
                {users
                  .filter(u => u.status === 'approved')
                  .map((user) => (
                    <div key={user.id} className="bg-white rounded-lg shadow p-4 flex items-center justify-between hover:shadow-md transition-shadow">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-lg">
                            {user.username.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h3 
                            className="font-medium text-gray-900 cursor-pointer hover:text-blue-600"
                            onClick={() => window.location.href = `/users/${user.id}`}
                          >
                            {user.username}
                          </h3>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow p-8 text-center">
                <p className="text-gray-500">У вас пока нет подтвержденных подписчиков</p>
              </div>
            )}
          </div>

          {users.length === 0 && (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500">У вас пока нет подписчиков</p>
            </div>
          )}
        </>
      )}
    </div>
  )
}

