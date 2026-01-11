import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

const CART_ID = 1; // 🔒 hardcoded for now

export default function ProductPage() {
  const [products, setProducts] = useState([]);
  const [params] = useSearchParams();
  const navigate = useNavigate();

  const categoryId = params.get("categoryId");

  /* =========================
     Fetch products by category
     ========================= */
  useEffect(() => {
    if (!categoryId) return;

    fetch(`http://localhost:8080/v1/products/category/${categoryId}`)
      .then((res) => res.json())
      .then(setProducts)
      .catch(console.error);
  }, [categoryId]);

  /* =========================
     Add product to cart (cartId = 1)
     ========================= */
  const addToCart = (productId) => {
    fetch(
      `http://localhost:8080/v1/cart/items` +
        `?cartId=${CART_ID}` +
        `&productId=${productId}` +
        `&quantity=1`,
      { method: "POST" }
    )
      .then(() => {
        alert("Added to cart 🛒");
      })
      .catch(console.error);
  };

  return (
    <div style={{ padding: "20px" }}>
      <button onClick={() => navigate(-1)}>⬅ Back</button>

      <h1>Products</h1>

      {products.length === 0 && <p>No products found.</p>}

      <ul>
        {products.map((p) => (
          <li key={p.productId} style={{ marginBottom: "12px" }}>
            <div>
              <strong>{p.name}</strong>
            </div>

            <div>
              ${p.price} | stock: {p.quantity} | category:{" "}
              {p.category?.categoryName}
            </div>

            <button onClick={() => addToCart(p.productId)}>Add to Cart</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
