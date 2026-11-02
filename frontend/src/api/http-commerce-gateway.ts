import type { CartLine, CheckoutInput, OrderReceipt, Product } from '../types'
import type { CommerceGateway, ProductFilters } from './commerce-gateway'

const baseUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) throw new Error(`Request failed (${response.status})`)
  return response.json() as Promise<T>
}

export const httpCommerceGateway: CommerceGateway = {
  listProducts(filters: ProductFilters = {}) {
    const params = new URLSearchParams()
    if (filters.category && filters.category !== 'All') params.set('category', filters.category)
    if (filters.search) params.set('search', filters.search)
    const query = params.size ? `?${params}` : ''
    return request<Product[]>(`/products${query}`)
  },
  getProduct(slug: string) {
    return request<Product>(`/products/${slug}`).catch((error: unknown) => {
      if (error instanceof Error && error.message.includes('(404)')) return null
      throw error
    })
  },
  createOrder(lines: CartLine[], checkout: CheckoutInput) {
    return request<OrderReceipt>('/orders', {
      method: 'POST',
      body: JSON.stringify({
        lines: lines.map(({ product, quantity }) => ({ productId: product.id, quantity })),
        checkout,
      }),
    })
  },
}

