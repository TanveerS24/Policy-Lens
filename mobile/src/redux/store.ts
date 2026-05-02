import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import schemesReducer from './slices/schemesSlice';
import documentsReducer from './slices/documentsSlice';
import notificationsReducer from './slices/notificationsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    schemes: schemesReducer,
    documents: documentsReducer,
    notifications: notificationsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['auth/setUser'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
