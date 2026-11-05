import { httpCommerceGateway } from './http-commerce-gateway'
import { mockCommerceGateway } from './mock-commerce-gateway'

export const isDemoMode = import.meta.env.VITE_USE_MOCKS !== 'false'

export const commerceGateway = !isDemoMode
  ? httpCommerceGateway
  : mockCommerceGateway

