import axios from "axios";

const base = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

const api = axios.create({
  baseURL: base,
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

// Add request interceptor to attach auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("admin_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried refreshing yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Wait for the refresh to complete
        return new Promise((resolve) => {
          refreshSubscribers.push((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem("admin_refresh_token");
        if (!refreshToken) {
          // No refresh token, logout
          localStorage.removeItem("admin_token");
          localStorage.removeItem("admin_refresh_token");
          window.location.href = "/login";
          return Promise.reject(error);
        }

        const res = await api.post("/auth/refresh", { refresh_token: refreshToken });
        const newToken = res.data.access_token;
        const newRefreshToken = res.data.refresh_token;

        localStorage.setItem("admin_token", newToken);
        localStorage.setItem("admin_refresh_token", newRefreshToken);
        api.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;

        // Notify all waiting requests
        refreshSubscribers.forEach((callback) => callback(newToken));
        refreshSubscribers = [];

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout
        localStorage.removeItem("admin_token");
        localStorage.removeItem("admin_refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export function setAuthToken(token: string) {
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export async function getDashboard() {
  const res = await api.get("/admin/dashboard");
  return res.data;
}

export async function getPending() {
  const res = await api.get("/admin/pending");
  return res.data;
}

export async function uploadPdf(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/uploads/pdf", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
}

export async function getPolicies() {
  const res = await api.get("/admin/policies");
  return res.data;
}

export async function approvePolicy(id: string) {
  const res = await api.post(`/admin/approve/${id}`);
  return res.data;
}

export async function rejectPolicy(id: string) {
  const res = await api.post(`/admin/reject/${id}`);
  return res.data;
}

export default api;
