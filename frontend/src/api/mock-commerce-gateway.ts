import { products } from '../data/products'
import type { CheckoutInput, CartLine, OrderReceipt } from '../types'
import type { CommerceGateway, ProductFilters } from './commerce-gateway'

const delay = (ms = 120) => new Promise((resolve) => window.setTimeout(resolve, ms))

export const mockCommerceGateway: CommerceGateway = {
  async listProducts(filters: ProductFilters = {}) {
    await delay()
    const search = filters.search?.trim().toLowerCase()
    return products.filter((product) => {
      const categoryMatch = !filters.category || filters.category === 'All' || product.category === filters.category
      const searchMatch = !search || `${product.name} ${product.description}`.toLowerCase().includes(search)
      return categoryMatch && searchMatch
    })
  },
  async getProduct(slug: string) {
    await delay()
    return products.find((product) => product.slug === slug) ?? null
  },
  async createOrder(lines: CartLine[], checkout: CheckoutInput): Promise<OrderReceipt> {
    await delay(500)
    return {
      id: `NS-${crypto.randomUUID().slice(0, 8).toUpperCase()}`,
      createdAt: new Date().toISOString(),
      total: lines.reduce((sum, line) => sum + line.product.price * line.quantity, 0),
      customerEmail: checkout.email,
    }
  },
}

