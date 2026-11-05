import type { CartLine, CheckoutInput, OrderReceipt, Product, RecommendationContext, RecommendationResponse } from '../types'

export interface ProductFilters {
  category?: string
  search?: string
}

export interface CommerceGateway {
  listProducts(filters?: ProductFilters): Promise<Product[]>
  getProduct(slug: string): Promise<Product | null>
  getRecommendations(context: RecommendationContext): Promise<RecommendationResponse>
  createOrder(lines: CartLine[], checkout: CheckoutInput): Promise<OrderReceipt>
}

