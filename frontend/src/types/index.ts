export interface User {
  id: number
  email: string
  username: string
}

export interface Exercise {
  id: number
  name: string
  description?: string
  image_path?: string
  is_custom: boolean
  user_id?: number
  muscle_group_ids: number[]
}

export interface MuscleGroup {
  id: number
  name: string
  is_system: boolean
}

export interface SetTemplate {
  order_index: number
  weight?: number
  reps?: number
}

export interface ImplementationTemplate {
  exercise_id: number
  order_index: number
  set_templates: SetTemplate[]
}

export interface TrainingTemplate {
  id: number
  name: string
  description?: string
  user_id?: number
  implementation_templates: ImplementationTemplate[]
}

export interface Set {
  order_index: number
  weight: number
  reps: number
  rest_time?: number
  duration?: number
  rpe?: number
}

export interface Implementation {
  exercise_id: number
  order_index: number
  sets: Set[]
}

export interface Training {
  id: number
  user_id: number
  training_template_id?: number
  date_time: string
  duration?: number
  notes?: string
  status: 'planned' | 'completed' | 'skipped'
  implementations: Implementation[]
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

