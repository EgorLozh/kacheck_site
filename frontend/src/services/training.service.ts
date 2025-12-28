import api from './api'
import type { Training } from '../types'

export interface CreateTrainingRequest {
  date_time: string
  training_template_id?: number
  implementations?: Array<{
    exercise_id: number
    order_index: number
    sets: Array<{
      order_index: number
      weight: number
      reps: number
      rest_time?: number
      duration?: number
      rpe?: number
    }>
  }>
  duration?: number
  notes?: string
  status?: 'planned' | 'in_progress' | 'completed' | 'skipped'
}

export interface UpdateTrainingRequest {
  date_time?: string
  implementations?: Array<{
    exercise_id: number
    order_index: number
    sets: Array<{
      order_index: number
      weight: number
      reps: number
      rest_time?: number
      duration?: number
      rpe?: number
    }>
  }>
  duration?: number
  notes?: string
  status?: 'planned' | 'in_progress' | 'completed' | 'skipped'
}

export const trainingService = {
  async getTrainings(startDate?: string, endDate?: string): Promise<Training[]> {
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    const response = await api.get<Training[]>('/trainings', { params })
    return response.data
  },

  async getTrainingById(id: number): Promise<Training> {
    const response = await api.get<Training>(`/trainings/${id}`)
    return response.data
  },

  async createTraining(data: CreateTrainingRequest): Promise<Training> {
    const response = await api.post<Training>('/trainings', data)
    return response.data
  },

  async updateTraining(id: number, data: UpdateTrainingRequest): Promise<Training> {
    const response = await api.put<Training>(`/trainings/${id}`, data)
    return response.data
  },

  async deleteTraining(id: number): Promise<void> {
    await api.delete(`/trainings/${id}`)
  },

  async createTrainingFromTemplate(templateId: number, dateTime: string): Promise<Training> {
    const response = await api.post<Training>(
      `/trainings/from-template/${templateId}?date_time=${encodeURIComponent(dateTime)}`
    )
    return response.data
  },
}

