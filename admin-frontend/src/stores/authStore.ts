import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'

export interface AdminUser {
  id: number
  name: string
  email: string
  role: string
}

interface AuthState {
  token: string | null
  refreshToken: string | null
  user: AdminUser | null
  isAuthenticated: boolean
  login: (email: string, password: string, mfaCode?: string) => Promise<void>
  logout: () => void
  setAuth: (token: string, refreshToken: string, user: AdminUser) => void
  refreshAccessToken: () => Promise<boolean>
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
const REFRESH_INTERVAL = parseInt(import.meta.env.VITE_TOKEN_REFRESH_INTERVAL || '300000') // 5 minutes default

// Track refresh promise to prevent multiple simultaneous refresh attempts
let refreshPromise: Promise<boolean> | null = null

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,

      login: async (email, password, mfaCode) => {
        const response = await axios.post(`${API_URL}/admin/login`, {
          email,
          password,
          mfa_code: mfaCode,
        })

        const { access_token, refresh_token, admin, expires_in } = response.data

        set({
          token: access_token,
          refreshToken: refresh_token,
          user: admin,
          isAuthenticated: true,
        })

        // Set default auth header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

        // Store token expiry time
        const expiryTime = Date.now() + (expires_in * 1000)
        localStorage.setItem('token_expiry', expiryTime.toString())
      },

      logout: () => {
        set({
          token: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
        })
        delete axios.defaults.headers.common['Authorization']
        localStorage.removeItem('token_expiry')
        refreshPromise = null
      },

      setAuth: (token, refreshToken, user) => {
        set({
          token,
          refreshToken,
          user,
          isAuthenticated: true,
        })
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get()
        
        if (!refreshToken) {
          return false
        }

        // Return existing promise if refresh is already in progress
        if (refreshPromise) {
          return refreshPromise
        }

        refreshPromise = (async () => {
          try {
            const response = await axios.post(`${API_URL}/admin/refresh`, {
              refresh_token: refreshToken,
            })

            const { access_token, refresh_token, expires_in } = response.data

            set({
              token: access_token,
              refreshToken: refresh_token,
            })

            // Update auth header
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

            // Store new token expiry time
            const expiryTime = Date.now() + (expires_in * 1000)
            localStorage.setItem('token_expiry', expiryTime.toString())

            return true
          } catch (error) {
            // Refresh failed, logout user
            get().logout()
            return false
          } finally {
            refreshPromise = null
          }
        })()

        return refreshPromise
      },
    }),
    {
      name: 'admin-auth',
      onRehydrateStorage: () => (state) => {
        // Restore auth header on store rehydration
        if (state?.token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
        }
      },
    }
  )
)

// Axios interceptor to handle token refresh
let isRefreshing = false
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason?: unknown) => void
}> = []

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is not 401 or request is already retried, reject
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // Check if token is expired
    const tokenExpiry = localStorage.getItem('token_expiry')
    const isTokenExpired = tokenExpiry ? Date.now() > parseInt(tokenExpiry) : false

    if (!isTokenExpired && error.response?.status === 401) {
      // Token not expired but still 401 - invalid credentials
      return Promise.reject(error)
    }

    if (isRefreshing) {
      // Wait for refresh to complete
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return axios(originalRequest)
      }).catch((err) => {
        return Promise.reject(err)
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const store = useAuthStore.getState()
      const refreshed = await store.refreshAccessToken()

      if (refreshed && store.token) {
        processQueue(null, store.token)
        originalRequest.headers.Authorization = `Bearer ${store.token}`
        return axios(originalRequest)
      } else {
        processQueue(new Error('Token refresh failed'), null)
        return Promise.reject(error)
      }
    } catch (err) {
      processQueue(err, null)
      return Promise.reject(err)
    } finally {
      isRefreshing = false
    }
  }
)

// Periodic token refresh (refresh 5 minutes before expiry)
setInterval(() => {
  const tokenExpiry = localStorage.getItem('token_expiry')
  if (tokenExpiry) {
    const expiryTime = parseInt(tokenExpiry)
    const timeUntilExpiry = expiryTime - Date.now()
    
    // Refresh if token expires in less than 5 minutes
    if (timeUntilExpiry > 0 && timeUntilExpiry < 5 * 60 * 1000) {
      const store = useAuthStore.getState()
      if (store.isAuthenticated) {
        store.refreshAccessToken()
      }
    }
  }
}, REFRESH_INTERVAL)
