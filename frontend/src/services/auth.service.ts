import api from './api'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types'

export const authService = {
  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', data)
    return response.data
  },

  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
  },

  getToken(): string | null {
    return localStorage.getItem('access_token')
  },

  setToken(token: string) {
    localStorage.setItem('access_token', token)
  },
}


