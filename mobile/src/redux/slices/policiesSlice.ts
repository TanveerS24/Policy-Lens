import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { Policy } from "../../types";
import { fetchPolicies } from "../../services/policyService";

interface PoliciesState {
  items: Policy[];
  loading: boolean;
  error: string | null;
}

const initialState: PoliciesState = {
  items: [],
  loading: false,
  error: null,
};

export const loadPolicies = createAsyncThunk("policies/load", async () => {
  return fetchPolicies();
});

const policiesSlice = createSlice({
  name: "policies",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadPolicies.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadPolicies.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(loadPolicies.rejected, (state) => {
        state.loading = false;
        state.error = "Unable to load policies";
      });
  },
});

export default policiesSlice.reducer;
