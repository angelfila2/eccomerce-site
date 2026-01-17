import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../api/api";
import { useNotification } from "../../context/NotificationContext";
import Notification from "../../components/Notification";

export default function Login() {
  const navigate = useNavigate();

  // ✅ call hook ONCE, inside component
  const { show, notification } = useNotification();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!email || !password) {
      show("Please fill in all fields", "error");
      return;
    }

    try {
      setLoading(true);

      const res = await api.post("/auth/login", { email, password });
      api.accessToken = res.data.accessToken;

      show("Login successful", "success");
      navigate("/");
    } catch {
      show("Invalid credentials", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#ee4d2d] to-[#ff7337] px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Login to ShopMart
          </h1>

          {/* 🔔 INLINE notification inside card */}
          {notification && (
            <div className="mb-4">
              <Notification notification={notification} />
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#ee4d2d]"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#ee4d2d]"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              disabled={loading}
              className="w-full bg-[#ee4d2d] hover:bg-[#e04325] text-white py-3 rounded font-medium transition"
            >
              {loading ? "Signing in..." : "Login"}
            </button>
          </form>

          <div className="text-center text-sm text-gray-600 mt-4">
            Don&apos;t have an account?{" "}
            <Link
              to="/register"
              className="text-[#ee4d2d] font-medium hover:underline"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
