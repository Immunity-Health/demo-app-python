import { createContext } from 'react'
import type { AuthState } from '../types/auth'

export interface AuthContextValue {
  auth: AuthState
  loading: boolean
  refresh: () => Promise<void>
  logout: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
