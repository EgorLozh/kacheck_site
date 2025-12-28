import api from './api'
import type { Exercise } from '../types'

export interface CreateExerciseRequest {
  name: string
  description?: string
  muscle_group_ids: number[]
  image_path?: string
}

export interface UpdateExerciseRequest {
  name?: string
  description?: string
  muscle_group_ids?: number[]
  image_path?: string
}

export const exerciseService = {
  async getExercises(includeSystem: boolean = true): Promise<Exercise[]> {
    const response = await api.get<Exercise[]>('/exercises', {
      params: { include_system: includeSystem },
    })
    return response.data
  },

  async getExerciseById(id: number): Promise<Exercise> {
    const response = await api.get<Exercise>(`/exercises/${id}`)
    return response.data
  },

  async createExercise(data: CreateExerciseRequest): Promise<Exercise> {
    const response = await api.post<Exercise>('/exercises', data)
    return response.data
  },

  async updateExercise(id: number, data: UpdateExerciseRequest): Promise<Exercise> {
    const response = await api.put<Exercise>(`/exercises/${id}`, data)
    return response.data
  },

  async deleteExercise(id: number): Promise<void> {
    await api.delete(`/exercises/${id}`)
  },
}

