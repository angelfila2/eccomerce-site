export type Category = 'Living' | 'Workspace' | 'Carry' | 'Wellness'

export interface Product {
  id: string
  slug: string
  name: string
  category: Category
  description: string
  details: string[]
  price: number
  inventory: number
  imageUrl: string
  accent: string
  featured?: boolean
}

export interface CartLine {
  product: Product
  quantity: number
}

export interface CheckoutInput {
  email: string
  fullName: string
  address: string
  city: string
  postalCode: string
  country: string
}

export interface OrderReceipt {
  id: string
  createdAt: string
  total: number
  customerEmail: string
}

