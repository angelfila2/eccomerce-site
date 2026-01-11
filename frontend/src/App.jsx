import { Routes, Route } from "react-router-dom";
import CategoryPage from "./pages/CategoryPage";
import ProductPage from "./pages/ProductPage";
import AdminCategoryPage from "./pages/admin/AdminCategoryPage";
import AdminProductPage from "./pages/admin/AdminProductPage";
import CartPage from "./pages/CartPage";
function App() {
  return (
    <Routes>
      <Route path="/" element={<CategoryPage />} />
      <Route path="/products" element={<ProductPage />} />

      {/* Admin */}
      <Route path="/admin/categories" element={<AdminCategoryPage />} />
      <Route path="/admin/products" element={<AdminProductPage />} />
      <Route path="/cart" element={<CartPage />} />
    </Routes>
  );
}

export default App;
