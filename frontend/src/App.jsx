import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import Notification from "./components/Notification";
import { NotificationProvider } from "./context/NotificationContext";

// Auth pages
import Login from "./pages/login/LoginPage";
import RegisterPage from "./pages/login/RegisterPage";

// Shop pages
import Home from "./pages/shoppages/Home";
import CategoryPage from "./pages/category/CategoryPage";
import ProductCreatePage from "./pages/product/ProductCreatePage";
import ProductListPage from "./pages/product/ProductListPage";
import ProductDetailPage from "./pages/shoppages/ProductDetailPage";
import CartPage from "./pages/shoppages/CartPage";
import OrderPage from "./pages/shoppages/OrderPage";
import PublicLayout from "./layouts/PublicLayout";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth (no layout) */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* App pages (with layout) */}
        <Route
          path="/"
          element={
            <MainLayout>
              <Home />
            </MainLayout>
          }
        />

        <Route
          path="/categories"
          element={
            <MainLayout>
              <CategoryPage />
            </MainLayout>
          }
        />

        <Route
          path="/products"
          element={
            <MainLayout>
              <ProductListPage />
            </MainLayout>
          }
        />

        <Route
          path="/products/create"
          element={
            <MainLayout>
              <ProductCreatePage />
            </MainLayout>
          }
        />

        <Route
          path="/products/:id"
          element={
            <MainLayout>
              <ProductDetailPage />
            </MainLayout>
          }
        />

        <Route
          path="/cart"
          element={
            <MainLayout>
              <CartPage />
            </MainLayout>
          }
        />

        <Route
          path="/orders/:id"
          element={
            <MainLayout>
              <OrderPage />
            </MainLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
