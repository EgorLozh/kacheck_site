import api from './api'

export interface UserProfile {
  id: number
  email: string
  username: string
  weight?: number
  height?: number
}

export interface BodyMetric {
  id: number
  user_id: number
  weight?: number
  height?: number
  date: string
}

export interface CreateBodyMetricRequest {
  weight?: number
  height?: number
  date?: string
}

export interface UpdateUserProfileRequest {
  weight?: number
  height?: number
}

export const userProfileService = {
  async getProfile(): Promise<UserProfile> {
    const response = await api.get<UserProfile>('/user/profile')
    return response.data
  },

  async updateProfile(data: UpdateUserProfileRequest): Promise<UserProfile> {
    const response = await api.put<UserProfile>('/user/profile', data)
    return response.data
  },

  async getBodyMetrics(startDate?: string, endDate?: string): Promise<BodyMetric[]> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<BodyMetric[]>('/user/profile/body-metrics', { params })
    return response.data
  },

  async createBodyMetric(data: CreateBodyMetricRequest): Promise<BodyMetric> {
    const response = await api.post<BodyMetric>('/user/profile/body-metrics', data)
    return response.data
  },
}


