import { MD3LightTheme as DefaultTheme } from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#2563EB',
    primaryContainer: '#DBEAFE',
    secondary: '#0D9488',
    secondaryContainer: '#CCFBF1',
    surface: '#FFFFFF',
    surfaceVariant: '#F1F5F9',
    background: '#F8FAFC',
    error: '#DC2626',
    errorContainer: '#FEE2E2',
    onPrimary: '#FFFFFF',
    onSurface: '#1E293B',
    onSurfaceVariant: '#64748B',
    outline: '#CBD5E1',
    outlineVariant: '#E2E8F0',
    inverseSurface: '#1E293B',
    inverseOnSurface: '#F8FAFC',
    scrim: 'rgba(0, 0, 0, 0.5)',
  },
  roundness: 8,
};

export const colors = {
  primary: '#2563EB',
  primaryLight: '#DBEAFE',
  secondary: '#0D9488',
  secondaryLight: '#CCFBF1',
  success: '#16A34A',
  warning: '#F59E0B',
  error: '#DC2626',
  info: '#2563EB',
  text: '#1E293B',
  textSecondary: '#64748B',
  textMuted: '#94A3B8',
  background: '#F8FAFC',
  surface: '#FFFFFF',
  border: '#E2E8F0',
};
