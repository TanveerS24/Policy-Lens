import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_URL } from '../config/api';

// Initial state
const initialState = {
  accessToken: null,
  refreshToken: null,
  user: null,
  role: null,
  loading: false,
  error: null,
};

// Thunks
export const register = createAsyncThunk(
  'auth/register',
  async (userData) => {
    const response = await axios.post(`${API_URL}/auth/register`, userData);
    return response.data;
  }
);

export const verifyOTP = createAsyncThunk(
  'auth/verifyOTP',
  async (otpData) => {
    const response = await axios.post(`${API_URL}/auth/verify-otp`, otpData);
    return response.data;
  }
);

export const login = createAsyncThunk(
  'auth/login',
  async (credentials) => {
    const response = await axios.post(`${API_URL}/auth/login`, credentials);
    return response.data;
  }
);

export const refreshAccessToken = createAsyncThunk(
  'auth/refreshToken',
  async (refreshToken) => {
    const response = await axios.post(`${API_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });
    return response.data;
  }
);

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      state.role = null;
      AsyncStorage.removeItem('accessToken');
      AsyncStorage.removeItem('refreshToken');
    },
    restoreToken: (state, action) => {
      state.accessToken = action.payload.accessToken;
      state.refreshToken = action.payload.refreshToken;
      state.user = action.payload.user;
      state.role = action.payload.role;
    },
  },
  extraReducers: (builder) => {
    // Register
    builder
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Verify OTP
    builder
      .addCase(verifyOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyOTP.fulfilled, (state, action) => {
        state.loading = false;
        state.accessToken = action.payload.access_token;
        state.refreshToken = action.payload.refresh_token;
        state.user = action.payload.email;
        state.role = action.payload.role;
        AsyncStorage.setItem('accessToken', action.payload.access_token);
        AsyncStorage.setItem('refreshToken', action.payload.refresh_token);
      })
      .addCase(verifyOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Login
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.accessToken = action.payload.access_token;
        state.refreshToken = action.payload.refresh_token;
        state.user = action.payload.email;
        state.role = action.payload.role;
        AsyncStorage.setItem('accessToken', action.payload.access_token);
        AsyncStorage.setItem('refreshToken', action.payload.refresh_token);
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Refresh Token
    builder
      .addCase(refreshAccessToken.fulfilled, (state, action) => {
        state.accessToken = action.payload.access_token;
        state.refreshToken = action.payload.refresh_token;
        AsyncStorage.setItem('accessToken', action.payload.access_token);
        AsyncStorage.setItem('refreshToken', action.payload.refresh_token);
      })
      .addCase(refreshAccessToken.rejected, (state) => {
        state.accessToken = null;
        state.refreshToken = null;
        state.user = null;
        state.role = null;
        AsyncStorage.removeItem('accessToken');
        AsyncStorage.removeItem('refreshToken');
      });
  },
});

export const { logout, restoreToken } = authSlice.actions;
export default authSlice.reducer;
