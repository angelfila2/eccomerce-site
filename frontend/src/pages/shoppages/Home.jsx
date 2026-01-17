import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import ProductCard from "../../components/products/ProductCard";
import {
  getProducts,
  getProductsByCategory,
  searchProducts,
} from "../../api/productApi";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const [searchParams] = useSearchParams();
  const categoryId = searchParams.get("categoryId");
  const query = searchParams.get("q");

  useEffect(() => {
    async function loadProducts() {
      setLoading(true);

      try {
        let res;

        if (query) {
          res = await searchProducts(query);
        } else if (categoryId) {
          res = await getProductsByCategory(categoryId);
        } else {
          res = await getProducts();
        }

        setProducts(res.data);
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, [categoryId, query]);

  return (
    <main className="max-w-7xl mx-auto p-4">
      {loading ? (
        <div className="text-sm text-muted-foreground">Loading products…</div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {products.map((product) => (
            <ProductCard key={product.productId} product={product} />
          ))}

          {products.length === 0 && (
            <div className="col-span-full text-center text-muted-foreground">
              No products found
            </div>
          )}
        </div>
      )}
    </main>
  );
}
