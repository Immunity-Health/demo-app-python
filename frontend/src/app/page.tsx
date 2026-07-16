"use client";

import { FormEvent, useEffect, useState } from "react";

type Customer = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/customers/";

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    address: "",
  });
  const [message, setMessage] = useState("");

  const loadCustomers = async () => {
    const response = await fetch(API_BASE_URL);
    const payload = (await response.json()) as Customer[];
    setCustomers(payload);
  };

  useEffect(() => {
    const controller = new AbortController();
    fetch(API_BASE_URL, { signal: controller.signal })
      .then((response) => response.json())
      .then((payload: Customer[]) => setCustomers(payload))
      .catch(() => setMessage("Could not load customers. Start backend and refresh."));

    return () => controller.abort();
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const response = await fetch(API_BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    if (!response.ok) {
      setMessage("Could not save customer. Check backend server and try again.");
      return;
    }

    setMessage("Customer saved. PII is encrypted in the backend database.");
    setForm({ first_name: "", last_name: "", email: "", phone: "", address: "" });
    await loadCustomers();
  };

  return (
    <main className="mx-auto max-w-5xl p-8">
      <h1 className="text-3xl font-bold">Customer Data Management Demo (Next.js + Django)</h1>
      <p className="mt-2 text-gray-600">
        This UI is built with TypeScript Next.js. Django handles AES-256 PII encryption.
      </p>

      <form onSubmit={handleSubmit} className="mt-6 grid max-w-xl gap-3 rounded border p-4">
        <input
          required
          placeholder="First name"
          className="rounded border p-2"
          value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
        />
        <input
          required
          placeholder="Last name"
          className="rounded border p-2"
          value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
        />
        <input
          required
          type="email"
          placeholder="Email"
          className="rounded border p-2"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          placeholder="Phone"
          className="rounded border p-2"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />
        <textarea
          placeholder="Address"
          className="rounded border p-2"
          value={form.address}
          onChange={(e) => setForm({ ...form, address: e.target.value })}
        />
        <button className="rounded bg-black px-4 py-2 text-white" type="submit">
          Save customer
        </button>
        {message && <p className="text-sm text-blue-700">{message}</p>}
      </form>

      <h2 className="mt-8 text-xl font-semibold">Customers</h2>
      <div className="mt-3 overflow-auto rounded border">
        <table className="min-w-full border-collapse text-left">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">Name</th>
              <th className="border p-2">Email</th>
              <th className="border p-2">Phone</th>
              <th className="border p-2">Address</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td className="border p-2">
                  {customer.first_name} {customer.last_name}
                </td>
                <td className="border p-2">{customer.email}</td>
                <td className="border p-2">{customer.phone}</td>
                <td className="border p-2">{customer.address}</td>
              </tr>
            ))}
            {customers.length === 0 && (
              <tr>
                <td colSpan={4} className="border p-2 text-center text-gray-500">
                  No customers yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}
