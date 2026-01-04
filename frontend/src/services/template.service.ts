import api from './api'
import type { TrainingTemplate } from '../types'

export interface CreateTemplateRequest {
  name: string
  description?: string
  implementation_templates: Array<{
    exercise_id: number
    order_index: number
    set_templates: Array<{
      order_index: number
      weight?: number
      reps?: number
    }>
  }>
}

export interface UpdateTemplateRequest {
  name?: string
  description?: string
  implementation_templates?: Array<{
    exercise_id: number
    order_index: number
    set_templates: Array<{
      order_index: number
      weight?: number
      reps?: number
    }>
  }>
}

export const templateService = {
  async getTemplates(includeSystem: boolean = true): Promise<TrainingTemplate[]> {
    const response = await api.get<TrainingTemplate[]>('/training-templates', {
      params: { include_system: includeSystem },
    })
    return response.data
  },

  async getTemplateById(id: number): Promise<TrainingTemplate> {
    const response = await api.get<TrainingTemplate>(`/training-templates/${id}`)
    return response.data
  },

  async createTemplate(data: CreateTemplateRequest): Promise<TrainingTemplate> {
    const response = await api.post<TrainingTemplate>('/training-templates', data)
    return response.data
  },

  async updateTemplate(id: number, data: UpdateTemplateRequest): Promise<TrainingTemplate> {
    const response = await api.put<TrainingTemplate>(`/training-templates/${id}`, data)
    return response.data
  },

  async deleteTemplate(id: number): Promise<void> {
    await api.delete(`/training-templates/${id}`)
  },
}




