import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../services/api';

export interface Scheme {
  id: number;
  name: string;
  code: string;
  type: string;
  ministry?: string;
  state?: string;
  description: string;
  short_description?: string;
  target_categories: string[];
  target_states: string[];
  coverage_amount?: number;
  services_covered: string[];
  min_age?: number;
  max_age?: number;
  income_criteria?: string;
  required_documents: string[];
  website?: string;
  helpline?: string;
  application_process?: string;
  processing_time?: string;
  is_bookmarked: boolean;
  has_original_document?: boolean;
  full_document_text?: string;
}

export interface EligibilityResult {
  scheme_id: number;
  scheme_name: string;
  result: string;
  confidence_score: number;
  matched_conditions: string[];
  failed_conditions: string[];
  missing_conditions: string[];
  explanation: string;
  required_documents?: string[];
  coverage_amount?: number;
  services_covered?: string[];
  application_process?: string;
  helpline?: string;
  website?: string;
}

interface SchemesState {
  schemes: Scheme[];
  currentScheme: Scheme | null;
  bookmarks: Scheme[];
  isLoading: boolean;
  error: string | null;
  eligibilityResult: EligibilityResult | null;
  eligibilityLoading: boolean;
  pagination: {
    page: number;
    perPage: number;
    total: number;
    totalPages: number;
  };
}

const initialState: SchemesState = {
  schemes: [],
  currentScheme: null,
  bookmarks: [],
  isLoading: false,
  error: null,
  eligibilityResult: null,
  eligibilityLoading: false,
  pagination: {
    page: 1,
    perPage: 20,
    total: 0,
    totalPages: 0,
  },
};

// Async thunks
export const fetchSchemes = createAsyncThunk(
  'schemes/fetchSchemes',
  async (params: { page?: number; per_page?: number; type?: string; state?: string; search?: string } = {}) => {
    const response = await api.get('/schemes', { params });
    return response.data;
  }
);

export const fetchSchemeById = createAsyncThunk(
  'schemes/fetchSchemeById',
  async (id: number) => {
    const response = await api.get(`/schemes/${id}`);
    return response.data;
  }
);

export const bookmarkScheme = createAsyncThunk(
  'schemes/bookmarkScheme',
  async (schemeId: number) => {
    await api.post('/schemes/bookmark', { scheme_id: schemeId, enable_notifications: true });
    return schemeId;
  }
);

export const removeBookmark = createAsyncThunk(
  'schemes/removeBookmark',
  async (schemeId: number) => {
    await api.delete(`/schemes/${schemeId}/bookmark`);
    return schemeId;
  }
);

export const fetchBookmarks = createAsyncThunk(
  'schemes/fetchBookmarks',
  async () => {
    const response = await api.get('/schemes/my/bookmarks');
    return response.data.bookmarks;
  }
);

export const checkEligibility = createAsyncThunk(
  'schemes/checkEligibility',
  async ({ schemeId, data }: { schemeId: number; data: any }) => {
    const response = await api.post('/eligibility/check', { scheme_id: schemeId, ...data });
    return response.data;
  }
);

const schemesSlice = createSlice({
  name: 'schemes',
  initialState,
  reducers: {
    clearCurrentScheme: (state) => {
      state.currentScheme = null;
    },
    clearError: (state) => {
      state.error = null;
    },
    clearEligibilityResult: (state) => {
      state.eligibilityResult = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch schemes
    builder.addCase(fetchSchemes.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchSchemes.fulfilled, (state, action) => {
      state.isLoading = false;
      state.schemes = action.payload.schemes;
      state.pagination = action.payload.pagination;
    });
    builder.addCase(fetchSchemes.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.error.message || 'Failed to fetch schemes';
    });
    
    // Fetch scheme by ID
    builder.addCase(fetchSchemeById.fulfilled, (state, action) => {
      state.currentScheme = action.payload;
    });
    
    // Bookmarks
    builder.addCase(fetchBookmarks.fulfilled, (state, action) => {
      state.bookmarks = action.payload.map((b: any) => b.scheme);
    });
    
    builder.addCase(bookmarkScheme.fulfilled, (state, action) => {
      const scheme = state.schemes.find(s => s.id === action.payload);
      if (scheme) {
        scheme.is_bookmarked = true;
      }
    });
    
    builder.addCase(removeBookmark.fulfilled, (state, action) => {
      const scheme = state.schemes.find(s => s.id === action.payload);
      if (scheme) {
        scheme.is_bookmarked = false;
      }
      state.bookmarks = state.bookmarks.filter(s => s.id !== action.payload);
    });

    // Check eligibility
    builder.addCase(checkEligibility.pending, (state) => {
      state.eligibilityLoading = true;
      state.eligibilityResult = null;
    });
    builder.addCase(checkEligibility.fulfilled, (state, action) => {
      state.eligibilityLoading = false;
      state.eligibilityResult = action.payload;
    });
    builder.addCase(checkEligibility.rejected, (state, action) => {
      state.eligibilityLoading = false;
      state.error = action.error.message || 'Eligibility check failed';
    });
  },
});

export const { clearCurrentScheme, clearError, clearEligibilityResult } = schemesSlice.actions;
export default schemesSlice.reducer;
