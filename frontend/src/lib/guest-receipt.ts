import type { OrderReceipt } from '../types'

const guestReceiptKey = 'pawchase-guest-receipt'

export function saveGuestReceipt(receipt: OrderReceipt) {
  sessionStorage.setItem(guestReceiptKey, JSON.stringify(receipt))
}

export function loadGuestReceipt(): OrderReceipt | null {
  const storedReceipt = sessionStorage.getItem(guestReceiptKey)
  if (!storedReceipt) return null

  try {
    return JSON.parse(storedReceipt) as OrderReceipt
  } catch {
    sessionStorage.removeItem(guestReceiptKey)
    return null
  }
}
