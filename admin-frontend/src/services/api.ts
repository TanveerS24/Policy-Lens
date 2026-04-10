import axios from "axios";

const base = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

const api = axios.create({
  baseURL: base,
  headers: {
    "Content-Type": "application/json",
  },
});

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
