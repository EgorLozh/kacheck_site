import api from './api'
import type { MuscleGroup } from '../types'

export const muscleGroupService = {
  async getMuscleGroups(includeSystem: boolean = true): Promise<MuscleGroup[]> {
    const response = await api.get<MuscleGroup[]>('/muscle-groups', {
      params: { include_system: includeSystem },
    })
    return response.data
  },
}




