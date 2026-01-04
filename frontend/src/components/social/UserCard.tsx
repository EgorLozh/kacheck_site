import { useNavigate } from 'react-router-dom'
import FollowButton from './FollowButton'

interface UserCardProps {
  userId: number
  username: string
  isFollowing?: boolean
  onFollowToggle?: (userId: number, isFollowing: boolean) => void
}

export default function UserCard({ userId, username, isFollowing = false, onFollowToggle }: UserCardProps) {
  const navigate = useNavigate()
  
  const handleToggle = (newIsFollowing: boolean) => {
    onFollowToggle?.(userId, newIsFollowing)
  }

  const handleUsernameClick = () => {
    navigate(`/users/${userId}`)
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 flex items-center justify-between hover:shadow-md transition-shadow">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
          <span className="text-blue-600 font-semibold text-lg">
            {username.charAt(0).toUpperCase()}
          </span>
        </div>
        <div>
          <h3 
            className="font-medium text-gray-900 cursor-pointer hover:text-blue-600"
            onClick={handleUsernameClick}
          >
            {username}
          </h3>
        </div>
      </div>
      <FollowButton
        userId={userId}
        isFollowing={isFollowing}
        onToggle={handleToggle}
      />
    </div>
  )
}

