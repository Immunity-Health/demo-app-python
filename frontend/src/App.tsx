import { NavLink, Outlet } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <>
      <header className="site-header">
        <h1>Customer Demo</h1>
        <nav>
          <NavLink to="/customers" end>
            Customers
          </NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </>
  )
}

export default App
