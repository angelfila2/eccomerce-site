import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080",
  withCredentials: true, // send httpOnly refresh token cookie
});

// =====================
// In-memory access token
// =====================
api.accessToken = null;

// =====================
// REQUEST INTERCEPTOR
// =====================
api.interceptors.request.use(
  (config) => {
    if (api.accessToken) {
      config.headers.Authorization = `Bearer ${api.accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// =====================
// RESPONSE INTERCEPTOR
// =====================
let isRefreshing = false;
let queue = [];

function flushQueue(error, token = null) {
  queue.forEach((p) => (error ? p.reject(error) : p.resolve(token)));
  queue = [];
}

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    const status = err.response?.status;
    const url = original?.url || "";

    // ===============================
    // 🚫 NEVER intercept auth endpoints
    // ===============================
    if (
      url.includes("/auth/login") ||
      url.includes("/auth/register") ||
      url.includes("/auth/refresh")
    ) {
      return Promise.reject(err);
    }

    // ===============================
    // Only handle real 401s once
    // ===============================
    if (status !== 401 || original._retry) {
      return Promise.reject(err);
    }

    original._retry = true;

    // ===============================
    // Queue requests while refreshing
    // ===============================
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject });
      }).then((token) => {
        original.headers.Authorization = `Bearer ${token}`;
        return api(original);
      });
    }

    isRefreshing = true;

    try {
      // ===============================
      // Attempt token refresh
      // ===============================
      const res = await axios.post(
        "http://localhost:8080/auth/refresh",
        {},
        { withCredentials: true }
      );

      api.accessToken = res.data.accessToken;
      flushQueue(null, api.accessToken);

      original.headers.Authorization = `Bearer ${api.accessToken}`;
      return api(original);
    } catch (refreshError) {
      flushQueue(refreshError);

      // ===============================
      // 🔔 Notify user
      // ===============================
      window.dispatchEvent(
        new CustomEvent("notify", {
          detail: {
            message: "Please log in to proceed",
            type: "info",
          },
        })
      );

      // ===============================
      // 🔁 Ask React to redirect (SPA-safe)
      // ===============================
      window.dispatchEvent(new Event("auth:redirect"));

      api.accessToken = null;
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
