import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { PaperProvider } from 'react-native-paper';
import { Provider as ReduxProvider } from 'react-redux';
import { ToastProvider } from 'react-native-toast-notifications';
import { store } from './src/redux/store';
import { AuthProvider } from './src/contexts/AuthContext';
import { ThemeProvider, useTheme } from './src/contexts/ThemeContext';
import { RootNavigator } from './src/navigation/RootNavigator';
import { getPaperTheme } from './src/theme';

function AppContent() {
  const { isDark } = useTheme();
  const paperTheme = getPaperTheme(isDark);

  return (
    <PaperProvider theme={paperTheme}>
      <SafeAreaProvider>
        <ToastProvider>
          <AuthProvider>
            <RootNavigator />
            <StatusBar style={isDark ? 'light' : 'dark'} />
          </AuthProvider>
        </ToastProvider>
      </SafeAreaProvider>
    </PaperProvider>
  );
}

export default function App() {
  return (
    <ReduxProvider store={store}>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </ReduxProvider>
  );
}
