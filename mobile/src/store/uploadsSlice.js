import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { API_URL } from '../config/api';

// Thunks
export const uploadPDF = createAsyncThunk(
  'uploads/uploadPDF',
  async (formData, { getState }) => {
    const { auth } = getState();
    const response = await axios.post(`${API_URL}/uploads/pdf`, formData, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
);

export const fetchMyUploads = createAsyncThunk(
  'uploads/fetchMyUploads',
  async (_, { getState }) => {
    const { auth } = getState();
    const response = await axios.get(`${API_URL}/uploads/my`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    });
    return response.data;
  }
);

export const deleteUpload = createAsyncThunk(
  'uploads/delete',
  async (uploadId, { getState }) => {
    const { auth } = getState();
    const response = await axios.delete(`${API_URL}/uploads/${uploadId}`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    });
    return response.data;
  }
);

export const publishUpload = createAsyncThunk(
  'uploads/publish',
  async ({ uploadId, publishData }, { getState }) => {
    const { auth } = getState();
    const response = await axios.post(
      `${API_URL}/uploads/${uploadId}/publish`,
      publishData,
      {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      }
    );
    return response.data;
  }
);

// Slice
const uploadsSlice = createSlice({
  name: 'uploads',
  initialState: {
    myUploads: [],
    uploadProgress: 0,
    loading: false,
    error: null,
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Upload PDF
    builder
      .addCase(uploadPDF.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.uploadProgress = 0;
      })
      .addCase(uploadPDF.fulfilled, (state, action) => {
        state.loading = false;
        state.uploadProgress = 100;
      })
      .addCase(uploadPDF.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Fetch My Uploads
    builder
      .addCase(fetchMyUploads.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMyUploads.fulfilled, (state, action) => {
        state.loading = false;
        state.myUploads = action.payload.uploads;
      })
      .addCase(fetchMyUploads.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });

    // Delete Upload
    builder
      .addCase(deleteUpload.fulfilled, (state, action) => {
        state.myUploads = state.myUploads.filter(
          (upload) => upload._id !== action.meta.arg
        );
      });

    // Publish Upload
    builder
      .addCase(publishUpload.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(publishUpload.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(publishUpload.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const { clearError } = uploadsSlice.actions;
export default uploadsSlice.reducer;
