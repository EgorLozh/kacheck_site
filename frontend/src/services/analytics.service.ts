import api from './api'

export interface TrainingFrequencyResponse {
  frequency: Record<string, number>
}

export interface TotalVolumeResponse {
  volume: Record<string, number>
}

export interface AnalyticsSummaryResponse {
  total_trainings: number
  completed_trainings: number
  total_volume: number
}

export interface WeightProgressResponse {
  progress: Record<string, number>
}

export interface BMIProgressResponse {
  progress: Record<string, number>
}

export interface ExerciseWeightProgressResponse {
  exercise_id: number
  progress: Record<string, number>
}

export interface ExerciseVolumeProgressResponse {
  exercise_id: number
  progress: Record<string, number>
}

export const analyticsService = {
  async getTrainingFrequency(startDate?: string, endDate?: string): Promise<TrainingFrequencyResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<TrainingFrequencyResponse>('/analytics/training-frequency', { params })
    return response.data
  },

  async getTotalVolume(startDate?: string, endDate?: string): Promise<TotalVolumeResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<TotalVolumeResponse>('/analytics/total-volume', { params })
    return response.data
  },

  async getSummary(): Promise<AnalyticsSummaryResponse> {
    const response = await api.get<AnalyticsSummaryResponse>('/analytics/summary')
    return response.data
  },

  async getWeightProgress(exerciseId: number, startDate?: string, endDate?: string): Promise<ExerciseWeightProgressResponse> {
    const params: Record<string, string> = { exercise_id: exerciseId.toString() }
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<ExerciseWeightProgressResponse>('/analytics/weight-progress', { params })
    return response.data
  },

  async getVolumeProgress(exerciseId: number, startDate?: string, endDate?: string): Promise<ExerciseVolumeProgressResponse> {
    const params: Record<string, string> = { exercise_id: exerciseId.toString() }
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<ExerciseVolumeProgressResponse>('/analytics/volume-progress', { params })
    return response.data
  },

  async getUserWeightProgress(startDate?: string, endDate?: string): Promise<WeightProgressResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<WeightProgressResponse>('/analytics/user-weight-progress', { params })
    return response.data
  },

  async getUserBMIProgress(startDate?: string, endDate?: string): Promise<BMIProgressResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<BMIProgressResponse>('/analytics/user-bmi-progress', { params })
    return response.data
  },
}

