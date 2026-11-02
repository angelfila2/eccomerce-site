import { ArrowUpRight, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { formatMoney } from '../lib/money'
import { useCart } from '../modules/cart/cart-store'
import type { Product } from '../types'

export function ProductCard({ product }: { product: Product }) {
  const { add } = useCart()
  return (
    <article className="product-card">
      <Link to={`/products/${product.slug}`} className="product-image-wrap" aria-label={`View ${product.name}`}>
        <img className="product-image" src={product.imageUrl} alt={product.name} />
        <span className="product-arrow"><ArrowUpRight size={18} /></span>
      </Link>
      <div className="product-meta">
        <div>
          <p className="eyebrow">{product.category}</p>
          <Link to={`/products/${product.slug}`}><h3>{product.name}</h3></Link>
          <p>{formatMoney(product.price)}</p>
        </div>
        <button className="icon-button" type="button" onClick={() => add(product)} aria-label={`Add ${product.name} to cart`}>
          <Plus size={19} />
        </button>
      </div>
    </article>
  )
}

