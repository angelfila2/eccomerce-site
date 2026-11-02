import { Menu, Search, ShoppingBag, X } from 'lucide-react'
import { useState } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useCart } from '../modules/cart/cart-store'

export function StoreLayout() {
  const { itemCount } = useCart()
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [search, setSearch] = useState('')
  const navigate = useNavigate()

  function submitSearch(event: React.FormEvent) {
    event.preventDefault()
    navigate(`/?search=${encodeURIComponent(search)}`)
    setSearchOpen(false)
  }

  return (
    <div className="app-shell">
      <div className="announcement">Complimentary shipping on orders over $150</div>
      <header className="site-header">
        <button className="mobile-menu-button" onClick={() => setMenuOpen((value) => !value)} aria-label="Toggle menu">
          {menuOpen ? <X /> : <Menu />}
        </button>
        <Link className="brand" to="/"><img src="/pawchase-mark.png" alt="" /><span className="brand-name">PAWCHASE</span><sup>®</sup></Link>
        <nav className={menuOpen ? 'main-nav open' : 'main-nav'} onClick={() => setMenuOpen(false)}>
          <NavLink to="/">Shop</NavLink>
          <NavLink to="/?category=Living">Living</NavLink>
          <NavLink to="/?category=Workspace">Workspace</NavLink>
          <NavLink to="/?category=Carry">Carry</NavLink>
          <NavLink to="/?category=Wellness">Wellness</NavLink>
        </nav>
        <div className="header-actions">
          <button onClick={() => setSearchOpen((value) => !value)} aria-label="Search"><Search /></button>
          <Link to="/cart" aria-label={`Cart with ${itemCount} items`}><ShoppingBag /><span>{itemCount}</span></Link>
        </div>
      </header>
      {searchOpen && (
        <form className="search-panel" onSubmit={submitSearch}>
          <Search size={20} /><input autoFocus value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search the collection" />
          <button type="submit">Search</button>
        </form>
      )}
      <main><Outlet /></main>
      <footer className="site-footer">
        <div><Link className="brand footer-brand" to="/"><img src="/pawchase-mark.png" alt="" /><span className="brand-name">PAWCHASE</span><sup>®</sup></Link><p>Fetching finds for everyday rituals.</p></div>
        <div><h4>Explore</h4><Link to="/">Collection</Link><Link to="/?category=Living">Living</Link><Link to="/?category=Workspace">Workspace</Link></div>
        <div><h4>Help</h4><a href="mailto:hello@pawchase.example">Contact</a><span>Shipping & returns</span><span>Care guide</span></div>
        <div><h4>Newsletter</h4><p>Quiet updates, new arrivals, no noise.</p><form onSubmit={(event) => event.preventDefault()}><input type="email" aria-label="Email address" placeholder="Email address" /><button>Join</button></form></div>
      </footer>
    </div>
  )
}

