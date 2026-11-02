import { httpCommerceGateway } from './http-commerce-gateway'
import { mockCommerceGateway } from './mock-commerce-gateway'

export const commerceGateway = import.meta.env.VITE_USE_MOCKS === 'false'
  ? httpCommerceGateway
  : mockCommerceGateway

