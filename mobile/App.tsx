import "react-native-url-polyfill/auto";
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { Provider, useSelector } from "react-redux";

import { store } from "./src/redux/store";
import AuthStack from "./src/navigation/AuthStack";
import MainStack from "./src/navigation/MainStack";
import { RootState } from "./src/redux/store";

function AppRouter() {
  const auth = useSelector((state: RootState) => state.auth);
  const isAuthenticated = Boolean(auth.tokens?.access_token);

  return <NavigationContainer>{isAuthenticated ? <MainStack /> : <AuthStack />}</NavigationContainer>;
}

export default function App() {
  return (
    <Provider store={store}>
      <AppRouter />
    </Provider>
  );
}
