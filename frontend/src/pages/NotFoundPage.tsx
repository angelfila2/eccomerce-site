import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return <section className="empty-state page-empty"><p className="eyebrow">404</p><h1>That page wandered off.</h1><Link className="button" to="/">Return home</Link></section>
}

