import { useState } from "react";
import { createCategory } from "../../api/categoryApi";
import { useNotification } from "../../context/NotificationContext";

export default function CategoryForm({ onCreated }) {
  const [name, setName] = useState("");
  const { show } = useNotification();

  async function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim()) {
      show("Category name cannot be empty", "error");
      return;
    }

    let cname = name[0].toUpperCase() + name.slice(1).toLowerCase();

    try {
      await createCategory(cname);
      show("Category created successfully", "success");
      setName("");
      onCreated();
    } catch (err) {
      show("Failed to create category: " + err, "error");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 mb-6">
      <input
        type="text"
        className="flex-1 border border-border px-3 py-2"
        placeholder="Category name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <button
        type="submit"
        className="bg-primary text-primary-foreground px-4 hover:opacity-90"
      >
        Add
      </button>
    </form>
  );
}
