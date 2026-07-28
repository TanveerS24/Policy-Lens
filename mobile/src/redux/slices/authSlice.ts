import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../services/api';
import { storage } from '../../services/storage';

interface User {
  id: number;
  name: string;
  mobile: string;
  email?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

// Async thunks
export const login = createAsyncThunk(
  'auth/login',
  async ({ mobileOrEmail, password }: { mobileOrEmail: string; password: string }) => {
    const response = await api.post('/auth/login', {
      mobile_or_email: mobileOrEmail,
      password,
    });
    
    // Save tokens securely
    await storage.setItemAsync('accessToken', response.data.access_token);
    await storage.setItemAsync('refreshToken', response.data.refresh_token);
    
    return response.data;
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (userData: any) => {
    // Convert date format from DD-MM-YYYY to YYYY-MM-DD for backend
    if (userData.date_of_birth) {
      const [day, month, year] = userData.date_of_birth.split('-');
      userData.date_of_birth = `${year}-${month}-${day}`;
    }
    
    const response = await api.post('/auth/register', userData);
    
    // Save tokens securely
    await storage.setItemAsync('accessToken', response.data.access_token);
    await storage.setItemAsync('refreshToken', response.data.refresh_token);
    
    return response.data;
  }
);

export const requestOTP = createAsyncThunk(
  'auth/requestOTP',
  async ({ email, mobile, purpose }: { email?: string; mobile?: string; purpose: string }, { rejectWithValue }) => {
    try {
      const payload: any = { purpose };
      if (email && email.trim()) payload.email = email.trim();
      if (mobile && mobile.trim()) payload.mobile = mobile.trim();
      const response = await api.post('/auth/request-otp', payload);
      return response.data;
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.message || 'Failed to request OTP';
      return rejectWithValue(detail);
    }
  }
);

export const verifyOTP = createAsyncThunk(
  'auth/verifyOTP',
  async ({ email, mobile, otp, purpose, userData }: { email?: string; mobile?: string; otp: string; purpose: string; userData?: any }, { rejectWithValue }) => {
    try {
      if (purpose === 'registration' && userData) {
        const backendUserData = {
          name: userData.name,
          email: (userData.email || email || '').trim() || null,
          mobile: (userData.mobile || mobile || '').trim(),
          date_of_birth: userData.dateOfBirth,
          gender: userData.gender,
          state: userData.state,
          district: userData.district,
          pin_code: userData.pinCode,
          password: userData.password,
          otp: otp
        };

        if (backendUserData.date_of_birth && backendUserData.date_of_birth.includes('-')) {
          const parts = backendUserData.date_of_birth.split('-');
          if (parts.length === 3 && parts[0].length === 2) {
            const [day, month, year] = parts;
            backendUserData.date_of_birth = `${year}-${month}-${day}`;
          }
        }

        const registerResponse = await api.post('/auth/register', backendUserData);
        await storage.setItemAsync('accessToken', registerResponse.data.access_token);
        await storage.setItemAsync('refreshToken', registerResponse.data.refresh_token);

        return { ...registerResponse.data, verified: true };
      }

      const payload: any = { otp };
      if (email && email.trim()) payload.email = email.trim();
      if (mobile && mobile.trim()) payload.mobile = mobile.trim();
      const verifyResponse = await api.post('/auth/verify-otp', payload);
      return { ...verifyResponse.data, verified: true };
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.message || 'Verification failed';
      return rejectWithValue(detail);
    }
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  await storage.deleteItemAsync('accessToken');
  await storage.deleteItemAsync('refreshToken');
});

export const loadStoredAuth = createAsyncThunk('auth/loadStored', async () => {
  try {
    const token = await storage.getItemAsync('accessToken');
    const refreshToken = await storage.getItemAsync('refreshToken');
    
    if (token) {
      // TODO: Validate token and get user info
      return { token, refreshToken };
    }
  } catch (error) {
    console.error('Error loading stored auth:', error);
  }
  
  return null;
});

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
  },
  extraReducers: (builder) => {
    // Login
    builder.addCase(login.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(login.fulfilled, (state, action) => {
      state.isLoading = false;
      state.user = action.payload.user;
      state.token = action.payload.access_token;
      state.refreshToken = action.payload.refresh_token;
      state.isAuthenticated = true;
    });
    builder.addCase(login.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.error.message || 'Login failed';
    });
    
    // Register
    builder.addCase(register.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(register.fulfilled, (state, action) => {
      state.isLoading = false;
      state.user = action.payload.user;
      state.token = action.payload.access_token;
      state.refreshToken = action.payload.refresh_token;
      state.isAuthenticated = true;
    });
    builder.addCase(register.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.error.message || 'Registration failed';
    });
    
    // Verify OTP
    builder.addCase(verifyOTP.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(verifyOTP.fulfilled, (state, action) => {
      state.isLoading = false;
      if (action.payload.access_token) {
        state.user = action.payload.user;
        state.token = action.payload.access_token;
        state.refreshToken = action.payload.refresh_token;
        state.isAuthenticated = true;
      }
    });
    builder.addCase(verifyOTP.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.error.message || 'OTP verification failed';
    });
    
    // Logout
    builder.addCase(logout.fulfilled, (state) => {
      state.user = null;
      state.token = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
    });
    
    // Load stored auth
    builder.addCase(loadStoredAuth.fulfilled, (state, action) => {
      if (action.payload) {
        state.token = action.payload.token;
        state.refreshToken = action.payload.refreshToken;
        state.isAuthenticated = true;
      }
    });
  },
});

export const { clearError, setUser } = authSlice.actions;
export default authSlice.reducer;
