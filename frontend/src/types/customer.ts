export interface Customer {
  id: number
  first_name: string
  last_name: string
  email: string
  phone: string
  address: string
  aadhar_number: string
}

export type NewCustomer = Omit<Customer, 'id'>
