import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import api, { setAuthToken } from "../services/api";

interface AuthContextType {
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  refreshAccessToken: () => Promise<string>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("admin_token"));
  const [refreshToken, setRefreshToken] = useState<string | null>(localStorage.getItem("admin_refresh_token"));

  useEffect(() => {
    const stored = localStorage.getItem("admin_token");
    const storedRefresh = localStorage.getItem("admin_refresh_token");
    if (stored) {
      setToken(stored);
      setAuthToken(stored);
    }
    if (storedRefresh) {
      setRefreshToken(storedRefresh);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const res = await api.post("/auth/login", { email, password });
    const newToken = res.data.access_token;
    const newRefreshToken = res.data.refresh_token;
    localStorage.setItem("admin_token", newToken);
    localStorage.setItem("admin_refresh_token", newRefreshToken);
    setToken(newToken);
    setRefreshToken(newRefreshToken);
    setAuthToken(newToken);
  };

  const register = async (email: string, password: string, fullName: string) => {
    const res = await api.post("/auth/register", { email, password, full_name: fullName });
    const newToken = res.data.access_token;
    const newRefreshToken = res.data.refresh_token;
    localStorage.setItem("admin_token", newToken);
    localStorage.setItem("admin_refresh_token", newRefreshToken);
    setToken(newToken);
    setRefreshToken(newRefreshToken);
    setAuthToken(newToken);
  };

  const refreshAccessToken = async () => {
    const storedRefresh = localStorage.getItem("admin_refresh_token");
    if (!storedRefresh) throw new Error("No refresh token");
    
    const res = await api.post("/auth/refresh", { refresh_token: storedRefresh });
    const newToken = res.data.access_token;
    const newRefreshToken = res.data.refresh_token;
    localStorage.setItem("admin_token", newToken);
    localStorage.setItem("admin_refresh_token", newRefreshToken);
    setToken(newToken);
    setRefreshToken(newRefreshToken);
    setAuthToken(newToken);
    return newToken;
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    localStorage.removeItem("admin_refresh_token");
    setToken(null);
    setRefreshToken(null);
    setAuthToken("");
  };

  return (
    <AuthContext.Provider value={{ token, refreshToken, isAuthenticated: !!token, login, register, refreshAccessToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
