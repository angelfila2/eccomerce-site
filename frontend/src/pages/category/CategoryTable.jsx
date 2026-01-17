import { deleteCategory } from "../../api/categoryApi";
import { useNotification } from "../../context/NotificationContext";

export default function CategoryTable({ categories, onDeleted }) {
  const { show } = useNotification();

  async function handleDelete(id) {
    const confirmed = window.confirm("Delete this category?");
    if (!confirmed) return;

    try {
      await deleteCategory(id);
      show("Category deleted", "success");
      onDeleted();
    } catch (err) {
      show("Failed to delete category", "error");
    }
  }

  return (
    <table className="w-full border border-border text-sm">
      <thead className="bg-muted">
        <tr>
          <th className="p-3 text-left">ID</th>
          <th className="p-3 text-left">Name</th>
          <th className="p-3 text-left">Actions</th>
        </tr>
      </thead>

      <tbody>
        {categories.map((cat) => (
          <tr key={cat.categoryId} className="border-t">
            <td className="p-3">{cat.categoryId}</td>
            <td className="p-3">{cat.categoryName}</td>
            <td className="p-3">
              <button
                onClick={() => handleDelete(cat.categoryId)}
                className="text-red-600 hover:underline"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}

        {categories.length === 0 && (
          <tr>
            <td colSpan="3" className="p-4 text-center text-muted-foreground">
              No categories found
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}
