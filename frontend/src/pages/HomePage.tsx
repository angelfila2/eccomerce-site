import { ArrowRight } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { commerceGateway } from '../api'
import { PageLoader } from '../components/PageLoader'
import { ProductCard } from '../components/ProductCard'
import { RecommendationSection } from '../components/RecommendationSection'
import { getRecentProductIds } from '../lib/recent-products'
import { useCart } from '../modules/cart/cart-store'
import type { Product } from '../types'

const categories = ['All', 'Living', 'Workspace', 'Carry', 'Wellness']

export function HomePage() {
  const { lines } = useCart()
  const [params, setParams] = useSearchParams()
  const category = params.get('category') ?? 'All'
  const search = params.get('search') ?? ''
  const queryKey = `${category}:${search}`
  const [result, setResult] = useState<{ key: string; products: Product[] }>({ key: '', products: [] })

  useEffect(() => {
    let active = true
    commerceGateway.listProducts({ category, search }).then((products) => {
      if (active) setResult({ key: queryKey, products })
    })
    return () => { active = false }
  }, [category, search, queryKey])

  const title = useMemo(() => search ? `Results for “${search}”` : category === 'All' ? 'The everyday collection' : category, [category, search])
  const loading = result.key !== queryKey
  const products = result.products
  const recommendationSeeds = useMemo(() => Array.from(new Set([
    ...lines.map((line) => line.product.id),
    ...getRecentProductIds(),
  ])).slice(0, 8), [lines])

  return (
    <>
      {!search && category === 'All' && (
        <section className="hero">
          <img src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=2000&q=90" alt="Calm modern interior" />
          <div className="hero-copy"><p className="eyebrow">Edition 01 · 2026</p><h1>Live with<br /><em>intention.</em></h1><p>Useful, enduring objects chosen to bring clarity to the everyday.</p><a href="#collection">Discover the collection <ArrowRight size={18} /></a></div>
        </section>
      )}
      {!search && category === 'All' && <RecommendationSection seedProductIds={recommendationSeeds} />}
      <section className="catalog-section" id="collection">
        <div className="section-heading"><div><p className="eyebrow">Curated essentials</p><h2>{title}</h2></div><p>{products.length} pieces</p></div>
        <div className="category-tabs" aria-label="Product categories">
          {categories.map((item) => <button key={item} className={category === item ? 'active' : ''} onClick={() => setParams(item === 'All' ? {} : { category: item })}>{item}</button>)}
        </div>
        {loading ? <PageLoader /> : products.length ? <div className="product-grid">{products.map((product) => <ProductCard key={product.id} product={product} />)}</div> : <div className="empty-state"><h3>No pieces found</h3><p>Try another category or a broader search.</p><button className="button secondary" onClick={() => setParams({})}>View all products</button></div>}
      </section>
      {!search && category === 'All' && <section className="manifesto"><p className="eyebrow">Our point of view</p><blockquote>“Buy fewer things. Choose the ones that quietly earn their place.”</blockquote><p>We select for usefulness, material honesty, and a life beyond the trend cycle.</p></section>}
    </>
  )
}

