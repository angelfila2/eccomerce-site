import { Check } from 'lucide-react'
import { Link, Navigate, useLocation } from 'react-router-dom'
import { formatMoney } from '../lib/money'
import type { OrderReceipt } from '../types'

export function OrderConfirmedPage() {
  const receipt = (useLocation().state as { receipt?: OrderReceipt } | null)?.receipt
  if (!receipt) return <Navigate to="/" replace />
  return <section className="confirmation page-empty"><span className="confirmation-icon"><Check /></span><p className="eyebrow">Order confirmed</p><h1>Thank you.</h1><p>Your order <strong>{receipt.id}</strong> has been received. A confirmation will be sent to {receipt.customerEmail}.</p><div><span>Total</span><strong>{formatMoney(receipt.total)}</strong></div><Link className="button" to="/">Return to the collection</Link></section>
}

