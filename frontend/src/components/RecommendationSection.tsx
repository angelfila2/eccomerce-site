import { Sparkles } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { commerceGateway } from '../api'
import type { Product, RecommendationResponse } from '../types'
import { ProductCard } from './ProductCard'

interface RecommendationSectionProps {
  seedProductIds: string[]
}

function fallbackResponse(products: Product[], seedProductIds: string[]): RecommendationResponse {
  const available = products.filter((product) => product.inventory > 0 && !seedProductIds.includes(product.id))
  const featured = available.filter((product) => product.featured)
  const selected = [...featured, ...available.filter((product) => !product.featured)].slice(0, 4)
  return {
    items: selected.map((product) => ({ product, score: 0, reason: 'A popular place to start' })),
    strategy: 'catalog_fallback',
    modelVersion: 'fallback-v1',
  }
}

export function RecommendationSection({ seedProductIds }: RecommendationSectionProps) {
  const [response, setResponse] = useState<RecommendationResponse>()

  useEffect(() => {
    let active = true

    commerceGateway.getRecommendations({ seedProductIds, limit: 4 })
      .catch(async () => fallbackResponse(await commerceGateway.listProducts(), seedProductIds))
      .then((result) => {
        if (active) setResponse(result)
      })

    return () => { active = false }
  }, [seedProductIds])

  const subtitle = useMemo(() => seedProductIds.length
    ? 'Shaped by the pieces you recently explored.'
    : 'A thoughtful starting point, selected from the collection.', [seedProductIds.length])

  return (
    <section className="recommendation-section" aria-labelledby="recommendation-title">
      <div className="recommendation-heading">
        <div>
          <p className="eyebrow"><Sparkles size={13} /> Personal selection</p>
          <h2 id="recommendation-title">Recommended for you</h2>
          <p>{subtitle}</p>
        </div>
        {response && <span className="recommendation-status">Personalized · {response.items.length} pieces</span>}
      </div>

      {!response ? (
        <div className="recommendation-skeleton" aria-label="Loading recommendations">
          {Array.from({ length: 4 }, (_, index) => <span key={index} />)}
        </div>
      ) : response.items.length ? (
        <div className="product-grid recommendation-grid">
          {response.items.map(({ product, reason }) => (
            <div className="recommendation-item" key={product.id}>
              <ProductCard product={product} />
              <p className="recommendation-reason"><Sparkles size={12} /> {reason}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="recommendation-empty">Explore the collection to shape your recommendations.</p>
      )}
    </section>
  )
}
