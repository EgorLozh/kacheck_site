import api from './api'
import type { User, Training } from '../types'

export interface Follow {
  id: number
  follower_id: number
  following_id: number
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
  follower_username?: string
  following_username?: string
}

export interface UserWithFollowInfo {
  id: number
  username: string
  isFollowing?: boolean
}

export interface Reaction {
  id: number
  training_id: number
  user_id: number
  reaction_type: 'LIKE' | 'LOVE' | 'FIRE' | 'MUSCLE' | 'TARGET'
  created_at: string
}

export interface Comment {
  id: number
  training_id: number
  user_id: number
  username?: string
  text: string
  created_at: string
  updated_at: string
}

export const socialService = {
  async followUser(userId: number): Promise<Follow> {
    const response = await api.post<Follow>(`/social/follow/${userId}`)
    return response.data
  },

  async unfollowUser(userId: number): Promise<void> {
    await api.delete(`/social/follow/${userId}`)
  },

  async getFollowers(): Promise<Follow[]> {
    const response = await api.get<Follow[]>('/social/followers')
    return response.data
  },

  async getFollowing(): Promise<Follow[]> {
    const response = await api.get<Follow[]>('/social/following')
    return response.data
  },

  async searchUsers(query: string, limit: number = 20): Promise<User[]> {
    const response = await api.get<User[]>('/social/users/search', {
      params: { q: query, limit },
    })
    return response.data
  },

  async addReaction(trainingId: number, reactionType: string): Promise<Reaction> {
    const response = await api.post<Reaction>(`/social/trainings/${trainingId}/reactions`, {
      reaction_type: reactionType,
    })
    return response.data
  },

  async removeReaction(trainingId: number): Promise<void> {
    await api.delete(`/social/trainings/${trainingId}/reactions`)
  },

  async getTrainingReactions(trainingId: number): Promise<Reaction[]> {
    const response = await api.get<Reaction[]>(`/social/trainings/${trainingId}/reactions`)
    return response.data
  },

  async addComment(trainingId: number, text: string): Promise<Comment> {
    const response = await api.post<Comment>(`/social/trainings/${trainingId}/comments`, {
      text,
    })
    return response.data
  },

  async deleteComment(trainingId: number, commentId: number): Promise<void> {
    await api.delete(`/social/trainings/${trainingId}/comments/${commentId}`)
  },

  async getTrainingComments(trainingId: number): Promise<Comment[]> {
    const response = await api.get<Comment[]>(`/social/trainings/${trainingId}/comments`)
    return response.data
  },

  async approveFollowRequest(userId: number): Promise<Follow> {
    const response = await api.post<Follow>(`/social/follow/${userId}/approve`)
    return response.data
  },

  async rejectFollowRequest(userId: number): Promise<Follow> {
    const response = await api.post<Follow>(`/social/follow/${userId}/reject`)
    return response.data
  },

  async getUserProfile(userId: number): Promise<User> {
    const response = await api.get<User>(`/social/users/${userId}/profile`)
    return response.data
  },

  async getUserTrainings(userId: number, startDate?: string, endDate?: string): Promise<Training[]> {
    const params: any = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    const response = await api.get<Training[]>(`/social/users/${userId}/trainings`, { params })
    return response.data
  },
}


