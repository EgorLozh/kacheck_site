import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authService } from '../services/auth.service'
import { userProfileService } from '../services/user-profile.service'
import type { User } from '../types'

interface AuthContextType {
  isAuthenticated: boolean
  token: string | null
  user: User | null
  setToken: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [token, setTokenState] = useState<string | null>(authService.getToken())
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!token)
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    setIsAuthenticated(!!token)
    if (token) {
      loadUser()
    } else {
      setUser(null)
    }
  }, [token])

  const loadUser = async () => {
    try {
      const profile = await userProfileService.getProfile()
      setUser({
        id: profile.id,
        email: profile.email,
        username: profile.username,
      })
    } catch (err) {
      console.error('Ошибка загрузки профиля:', err)
      setUser(null)
    }
  }

  const setToken = (newToken: string) => {
    authService.setToken(newToken)
    setTokenState(newToken)
  }

  const logout = () => {
    authService.logout()
    setTokenState(null)
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, token, user, setToken, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}




