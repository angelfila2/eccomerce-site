import { useEffect, useState } from "react";
import { getCategories } from "../../api/categoryApi";
import CategoryForm from "./CategoryForm";
import CategoryTable from "./CategoryTable";

export default function CategoryPage() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadCategories() {
    try {
      const res = await getCategories();
      setCategories(res.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCategories();
  }, []);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-xl font-semibold mb-4">Category Management</h1>

      <CategoryForm onCreated={loadCategories} />

      {loading ? (
        <div className="text-sm text-muted-foreground">Loading categories…</div>
      ) : (
        <CategoryTable categories={categories} onDeleted={loadCategories} />
      )}
    </div>
  );
}
