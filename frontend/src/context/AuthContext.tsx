import { useCallback, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import type { AuthState } from '../types/auth'
import { AuthContext } from './authContext'

const EMPTY_STATE: AuthState = {
  isAuthenticated: false,
  email: '',
  firstName: '',
  lastName: '',
  permissions: [],
}

function getCookie(name: string): string {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))
  return match ? decodeURIComponent(match[1]) : ''
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<AuthState>(EMPTY_STATE)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    const response = await fetch('/api/auth/me/')
    const data = await response.json()
    setAuth(
      data.is_authenticated
        ? {
            isAuthenticated: true,
            email: data.email,
            firstName: data.first_name,
            lastName: data.last_name,
            permissions: data.permissions,
          }
        : EMPTY_STATE,
    )
  }, [])

  useEffect(() => {
    refresh().finally(() => setLoading(false))
  }, [refresh])

  const logout = useCallback(async () => {
    await fetch('/api/auth/logout/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
    })
    setAuth(EMPTY_STATE)
  }, [])

  return (
    <AuthContext.Provider value={{ auth, loading, refresh, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
