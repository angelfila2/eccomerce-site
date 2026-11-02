import type { CartLine, CheckoutInput, OrderReceipt, Product } from '../types'

export interface ProductFilters {
  category?: string
  search?: string
}

export interface CommerceGateway {
  listProducts(filters?: ProductFilters): Promise<Product[]>
  getProduct(slug: string): Promise<Product | null>
  createOrder(lines: CartLine[], checkout: CheckoutInput): Promise<OrderReceipt>
}

