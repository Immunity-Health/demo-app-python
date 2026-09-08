import '../App.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

function LoginPage() {
  return (
    <section className="login">
      <h2>Sign in</h2>
      <p>Choose an identity provider to continue.</p>
      <div className="login-buttons">
        <a className="login-button login-button-google" href={`${API_BASE}/api/auth/google/login/`}>
          Continue with Google
        </a>
        <a className="login-button login-button-zoho" href={`${API_BASE}/api/auth/zoho/login/`}>
          Continue with Zoho
        </a>
      </div>
    </section>
  )
}

export default LoginPage
