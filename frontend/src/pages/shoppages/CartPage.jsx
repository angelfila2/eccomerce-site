import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import {
  getCart,
  removeCartItem,
  updateCartItem,
  checkout,
  clearCart,
} from "../../api/cartApi";

import { useNotification } from "../../context/NotificationContext";

export default function CartPage() {
  const { show } = useNotification();
  const navigate = useNavigate();

  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedItems, setSelectedItems] = useState(new Set());

  // ⭐ NEW: store original max quantities
  const [initialQuantities, setInitialQuantities] = useState({});

  async function loadCart() {
    try {
      const res = await getCart();
      setCart(res.data);

      // capture original quantities ONCE
      setInitialQuantities((prev) => {
        if (Object.keys(prev).length > 0) return prev;

        const map = {};
        res.data.items.forEach((item) => {
          map[item.product.productId] = item.quantity;
        });
        return map;
      });
    } catch (err) {
      if (err.response?.status === 401) {
        show("Please login to perform this action", "info");
        return;
      }

      show("Failed to load cart", "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCart();
  }, []);

  function toggleItem(productId) {
    setSelectedItems((prev) => {
      const next = new Set(prev);
      next.has(productId) ? next.delete(productId) : next.add(productId);
      return next;
    });
  }

  async function handleUpdateQuantity(productId, quantity) {
    if (quantity < 1) return;

    try {
      await updateCartItem(productId, quantity);
      loadCart();
    } catch {
      show("Failed to update quantity", "error");
    }
  }

  async function handleRemove(productId) {
    try {
      await removeCartItem(productId);
      loadCart();
    } catch {
      show("Failed to remove item", "error");
    }
  }

  async function handleClearCart() {
    try {
      await clearCart();
      setSelectedItems(new Set());
      setInitialQuantities({});
      loadCart();
      show("Cart cleared", "success");
    } catch {
      show("Failed to clear cart", "error");
    }
  }

  function calculateTotal() {
    if (!cart) return 0;

    return cart.items
      .filter((i) => selectedItems.has(i.product.productId))
      .reduce((sum, i) => sum + i.product.price * i.quantity, 0);
  }

  async function handleCheckout() {
    if (selectedItems.size === 0) {
      show("Select items to checkout", "warning");
      return;
    }

    try {
      const res = await checkout();
      navigate(`/orders/${res.data.id}`);
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        "Checkout failed. Please try again. :" + err;
      show(msg, "error");
    }
  }

  if (loading) {
    return <div className="p-6">Loading…</div>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <main className="max-w-6xl mx-auto p-6">
        <div className="p-6">
          Your cart is empty. Checkout our catalogue{" "}
          <Link className="font-bold underline hover:bg-orange-400" to="/">
            here
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-6xl mx-auto p-6">
      <h1 className="text-xl font-semibold mb-6">Shopping Cart</h1>

      <div className="space-y-4">
        {cart.items.map((item) => {
          const productId = item.product.productId;
          const maxQty = initialQuantities[productId];

          return (
            <div key={productId} className="flex items-center gap-4 border p-4">
              {/* Select */}
              <input
                type="checkbox"
                checked={selectedItems.has(productId)}
                onChange={() => toggleItem(productId)}
              />

              {/* Info */}
              <div className="flex-1">
                <div className="font-medium">{item.product.name}</div>
                <div className="text-sm text-gray-600">
                  ${item.product.price.toFixed(2)}
                </div>
              </div>

              {/* Quantity (cart-capped) */}
              <div className="flex items-center border">
                <button
                  className="w-8 h-8 flex items-center justify-center disabled:opacity-40"
                  disabled={item.quantity === 1}
                  onClick={() =>
                    handleUpdateQuantity(productId, item.quantity - 1)
                  }
                >
                  −
                </button>

                <div className="px-3 text-sm border-x">
                  {item.quantity} | {maxQty}
                </div>

                <button
                  className="w-8 h-8 flex items-center justify-center disabled:opacity-40"
                  disabled={item.quantity >= maxQty}
                  onClick={() =>
                    handleUpdateQuantity(productId, item.quantity + 1)
                  }
                >
                  +
                </button>
              </div>

              {/* Remove */}
              <button
                className="text-red-600 text-sm"
                onClick={() => handleRemove(productId)}
              >
                Remove
              </button>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div className="mt-6 flex justify-between items-center">
        <button
          className="text-sm text-red-600 disabled:opacity-40"
          onClick={handleClearCart}
        >
          Clear Cart
        </button>

        <div className="text-right">
          <div className="text-lg font-semibold">
            Total: ${calculateTotal().toFixed(2)}
          </div>

          <button
            className="mt-2 bg-[#ee4d2d] text-white px-6 py-2 disabled:opacity-50"
            disabled={selectedItems.size === 0}
            onClick={handleCheckout}
          >
            Checkout
          </button>
        </div>
      </div>
    </main>
  );
}
