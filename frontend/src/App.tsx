import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { StoreLayout } from './layouts/StoreLayout'
import { CartProvider } from './modules/cart/cart-store'
import { CartPage } from './pages/CartPage'
import { CheckoutPage } from './pages/CheckoutPage'
import { HomePage } from './pages/HomePage'
import { NotFoundPage } from './pages/NotFoundPage'
import { OrderConfirmedPage } from './pages/OrderConfirmedPage'
import { ProductPage } from './pages/ProductPage'

const router = createBrowserRouter([{ path: '/', element: <StoreLayout />, children: [
  { index: true, element: <HomePage /> },
  { path: 'products/:slug', element: <ProductPage /> },
  { path: 'cart', element: <CartPage /> },
  { path: 'checkout', element: <CheckoutPage /> },
  { path: 'order-confirmed', element: <OrderConfirmedPage /> },
  { path: '*', element: <NotFoundPage /> },
]}])

export default function App() {
  return <CartProvider><RouterProvider router={router} /></CartProvider>
}

