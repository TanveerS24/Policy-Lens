// Storage utility - uses SecureStore for native, AsyncStorage for web
import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

const isWeb = Platform.OS === 'web';

const storage = {
  async getItemAsync(key: string): Promise<string | null> {
    try {
      if (isWeb) {
        return await AsyncStorage.getItem(key);
      } else {
        return await SecureStore.getItemAsync(key);
      }
    } catch (error) {
      console.error(`Error getting ${key} from storage:`, error);
      return null;
    }
  },
  
  async setItemAsync(key: string, value: string): Promise<void> {
    try {
      if (isWeb) {
        await AsyncStorage.setItem(key, value);
      } else {
        await SecureStore.setItemAsync(key, value);
      }
    } catch (error) {
      console.error(`Error setting ${key} in storage:`, error);
      throw error;
    }
  },
  
  async deleteItemAsync(key: string): Promise<void> {
    try {
      if (isWeb) {
        await AsyncStorage.removeItem(key);
      } else {
        await SecureStore.deleteItemAsync(key);
      }
    } catch (error) {
      console.error(`Error deleting ${key} from storage:`, error);
    }
  }
};

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// For development, use the machine's LAN IP so physical devices can reach the backend.
// localhost only works for web; Android emulators need 10.0.2.2; physical devices need the LAN IP.
const getDevelopmentApiUrl = (): string => {
  if (Platform.OS === 'web') {
    return 'http://localhost:8000/api/v1';
  }
  // For Expo Go on physical devices, use the machine's LAN IP
  // Current PC IP: 10.196.46.32 (Wi-Fi adapter)
  return 'http://10.196.46.32:8000/api/v1';
};

const FINAL_API_URL = __DEV__ ? getDevelopmentApiUrl() : API_BASE_URL;

export const api = axios.create({
  baseURL: FINAL_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await storage.getItemAsync('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // For multipart/form-data, let the browser/React Native set the Content-Type with boundary
      if (config.headers['Content-Type'] === 'multipart/form-data') {
        delete config.headers['Content-Type'];
      }
    } catch (error) {
      console.error('Error getting token from storage:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle token expiration
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = await storage.getItemAsync('refreshToken');
        
        if (refreshToken) {
          const response = await axios.post(`${FINAL_API_URL}/auth/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` },
          });
          
          const { access_token, refresh_token } = response.data;
          
          await storage.setItemAsync('accessToken', access_token);
          await storage.setItemAsync('refreshToken', refresh_token);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        try {
          await storage.deleteItemAsync('accessToken');
          await storage.deleteItemAsync('refreshToken');
        } catch (error) {
          console.error('Error clearing tokens from storage:', error);
        }
        // Navigate to login (handled by auth context)
      }
    }
    
    return Promise.reject(error);
  }
);
