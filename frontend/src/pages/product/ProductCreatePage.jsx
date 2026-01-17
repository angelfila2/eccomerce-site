import { useEffect, useState } from "react";
import { getCategories } from "../../api/categoryApi";
import { createProduct } from "../../api/productApi";
import { useNotification } from "../../context/NotificationContext";

export default function ProductCreatePage() {
  const { show } = useNotification();

  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    name: "",
    price: "",
    quantity: "",
    categoryId: "",
  });

  // Load categories for dropdown
  async function loadCategories() {
    try {
      const res = await getCategories();
      setCategories(res.data);
    } catch (err) {
      show("Failed to load categories: " + err, "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCategories();
  }, []);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !form.name.trim() ||
      !form.price ||
      !form.quantity ||
      !form.categoryId
    ) {
      show("Please fill in all fields", "error");
      return;
    }

    try {
      await createProduct({
        name:
          form.name.charAt(0).toUpperCase() + form.name.slice(1).toLowerCase(),
        price: form.price,
        quantity: form.quantity,
        categoryId: form.categoryId,
      });

      show("Product created successfully", "success");

      setForm({
        name: "",
        price: "",
        quantity: "",
        categoryId: "",
      });
    } catch (err) {
      show("Failed to create product: " + err, "error");
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-xl font-semibold mb-4">Create Product</h1>

      {loading ? (
        <div className="text-sm text-muted-foreground">Loading categories…</div>
      ) : (
        <form
          onSubmit={handleSubmit}
          className="space-y-4 border border-border p-6"
        >
          <input
            type="text"
            className="w-full border border-border px-3 py-2"
            placeholder="Product name"
            value={form.name}
            onChange={(e) => updateField("name", e.target.value)}
          />

          <input
            type="number"
            step="0.01"
            className="w-full border border-border px-3 py-2"
            placeholder="Price"
            value={form.price}
            onChange={(e) => updateField("price", e.target.value)}
          />

          <input
            type="number"
            min="0"
            className="w-full border border-border px-3 py-2"
            placeholder="Quantity"
            value={form.quantity}
            onChange={(e) => updateField("quantity", e.target.value)}
          />

          <select
            className="w-full border border-border px-3 py-2 bg-background"
            value={form.categoryId}
            onChange={(e) => updateField("categoryId", e.target.value)}
          >
            <option value="">Select category</option>
            {categories.map((cat) => (
              <option key={cat.categoryId} value={cat.categoryId}>
                {cat.categoryName}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-primary text-primary-foreground px-6 py-2 hover:opacity-90"
          >
            Create Product
          </button>
        </form>
      )}
    </div>
  );
}
