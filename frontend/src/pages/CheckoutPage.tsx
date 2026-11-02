import { ArrowLeft, LockKeyhole } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { commerceGateway } from '../api'
import { formatMoney } from '../lib/money'
import { useCart } from '../modules/cart/cart-store'
import type { CheckoutInput } from '../types'

const initialForm: CheckoutInput = { email: '', fullName: '', address: '', city: '', postalCode: '', country: '' }

export function CheckoutPage() {
  const { lines, subtotal, clear } = useCart()
  const [form, setForm] = useState(initialForm)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const shipping = subtotal >= 150 ? 0 : 12
  if (!lines.length) return <Navigate to="/cart" replace />

  async function submit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true); setError('')
    try {
      const receipt = await commerceGateway.createOrder(lines, form)
      clear()
      navigate('/order-confirmed', { state: { receipt } })
    } catch {
      setError('We could not place your order. Please try again.')
    } finally { setSubmitting(false) }
  }

  function field(name: keyof CheckoutInput, label: string, options?: { type?: string; span?: boolean }) {
    return <label className={options?.span ? 'field span' : 'field'}><span>{label}</span><input required type={options?.type ?? 'text'} value={form[name]} onChange={(event) => setForm({ ...form, [name]: event.target.value })} /></label>
  }

  return (
    <section className="checkout-page page-width">
      <Link className="continue-link" to="/cart"><ArrowLeft size={17} /> Back to bag</Link>
      <div className="checkout-layout">
        <form className="checkout-form" onSubmit={submit}><p className="eyebrow">Checkout</p><h1>Where should we send it?</h1><div className="form-grid">{field('email', 'Email', { type: 'email', span: true })}{field('fullName', 'Full name', { span: true })}{field('address', 'Street address', { span: true })}{field('city', 'City')}{field('postalCode', 'Postal code')}{field('country', 'Country', { span: true })}</div><div className="payment-placeholder"><LockKeyhole size={20} /><div><strong>Payment comes next</strong><p>This frontend demo places a mock order. Add a payment provider only after the backend order transaction and webhook handling are implemented.</p></div></div>{error && <p className="form-error">{error}</p>}<button disabled={submitting} className="button wide" type="submit">{submitting ? 'Placing order…' : `Place order · ${formatMoney(subtotal + shipping)}`}</button></form>
        <aside className="checkout-summary"><p className="eyebrow">In your bag</p>{lines.map(({ product, quantity }) => <div className="checkout-line" key={product.id}><img src={product.imageUrl} alt="" /><p><strong>{product.name}</strong><span>Qty {quantity}</span></p><strong>{formatMoney(product.price * quantity)}</strong></div>)}<div className="summary-total"><span>Total</span><strong>{formatMoney(subtotal + shipping)}</strong></div></aside>
      </div>
    </section>
  )
}

