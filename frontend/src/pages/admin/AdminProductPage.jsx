import { useEffect, useState } from "react";

export default function AdminProductPage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [categoryId, setCategoryId] = useState("");

  // ===== FETCH =====
  const fetchProducts = () => {
    fetch("http://localhost:8080/v1/products")
      .then((res) => res.json())
      .then(setProducts)
      .catch(console.error);
  };

  const fetchCategories = () => {
    fetch("http://localhost:8080/v1/category")
      .then((res) => res.json())
      .then(setCategories)
      .catch(console.error);
  };

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  // ===== CREATE =====
  const addProduct = () => {
    if (!name || !price || !quantity || !categoryId) return;

    const url =
      `http://localhost:8080/v1/products` +
      `?name=${encodeURIComponent(name)}` +
      `&price=${price}` +
      `&quantity=${quantity}` +
      `&categoryId=${categoryId}`;

    fetch(url, { method: "POST" })
      .then(() => {
        setName("");
        setPrice("");
        setQuantity("");
        setCategoryId("");
        fetchProducts();
      })
      .catch(console.error);
  };

  // ===== DELETE =====
  const deleteProduct = (id) => {
    fetch(`http://localhost:8080/v1/products/${id}`, {
      method: "DELETE",
    }).then(fetchProducts);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin – Products</h1>

      {/* CREATE PRODUCT */}
      <div style={{ marginBottom: "20px" }}>
        <input
          placeholder="Product name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />

        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
        >
          <option value="">Select category</option>
          {categories.map((c) => (
            <option key={c.categoryId} value={c.categoryId}>
              {c.categoryName}
            </option>
          ))}
        </select>

        <button onClick={addProduct}>Add Product</button>
      </div>

      {/* PRODUCT LIST */}
      <ul>
        {products.map((p) => (
          <li key={p.productId}>
            <strong>{p.name}</strong> — ${p.price} | qty: {p.quantity}
            <button onClick={() => deleteProduct(p.productId)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
