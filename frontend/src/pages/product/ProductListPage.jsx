import { useEffect, useState } from "react";
import { getProducts, deleteProduct } from "../../api/productApi";
import { useNotification } from "../../context/NotificationContext";

export default function ProductListPage() {
  const { show } = useNotification();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadProducts() {
    try {
      const res = await getProducts();
      setProducts(res.data);
    } catch (err) {
      show("Failed to load products", "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProducts();
  }, []);

  async function handleDelete(id) {
    const confirmed = window.confirm("Delete this product?");
    if (!confirmed) return;

    try {
      await deleteProduct(id);
      show("Product deleted", "success");
      loadProducts();
    } catch (err) {
      show("Failed to delete product", "error");
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-xl font-semibold mb-4">Product Management</h1>

      {loading ? (
        <div className="text-sm text-muted-foreground">Loading products…</div>
      ) : (
        <table className="w-full border border-border text-sm">
          <thead className="bg-muted">
            <tr>
              <th className="p-3 text-left">ID</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Category</th>
              <th className="p-3 text-left">Price</th>
              <th className="p-3 text-left">Qty</th>
              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>

          <tbody>
            {products.map((product) => (
              <tr key={product.productId} className="border-t">
                <td className="p-3">{product.productId}</td>
                <td className="p-3">{product.name}</td>
                <td className="p-3">{product.category?.categoryName ?? "-"}</td>
                <td className="p-3">${product.price}</td>
                <td className="p-3">{product.quantity}</td>
                <td className="p-3">
                  <button
                    onClick={() => handleDelete(product.productId)}
                    className="text-red-600 hover:underline"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}

            {products.length === 0 && (
              <tr>
                <td
                  colSpan="6"
                  className="p-4 text-center text-muted-foreground"
                >
                  No products found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
