import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Search, ShoppingCart, Bell, MessageCircle } from "lucide-react";

import { getMe, logout } from "../api/authApi";
import api from "../api/api";

export default function Header() {
  const [user, setUser] = useState(null);
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    async function loadUser() {
      if (!api.accessToken) {
        setUser(null);
        return;
      }

      try {
        const res = await getMe();
        setUser(res.data);
      } catch {
        setUser(null);
      }
    }

    loadUser();
  }, []);

  // ⭐ NEW: keep input in sync with URL (?q=)
  useEffect(() => {
    const q = searchParams.get("q");
    setQuery(q || "");
  }, [searchParams]);

  function handleSearch(e) {
    e.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) {
      navigate("/");
    } else {
      navigate(`/?q=${encodeURIComponent(trimmed)}`);
    }
  }

  async function handleLogout() {
    try {
      await logout();
    } finally {
      api.accessToken = null;
      setUser(null);
      navigate("/login");
    }
  }

  return (
    <header className="bg-[#ee4d2d] text-white">
      <div className="max-w-7xl mx-auto px-4">
        {/* Top bar */}
        <div className="flex items-center justify-between py-1 text-xs">
          <div className="flex items-center gap-3">
            <Link to="#" className="hover:opacity-80">
              Seller Centre
            </Link>
            <span className="opacity-60">|</span>
            <Link to="#" className="hover:opacity-80">
              Download
            </Link>
            <span className="opacity-60">|</span>
            <Link to="#" className="hover:opacity-80">
              Follow us
            </Link>
          </div>

          <div className="flex items-center gap-4">
            <Link to="#" className="flex items-center gap-1 hover:opacity-80">
              <Bell className="h-4 w-4" />
              Notifications
            </Link>

            <Link to="#" className="flex items-center gap-1 hover:opacity-80">
              <MessageCircle className="h-4 w-4" />
              Help
            </Link>

            {user ? (
              <div className="flex items-center gap-2">
                <span className="font-medium">Hello, {user.firstName}</span>
                <span className="opacity-60">|</span>
                <button
                  onClick={handleLogout}
                  className="hover:underline text-white"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/register" className="hover:opacity-80">
                  Sign Up
                </Link>
                <span className="opacity-60">|</span>
                <Link to="/login" className="hover:opacity-80">
                  Login
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Main header */}
        <div className="flex items-center gap-6 py-4">
          <Link to="/" className="text-2xl font-bold">
            ShopMart
          </Link>

          {/* Search */}
          <form onSubmit={handleSearch} className="flex-1 max-w-3xl">
            <div className="flex bg-white rounded-sm overflow-hidden">
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for products"
                className="flex-1 px-3 py-2 text-sm text-gray-700 focus:outline-none"
              />
              <button className="px-5 bg-[#fb5533] hover:bg-[#f53d2d] flex items-center justify-center">
                <Search className="h-5 w-5 text-white" />
              </button>
            </div>
          </form>

          <Link to="/cart" className="relative">
            <ShoppingCart className="h-7 w-7" />
          </Link>
        </div>
      </div>
    </header>
  );
}
