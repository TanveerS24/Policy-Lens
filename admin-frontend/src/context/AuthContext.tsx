import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import api, { setAuthToken } from "../services/api";

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("admin_token"));

  useEffect(() => {
    const stored = localStorage.getItem("admin_token");
    if (stored) {
      setToken(stored);
      setAuthToken(stored);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const res = await api.post("/auth/login", { email, password });
    const newToken = res.data.access_token;
    localStorage.setItem("admin_token", newToken);
    setToken(newToken);
    setAuthToken(newToken);
  };

  const register = async (email: string, password: string, fullName: string) => {
    const res = await api.post("/auth/register", { email, password, full_name: fullName });
    const newToken = res.data.access_token;
    localStorage.setItem("admin_token", newToken);
    setToken(newToken);
    setAuthToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    setToken(null);
    setAuthToken("");
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
