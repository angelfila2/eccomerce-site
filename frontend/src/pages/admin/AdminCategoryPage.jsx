import { useEffect, useState } from "react";

export default function AdminCategoryPage() {
  const [categories, setCategories] = useState([]);
  const [name, setName] = useState("");

  const fetchCategories = () => {
    fetch("http://localhost:8080/v1/category")
      .then((res) => res.json())
      .then(setCategories);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const addCategory = () => {
    if (!name.trim()) return;

    fetch(
      `http://localhost:8080/v1/category?name=${encodeURIComponent(name)}`,
      { method: "POST" }
    ).then(() => {
      setName("");
      fetchCategories();
    });
  };

  const deleteCategory = (id) => {
    fetch(`http://localhost:8080/v1/category/${id}`, {
      method: "DELETE",
    }).then(fetchCategories);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin – Categories</h1>

      <input
        placeholder="Category name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={addCategory}>Add</button>

      <ul>
        {categories.map((c) => (
          <li key={c.categoryId}>
            {c.categoryName}
            <button onClick={() => deleteCategory(c.categoryId)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
