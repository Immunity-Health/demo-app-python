import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import type { Customer, NewCustomer } from '../types/customer'
import { useAuth } from '../context/useAuth'

const EMPTY_FORM: NewCustomer = {
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: '',
  aadhar_number: '',
}

function CustomersPage() {
  const { auth } = useAuth()
  const canAddCustomer = auth.permissions.includes('customers.add_customer')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [form, setForm] = useState<NewCustomer>(EMPTY_FORM)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadCustomers = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/customers/')
      if (!response.ok) throw new Error(`Failed to load customers (${response.status})`)
      setCustomers(await response.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load customers')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCustomers()
  }, [])

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const response = await fetch('/api/customers/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!response.ok) throw new Error(`Failed to add customer (${response.status})`)
      setForm(EMPTY_FORM)
      await loadCustomers()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add customer')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="customers">
      {canAddCustomer && (
        <form className="customer-form" onSubmit={handleSubmit}>
          <h2>Add customer</h2>
          <input
            required
            placeholder="First name"
            value={form.first_name}
            onChange={(e) => setForm({ ...form, first_name: e.target.value })}
          />
          <input
            required
            placeholder="Last name"
            value={form.last_name}
            onChange={(e) => setForm({ ...form, last_name: e.target.value })}
          />
          <input
            required
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <input
            placeholder="Phone"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
          />
          <input
            placeholder="Address"
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />
          <input
            placeholder="Aadhar number"
            value={form.aadhar_number}
            onChange={(e) => setForm({ ...form, aadhar_number: e.target.value })}
          />
          <button type="submit" disabled={submitting}>
            {submitting ? 'Adding…' : 'Add customer'}
          </button>
        </form>
      )}

      {error && <p className="error">{error}</p>}

      <h2>Customers</h2>
      {loading ? (
        <p>Loading…</p>
      ) : customers.length === 0 ? (
        <p>No customers yet.</p>
      ) : (
        <table className="customer-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
              <th>Aadhar Number</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td>
                  {customer.first_name} {customer.last_name}
                </td>
                <td>{customer.email}</td>
                <td>{customer.phone}</td>
                <td>{customer.address}</td>
                <td>{customer.aadhar_number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default CustomersPage
