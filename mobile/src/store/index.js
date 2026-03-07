import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import policiesReducer from './policiesSlice';
import uploadsReducer from './uploadsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    policies: policiesReducer,
    uploads: uploadsReducer,
  },
});

export default store;
