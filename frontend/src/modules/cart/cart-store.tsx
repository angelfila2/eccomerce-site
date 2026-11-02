import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import type { CartLine, Product } from '../../types'

interface CartStore {
  lines: CartLine[]
  itemCount: number
  subtotal: number
  add: (product: Product, quantity?: number) => void
  setQuantity: (productId: string, quantity: number) => void
  remove: (productId: string) => void
  clear: () => void
}

const storageKey = 'pawchase-cart-v1'
const CartContext = createContext<CartStore | null>(null)

function loadCart(): CartLine[] {
  try {
    const stored = localStorage.getItem(storageKey)
    return stored ? JSON.parse(stored) as CartLine[] : []
  } catch {
    return []
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [lines, setLines] = useState<CartLine[]>(loadCart)

  useEffect(() => localStorage.setItem(storageKey, JSON.stringify(lines)), [lines])

  const store = useMemo<CartStore>(() => ({
    lines,
    itemCount: lines.reduce((sum, line) => sum + line.quantity, 0),
    subtotal: lines.reduce((sum, line) => sum + line.product.price * line.quantity, 0),
    add(product, quantity = 1) {
      setLines((current) => {
        const existing = current.find((line) => line.product.id === product.id)
        if (!existing) return [...current, { product, quantity }]
        return current.map((line) => line.product.id === product.id
          ? { ...line, quantity: Math.min(product.inventory, line.quantity + quantity) }
          : line)
      })
    },
    setQuantity(productId, quantity) {
      setLines((current) => current
        .map((line) => line.product.id === productId
          ? { ...line, quantity: Math.min(line.product.inventory, Math.max(0, quantity)) }
          : line)
        .filter((line) => line.quantity > 0))
    },
    remove(productId) {
      setLines((current) => current.filter((line) => line.product.id !== productId))
    },
    clear() { setLines([]) },
  }), [lines])

  return <CartContext.Provider value={store}>{children}</CartContext.Provider>
}

// This module keeps the hook beside its provider so the storage invariant stays local.
// eslint-disable-next-line react-refresh/only-export-components
export function useCart(): CartStore {
  const store = useContext(CartContext)
  if (!store) throw new Error('useCart must be used inside CartProvider')
  return store
}

