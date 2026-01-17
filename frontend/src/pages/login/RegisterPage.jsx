import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../../api/api";
import { useNotification } from "../../context/NotificationContext";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { show } = useNotification();

  const [form, setForm] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "ROLE_USER", // default, can be changed later
    agreeToTerms: false,
  });

  const [loading, setLoading] = useState(false);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    // 🔒 Validation
    if (
      !form.firstname ||
      !form.lastname ||
      !form.email ||
      !form.password ||
      !form.confirmPassword
    ) {
      show("Please fill in all fields", "error");
      return;
    }

    if (form.password !== form.confirmPassword) {
      show("Passwords do not match", "error");
      return;
    }

    if (form.password.length < 6) {
      show("Password must be at least 6 characters", "error");
      return;
    }

    if (!form.agreeToTerms) {
      show("Please agree to the terms and conditions", "error");
      return;
    }

    try {
      setLoading(true);

      await api.post("/users", {
        firstname: form.firstname,
        lastname: form.lastname,
        email: form.email,
        password: form.password,
        role: form.role,
      });

      show("User registered successfully", "success");
      navigate("/login");
    } catch (err) {
      show("Registration failed. Error:" + err, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <Link to="/" className="text-sm mb-6 inline-block hover:underline">
          ← Back
        </Link>

        <div className="bg-card border border-border p-6">
          <h1 className="text-xl font-semibold mb-1">Create Admin Account</h1>
          <p className="text-sm text-muted-foreground mb-5">
            Register a new user
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              className="w-full border border-border px-3 py-2"
              placeholder="First Name"
              value={form.firstname}
              onChange={(e) => updateField("firstname", e.target.value)}
            />

            <input
              className="w-full border border-border px-3 py-2"
              placeholder="Last Name"
              value={form.lastname}
              onChange={(e) => updateField("lastname", e.target.value)}
            />

            <input
              className="w-full border border-border px-3 py-2"
              type="email"
              placeholder="Email"
              value={form.email}
              onChange={(e) => updateField("email", e.target.value)}
            />

            <input
              className="w-full border border-border px-3 py-2"
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={(e) => updateField("password", e.target.value)}
            />

            <input
              className="w-full border border-border px-3 py-2"
              type="password"
              placeholder="Confirm Password"
              value={form.confirmPassword}
              onChange={(e) => updateField("confirmPassword", e.target.value)}
            />

            {/* Role (hidden for now, but explicit) */}
            <input type="hidden" value={form.role} />

            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={form.agreeToTerms}
                onChange={(e) => updateField("agreeToTerms", e.target.checked)}
              />
              I agree to the terms and conditions
            </label>

            <button
              disabled={loading}
              className="w-full bg-primary text-primary-foreground py-2 hover:opacity-90 disabled:opacity-60"
            >
              {loading ? "Creating user..." : "Create Account"}
            </button>

            <div className="text-center text-sm">
              Already have an account?{" "}
              <Link to="/login" className="text-primary hover:underline">
                Login
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
