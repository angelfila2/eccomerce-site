import { ArrowLeft, ArrowRight, Trash2 } from 'lucide-react'
import { Link } from 'react-router-dom'
import { QuantityControl } from '../components/QuantityControl'
import { formatMoney } from '../lib/money'
import { useCart } from '../modules/cart/cart-store'

export function CartPage() {
  const { lines, subtotal, setQuantity, remove } = useCart()
  const shipping = subtotal >= 150 ? 0 : 12

  if (!lines.length) return (
    <section className="empty-state page-empty"><p className="eyebrow">Your bag</p><h1>Nothing here yet.</h1><p>Explore the collection and choose something worth keeping.</p><Link className="button" to="/">Browse the collection</Link></section>
  )

  return (
    <section className="cart-page page-width">
      <div className="page-title"><p className="eyebrow">Your selection</p><h1>Shopping bag</h1><p>{lines.length} {lines.length === 1 ? 'piece' : 'pieces'}</p></div>
      <div className="cart-layout">
        <div className="cart-lines">
          {lines.map(({ product, quantity }) => (
            <article className="cart-line" key={product.id}>
              <Link to={`/products/${product.slug}`}><img src={product.imageUrl} alt={product.name} /></Link>
              <div className="cart-line-info"><p className="eyebrow">{product.category}</p><Link to={`/products/${product.slug}`}><h2>{product.name}</h2></Link><p>{formatMoney(product.price)}</p><QuantityControl value={quantity} max={product.inventory} onChange={(value) => setQuantity(product.id, value)} /></div>
              <button className="remove-button" onClick={() => remove(product.id)} aria-label={`Remove ${product.name}`}><Trash2 size={18} /></button>
            </article>
          ))}
          <Link className="continue-link" to="/"><ArrowLeft size={17} /> Continue shopping</Link>
        </div>
        <aside className="order-summary"><p className="eyebrow">Order summary</p><div><span>Subtotal</span><strong>{formatMoney(subtotal)}</strong></div><div><span>Shipping</span><strong>{shipping ? formatMoney(shipping) : 'Complimentary'}</strong></div><div className="summary-total"><span>Total</span><strong>{formatMoney(subtotal + shipping)}</strong></div>{subtotal < 150 && <p className="shipping-note">Add {formatMoney(150 - subtotal)} more for complimentary shipping.</p>}<Link className="button wide" to="/checkout">Continue to checkout <ArrowRight size={18} /></Link><small>Taxes calculated at checkout.</small></aside>
      </div>
    </section>
  )
}

