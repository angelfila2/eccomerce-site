import { Check } from 'lucide-react'
import { Link, Navigate, useLocation } from 'react-router-dom'
import { loadGuestReceipt } from '../lib/guest-receipt'
import { formatMoney } from '../lib/money'
import type { OrderReceipt } from '../types'

export function OrderConfirmedPage() {
  const receiptFromNavigation = (useLocation().state as { receipt?: OrderReceipt } | null)?.receipt
  const receipt = receiptFromNavigation ?? loadGuestReceipt()
  if (!receipt) return <Navigate to="/" replace />

  const orderDate = new Intl.DateTimeFormat('en-SG', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(receipt.createdAt))

  return <section className="confirmation page-empty"><span className="confirmation-icon"><Check /></span><p className="eyebrow">Order confirmed</p><h1>Thank you.</h1><p>Your guest order has been received. Keep this receipt or save your order number for reference.</p><article className="guest-receipt"><header><div><span className="eyebrow">Guest receipt</span><strong>PAWCHASE</strong></div><small>No account required</small></header><dl><div><dt>Order number</dt><dd>{receipt.id}</dd></div><div><dt>Placed</dt><dd>{orderDate}</dd></div><div><dt>Contact</dt><dd>{receipt.customerEmail}</dd></div><div className="receipt-total"><dt>Total</dt><dd>{formatMoney(receipt.total)}</dd></div></dl><p>This receipt is saved only in this browser tab. Account order history can be added when login is available.</p></article><Link className="button" to="/">Return to the collection</Link></section>
}

