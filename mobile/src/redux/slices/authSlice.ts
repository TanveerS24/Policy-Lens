import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AuthResponse, LoginPayload, RegisterPayload } from "../../types";
import api from "../../services/api";
import { removeTokens, storeTokens } from "../../services/tokenService";

interface AuthState {
  loading: boolean;
  error: string | null;
  user: { name: string; email: string } | null;
  tokens: AuthResponse | null;
}

const initialState: AuthState = {
  loading: false,
  error: null,
  user: null,
  tokens: null,
};

export const login = createAsyncThunk("auth/login", async (payload: LoginPayload, { rejectWithValue }) => {
  try {
    const response = await api.post<AuthResponse>("/auth/login", payload);
    await storeTokens(response.data);
    return response.data;
  } catch (error: any) {
    return rejectWithValue(error.response?.data?.detail ?? "Login failed");
  }
});

export const register = createAsyncThunk("auth/register", async (payload: RegisterPayload, { rejectWithValue }) => {
  try {
    const response = await api.post<AuthResponse>("/auth/register", payload);
    await storeTokens(response.data);
    return response.data;
  } catch (error: any) {
    return rejectWithValue(error.response?.data?.detail ?? "Registration failed");
  }
});

export const logout = createAsyncThunk("auth/logout", async () => {
  await removeTokens();
  return null;
});

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<{ name: string; email: string }>) {
      state.user = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.tokens = action.payload;
        state.user = { name: "", email: "" };
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false;
        state.tokens = action.payload;
        state.user = { name: "", email: "" };
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(logout.fulfilled, (state) => {
        state.loading = false;
        state.user = null;
        state.tokens = null;
      });
  },
});

export const { setUser } = authSlice.actions;
export default authSlice.reducer;
