import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UiState {
  toast: string | null;
}

const initialState: UiState = {
  toast: null,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    setToast(state, action: PayloadAction<string | null>) {
      state.toast = action.payload;
    },
  },
});

export const { setToast } = uiSlice.actions;
export default uiSlice.reducer;
