import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./slices/authSlice";
import uiReducer from "./slices/uiSlice";
import policiesReducer from "./slices/policiesSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    policies: policiesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
