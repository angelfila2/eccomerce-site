import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import { getCategories } from "../api/categoryApi";

export default function CategoryBar() {
  const [categories, setCategories] = useState([]);
  const location = useLocation();

  useEffect(() => {
    async function loadCategories() {
      try {
        const res = await getCategories();
        setCategories(res.data);
      } catch {
        setCategories([]);
      }
    }

    loadCategories();
  }, []);

  function isActive(categoryId) {
    return location.search === `?categoryId=${categoryId}`;
  }

  return (
    <div className="bg-background border-b border-border">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center gap-6 py-3 overflow-x-auto scrollbar-hide text-sm">
          {/* All Categories */}
          <Link
            to="/"
            className={`whitespace-nowrap transition-colors ${
              location.search === ""
                ? "text-primary font-semibold"
                : "text-foreground hover:text-primary"
            }`}
          >
            All Categories
          </Link>

          {categories.map((category) => (
            <Link
              key={category.categoryId}
              to={`/?categoryId=${category.categoryId}`}
              className={`whitespace-nowrap transition-colors ${
                isActive(category.id)
                  ? "text-primary font-semibold"
                  : "text-foreground hover:text-primary"
              }`}
            >
              {category.categoryName}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
