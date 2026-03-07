import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { API_URL } from '../config/api';

// Thunks
export const fetchPolicies = createAsyncThunk(
  'policies/fetchPolicies',
  async (filters, { getState }) => {
    const { auth } = getState();
    const response = await axios.get(`${API_URL}/policies`, {
      params: filters,
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    });
    return response.data;
  }
);

export const fetchPolicyDetail = createAsyncThunk(
  'policies/fetchDetail',
  async (policyId, { getState }) => {
    const { auth } = getState();
    const response = await axios.get(`${API_URL}/policies/${policyId}`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    });
    return response.data;
  }
);

export const checkEligibility = createAsyncThunk(
  'policies/checkEligibility',
  async (payload, { getState }) => {
    const { auth } = getState();
    const response = await axios.post(
      `${API_URL}/policies/check-eligibility/me`,
      payload,
      {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      }
    );
    return response.data;
  }
);

export const askQuestion = createAsyncThunk(
  'policies/askQuestion',
  async (payload, { getState }) => {
    const { auth } = getState();
    const response = await axios.post(`${API_URL}/policies/ask`, payload, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    });
    return response.data;
  }
);

// Slice
const policiesSlice = createSlice({
  name: 'policies',
  initialState: {
    list: [],
    selectedPolicy: null,
    eligibilityResult: null,
    question: null,
    answer: null,
    loading: false,
    error: null,
  },
  reducers: {
    clearEligibilityResult: (state) => {
      state.eligibilityResult = null;
    },
    clearAnswer: (state) => {
      state.answer = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch Policies
    builder
      .addCase(fetchPolicies.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPolicies.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload.policies;
      })
      .addCase(fetchPolicies.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Fetch Policy Detail
    builder
      .addCase(fetchPolicyDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPolicyDetail.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedPolicy = action.payload;
      })
      .addCase(fetchPolicyDetail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Check Eligibility
    builder
      .addCase(checkEligibility.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(checkEligibility.fulfilled, (state, action) => {
        state.loading = false;
        state.eligibilityResult = action.payload;
      })
      .addCase(checkEligibility.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Ask Question
    builder
      .addCase(askQuestion.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(askQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.question = action.payload.question;
        state.answer = action.payload.answer;
      })
      .addCase(askQuestion.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const { clearEligibilityResult, clearAnswer } = policiesSlice.actions;
export default policiesSlice.reducer;
