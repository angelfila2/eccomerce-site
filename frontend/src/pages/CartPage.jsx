import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const CART_ID = 1; // hardcoded for now

export default function CartPage() {
  const [cart, setCart] = useState(null);
  const navigate = useNavigate();

  /* =========================
     Fetch cart
     ========================= */
  const fetchCart = () => {
    fetch(`http://localhost:8080/v1/cart?cartId=${CART_ID}`)
      .then((res) => res.json())
      .then(setCart)
      .catch(console.error);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  /* =========================
     Update quantity
     ========================= */
  const updateQuantity = (productId, quantity) => {
    if (quantity < 1) return;

    fetch(
      `http://localhost:8080/v1/cart/items` +
        `?cartId=${CART_ID}` +
        `&productId=${productId}` +
        `&quantity=${quantity}`,
      { method: "PUT" }
    ).then(fetchCart);
  };

  /* =========================
     Remove item
     ========================= */
  const removeItem = (productId) => {
    fetch(
      `http://localhost:8080/v1/cart/${CART_ID}/items?productId=${productId}`,
      { method: "DELETE" }
    ).then(fetchCart);
  };

  /* =========================
     Checkout
     ========================= */
  const checkout = () => {
    fetch(`http://localhost:8080/v1/cart/${CART_ID}/checkout`, {
      method: "POST",
    }).then(() => {
      alert("Checkout successful ✅");
      fetchCart();
    });
  };

  if (!cart) return <p>Loading cart...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <button onClick={() => navigate(-1)}>⬅ Back</button>

      <h1>Cart</h1>
      <p>Status: {cart.status}</p>

      {cart.items.length === 0 && <p>Your cart is empty.</p>}

      <ul>
        {cart.items.map((item) => (
          <li key={item.product.id} style={{ marginBottom: "12px" }}>
            <div>
              <strong>{item.product.name}</strong>
            </div>

            <div>Price: ${item.product.price}</div>

            <div>
              Quantity:
              <input
                type="number"
                value={item.quantity}
                min="1"
                onChange={(e) =>
                  updateQuantity(item.product.id, Number(e.target.value))
                }
                style={{ width: "60px", marginLeft: "8px" }}
              />
            </div>

            <button onClick={() => removeItem(item.product.id)}>Remove</button>
          </li>
        ))}
      </ul>

      {cart.items.length > 0 && cart.status === "ACTIVE" && (
        <button onClick={checkout}>Checkout</button>
      )}
    </div>
  );
}
