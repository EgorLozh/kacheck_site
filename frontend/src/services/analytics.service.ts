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

export interface PR {
  exercise_id: number
  exercise_name: string
  weight: number
  reps: number
  date: string
  training_id: number
}

export interface PRsResponse {
  prs: PR[]
}

export interface ExercisePRResponse {
  exercise_id: number
  exercise_name?: string
  pr: {
    weight: number
    reps: number
    date: string
    training_id: number
  } | null
}

export interface OneRMProgressResponse {
  exercise_id: number
  formula: string
  progress: Record<string, number>
}

export interface MuscleGroupVolumeItem {
  muscle_group_id: number
  muscle_group_name: string
  volume: number
}

export interface MuscleGroupVolumeResponse {
  volume_by_group: MuscleGroupVolumeItem[]
}

export interface MuscleGroupFrequencyItem {
  muscle_group_id: number
  muscle_group_name: string
  frequency: number
}

export interface MuscleGroupFrequencyResponse {
  frequency_by_group: MuscleGroupFrequencyItem[]
}

export interface NewRecord {
  type: 'first_time' | 'pr'
  exercise_id: number
  exercise_name: string
  weight: number
  reps: number
  date: string
  training_id: number
}

export interface NewRecordsResponse {
  new_records: NewRecord[]
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

  async getStreak(): Promise<{ streak: number }> {
    const response = await api.get<{ streak: number }>('/analytics/streak')
    return response.data
  },

  async getAllPRs(limit?: number): Promise<PRsResponse> {
    const params: Record<string, string> = {}
    if (limit) params.limit = limit.toString()
    
    const response = await api.get<PRsResponse>('/analytics/prs', { params })
    return response.data
  },

  async getExercisePR(exerciseId: number): Promise<ExercisePRResponse> {
    const response = await api.get<ExercisePRResponse>(`/analytics/exercise/${exerciseId}/pr`)
    return response.data
  },

  async getExercise1RMProgress(
    exerciseId: number,
    startDate?: string,
    endDate?: string,
    formula?: string
  ): Promise<OneRMProgressResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    if (formula) params.formula = formula
    
    const response = await api.get<OneRMProgressResponse>(
      `/analytics/exercise/${exerciseId}/1rm-progress`,
      { params }
    )
    return response.data
  },

  async getMuscleGroupVolume(startDate?: string, endDate?: string): Promise<MuscleGroupVolumeResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<MuscleGroupVolumeResponse>('/analytics/muscle-groups/volume', { params })
    return response.data
  },

  async getMuscleGroupFrequency(startDate?: string, endDate?: string): Promise<MuscleGroupFrequencyResponse> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<MuscleGroupFrequencyResponse>(
      '/analytics/muscle-groups/frequency',
      { params }
    )
    return response.data
  },

  async getNewRecords(): Promise<NewRecordsResponse> {
    const response = await api.get<NewRecordsResponse>('/analytics/new-records')
    return response.data
  },
}


