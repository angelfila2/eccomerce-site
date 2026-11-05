import { products } from '../data/products'
import type { CheckoutInput, CartLine, OrderReceipt, RecommendationContext } from '../types'
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
  async getRecommendations({ seedProductIds, limit = 4 }: RecommendationContext) {
    await delay(220)
    const seeds = products.filter((product) => seedProductIds.includes(product.id))
    const preferredCategories = new Set(seeds.map((product) => product.category))
    const ranked = products
      .filter((product) => !seedProductIds.includes(product.id) && product.inventory > 0)
      .map((product) => {
        const categoryMatch = preferredCategories.has(product.category)
        const score = seeds.length
          ? (categoryMatch ? 0.78 : 0.42) + (product.featured ? 0.08 : 0)
          : product.featured ? 0.72 : 0.38
        return {
          product,
          score,
          reason: seeds.length
            ? categoryMatch
              ? `Matches your interest in ${product.category}`
              : 'A popular complement to your recent picks'
            : 'A popular place to start',
        }
      })
      .sort((left, right) => right.score - left.score)
      .slice(0, limit)

    return {
      items: ranked,
      strategy: seeds.length ? 'mock_session_profile' : 'featured_fallback',
      modelVersion: 'frontend-mock-v1',
    }
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

