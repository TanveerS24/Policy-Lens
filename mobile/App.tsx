import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { PaperProvider } from 'react-native-paper';
import { Provider as ReduxProvider } from 'react-redux';
import { ToastProvider } from 'react-native-toast-notifications';
import { store } from './src/redux/store';
import { AuthProvider } from './src/contexts/AuthContext';
import { ThemeProvider } from './src/contexts/ThemeContext';
import { RootNavigator } from './src/navigation/RootNavigator';
import { theme } from './src/theme';

export default function App() {
  return (
    <ReduxProvider store={store}>
      <ThemeProvider>
        <PaperProvider theme={theme}>
          <SafeAreaProvider>
            <ToastProvider>
              <AuthProvider>
                <RootNavigator />
                <StatusBar style="auto" />
              </AuthProvider>
            </ToastProvider>
          </SafeAreaProvider>
        </PaperProvider>
      </ThemeProvider>
    </ReduxProvider>
  );
}
