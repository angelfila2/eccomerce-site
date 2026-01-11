import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CategoryPage() {
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8080/v1/category")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Categories</h1>

      {categories.length === 0 && <p>Loading...</p>}

      <ul>
        {categories.map((cat) => (
          <li key={cat.categoryId}>
            <button
              onClick={() => navigate(`/products?categoryId=${cat.categoryId}`)}
            >
              {cat.categoryName}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
