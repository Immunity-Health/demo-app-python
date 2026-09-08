import { Navigate, NavLink, Outlet } from 'react-router-dom'
import './App.css'
import { useAuth } from './context/useAuth'

function App() {
  const { auth, loading, logout } = useAuth()

  if (loading) return null
  if (!auth.isAuthenticated) return <Navigate to="/login" replace />

  return (
    <>
      <header className="site-header">
        <h1>Customer Demo</h1>
        <nav>
          <NavLink to="/customers" end>
            Customers
          </NavLink>
        </nav>
        <div className="user-info">
          <span>{auth.email}</span>
          <button type="button" onClick={() => logout()}>
            Logout
          </button>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </>
  )
}

export default App
