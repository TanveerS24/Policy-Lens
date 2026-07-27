import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Platform } from 'react-native';
import { api } from '../../services/api';

export interface Document {
  id: number;
  filename: string;
  file_size: number;
  mime_type: string;
  status: string;
  uploaded_at: string;
  processed_at?: string;
  summary_generated: boolean;
  publish_status?: string;
  publish_requested?: boolean;
  eligibility_criteria?: string;
  ai_summary?: {
    coverage_summary?: string;
    exclusions?: string;
    waiting_period?: string;
    claims_process?: string;
    renewal_conditions?: string;
    eligibility_criteria?: string;
    coverage_details?: any;
    exclusions_list?: string[];
    confidence_score?: number;
  };
}

interface DocumentsState {
  documents: Document[];
  currentDocument: Document | null;
  isUploading: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: DocumentsState = {
  documents: [],
  currentDocument: null,
  isUploading: false,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchDocuments = createAsyncThunk(
  'documents/fetchDocuments',
  async () => {
    const response = await api.get('/documents');
    return response.data.documents;
  }
);

export const fetchDocumentById = createAsyncThunk(
  'documents/fetchDocumentById',
  async (id: number) => {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  }
);

export const uploadDocument = createAsyncThunk(
  'documents/uploadDocument',
  async (file: { uri: string; name: string; type: string; fileObj?: any }) => {
    const formData = new FormData();
    
    if (Platform.OS === 'web') {
      if (file.fileObj) {
        formData.append('file', file.fileObj, file.name || 'document.pdf');
      } else if (file.uri && (file.uri.startsWith('blob:') || file.uri.startsWith('data:'))) {
        const blobResp = await fetch(file.uri);
        const blob = await blobResp.blob();
        formData.append('file', blob, file.name || 'document.pdf');
      } else {
        formData.append('file', {
          uri: file.uri,
          name: file.name || 'document.pdf',
          type: file.type || 'application/pdf',
        } as any);
      }
    } else {
      formData.append('file', {
        uri: file.uri,
        name: file.name || 'document.pdf',
        type: file.type || 'application/pdf',
      } as any);
    }
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }
);

export const deleteDocument = createAsyncThunk(
  'documents/deleteDocument',
  async (id: number) => {
    await api.delete(`/documents/${id}`);
    return id;
  }
);

export const fetchAISummary = createAsyncThunk(
  'documents/fetchAISummary',
  async (documentId: number) => {
    const response = await api.get(`/documents/${documentId}/summary`);
    return { documentId, summary: response.data };
  }
);

export const requestPublishDocument = createAsyncThunk(
  'documents/requestPublishDocument',
  async (documentId: number) => {
    const response = await api.post(`/documents/${documentId}/request-publish`);
    return { documentId, publishStatus: response.data.publish_status };
  }
);

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch documents
    builder.addCase(fetchDocuments.pending, (state) => {
      state.isLoading = true;
    });
    builder.addCase(fetchDocuments.fulfilled, (state, action) => {
      state.isLoading = false;
      state.documents = action.payload;
    });
    builder.addCase(fetchDocuments.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.error.message || 'Failed to fetch documents';
    });
    
    // Upload
    builder.addCase(uploadDocument.pending, (state) => {
      state.isUploading = true;
    });
    builder.addCase(uploadDocument.fulfilled, (state, action) => {
      state.isUploading = false;
      state.documents.unshift(action.payload);
    });
    builder.addCase(uploadDocument.rejected, (state, action) => {
      state.isUploading = false;
      state.error = action.error.message || 'Upload failed';
    });
    
    // Delete
    builder.addCase(deleteDocument.fulfilled, (state, action) => {
      state.documents = state.documents.filter(d => d.id !== action.payload);
    });
    
    // AI Summary
    builder.addCase(fetchAISummary.fulfilled, (state, action) => {
      const doc = state.documents.find(d => d.id === action.payload.documentId);
      if (doc) {
        doc.ai_summary = action.payload.summary;
        doc.summary_generated = true;
      }
    });

    // Request Publish
    builder.addCase(requestPublishDocument.fulfilled, (state, action) => {
      const doc = state.documents.find(d => d.id === action.payload.documentId);
      if (doc) {
        doc.publish_status = action.payload.publishStatus || 'pending_review';
        doc.publish_requested = true;
      }
    });
  },
});

export const { clearError, clearCurrentDocument } = documentsSlice.actions;
export default documentsSlice.reducer;
