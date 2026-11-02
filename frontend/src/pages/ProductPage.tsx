import { ArrowLeft, Check, ShoppingBag } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { commerceGateway } from '../api'
import { PageLoader } from '../components/PageLoader'
import { QuantityControl } from '../components/QuantityControl'
import { formatMoney } from '../lib/money'
import { useCart } from '../modules/cart/cart-store'
import type { Product } from '../types'

export function ProductPage() {
  const { slug = '' } = useParams()
  const [product, setProduct] = useState<Product | null | undefined>()
  const [quantity, setQuantity] = useState(1)
  const [added, setAdded] = useState(false)
  const { add } = useCart()

  useEffect(() => { commerceGateway.getProduct(slug).then(setProduct) }, [slug])
  if (product === undefined) return <PageLoader />
  if (product === null) return <div className="empty-state page-empty"><h1>Product not found</h1><Link className="button" to="/">Return to shop</Link></div>

  function addToCart() {
    add(product as Product, quantity)
    setAdded(true)
    window.setTimeout(() => setAdded(false), 1800)
  }

  return (
    <section className="product-detail">
      <div className="product-detail-image"><img src={product.imageUrl} alt={product.name} /><Link to="/"><ArrowLeft size={17} /> Back to collection</Link></div>
      <div className="product-detail-copy">
        <p className="eyebrow">{product.category} · In stock</p><h1>{product.name}</h1><p className="detail-price">{formatMoney(product.price)}</p>
        <p className="detail-description">{product.description}</p>
        <ul>{product.details.map((detail) => <li key={detail}><Check size={16} />{detail}</li>)}</ul>
        <div className="buy-row"><QuantityControl value={quantity} max={product.inventory} onChange={(value) => setQuantity(Math.max(1, value))} /><button className="button" onClick={addToCart}>{added ? <><Check /> Added</> : <><ShoppingBag /> Add to cart</>}</button></div>
        <div className="product-notes"><p><strong>Delivery</strong><span>Complimentary over $150. Ships in 1–2 business days.</span></p><p><strong>Returns</strong><span>Return unused pieces within 30 days.</span></p></div>
      </div>
    </section>
  )
}

