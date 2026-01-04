import UserCard from './UserCard'

export interface UserListItem {
  id: number
  username: string
  isFollowing?: boolean
}

interface UsersListProps {
  users: UserListItem[]
  onFollowToggle?: (userId: number, isFollowing: boolean) => void
  emptyMessage?: string
}

export default function UsersList({ users, onFollowToggle, emptyMessage = 'Нет пользователей' }: UsersListProps) {
  if (users.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {users.map((user) => (
        <UserCard
          key={user.id}
          userId={user.id}
          username={user.username}
          isFollowing={user.isFollowing}
          onFollowToggle={onFollowToggle}
        />
      ))}
    </div>
  )
}

