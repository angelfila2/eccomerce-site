import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Header from "../../components/Header";
import CategoryBar from "../../components/CategoryBar";

import { getProductById } from "../../api/productApi";
import { addToCart } from "../../api/cartApi";
import { useNotification } from "../../context/NotificationContext";

export default function ProductDetailPage() {
  const { id } = useParams();
  const { show } = useNotification();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [buyQty, setBuyQty] = useState(1);

  async function loadProduct() {
    try {
      const res = await getProductById(id);
      setProduct(res.data);
    } catch (err) {
      console.error(err);
      show("Failed to load product", "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleAddToCart() {
    try {
      await addToCart(product.productId, buyQty);
      show("Added to cart", "success");
    } catch (err) {
      if (err.response?.status === 401) {
        show("Please login to perform this action", "info");
        return;
      }
      show("Failed to add to cart", "error");
    }
  }

  useEffect(() => {
    loadProduct();
  }, [id]);

  useEffect(() => {
    if (product) setBuyQty(1);
  }, [product]);

  return (
    <>
      <main className="max-w-6xl mx-auto p-6">
        {loading ? (
          <div className="text-sm text-muted-foreground">Loading product…</div>
        ) : !product ? (
          <div className="text-center text-muted-foreground">
            Product not found
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Image */}
            <div className="h-80 bg-gray-200 flex items-center justify-center text-gray-500 text-sm">
              Image not found
            </div>

            {/* Info */}
            <div className="space-y-4">
              <h1 className="text-2xl font-semibold">{product.name}</h1>

              <div className="text-[#ee4d2d] text-xl font-bold">
                ${product.price.toFixed(2)}
              </div>

              <div className="text-sm text-gray-600">
                Category:{" "}
                <span className="font-medium text-gray-900">
                  {product.category?.categoryName}
                </span>
              </div>

              {/* Shopee-style quantity */}
              <div className="flex items-center gap-4 text-sm">
                <span className="text-gray-600">Quantity</span>

                {product.quantity === 0 ? (
                  <span className="text-red-500 font-medium">Out of Stock</span>
                ) : (
                  <>
                    <div className="flex items-center border">
                      <button
                        className="w-8 h-8 flex items-center justify-center disabled:opacity-40"
                        disabled={buyQty === 1}
                        onClick={() => setBuyQty((q) => Math.max(1, q - 1))}
                      >
                        −
                      </button>

                      <div className="w-12 h-8 flex items-center justify-center border-x">
                        {buyQty}
                      </div>

                      <button
                        className="w-8 h-8 flex items-center justify-center disabled:opacity-40"
                        disabled={buyQty === product.quantity}
                        onClick={() =>
                          setBuyQty((q) => Math.min(product.quantity, q + 1))
                        }
                      >
                        +
                      </button>
                    </div>

                    <span className="text-gray-500">
                      {product.quantity} available
                    </span>
                  </>
                )}
              </div>

              {/* Add to cart */}
              <button
                className="mt-4 bg-[#ee4d2d] text-white px-6 py-2 hover:opacity-90 disabled:opacity-50"
                disabled={product.quantity === 0}
                onClick={handleAddToCart}
              >
                {product.quantity === 0 ? "Out of Stock" : "Add to Cart"}
              </button>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
