import { MD3DarkTheme, MD3LightTheme } from 'react-native-paper';

// Dark Ember Theme - Dark mode with orange accents
export const darkEmberTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: '#FF6B35',
    primaryContainer: 'rgba(255, 107, 53, 0.15)',
    secondary: '#FF7F52',
    secondaryContainer: 'rgba(255, 127, 82, 0.15)',
    surface: 'rgba(42, 26, 21, 0.6)',
    surfaceVariant: '#2A1A15',
    background: '#1A1A1A',
    error: '#DC2626',
    errorContainer: 'rgba(220, 38, 38, 0.15)',
    onPrimary: '#FFFFFF',
    onSurface: '#F5F5F5',
    onSurfaceVariant: '#A0A0A0',
    outline: 'rgba(255, 107, 53, 0.2)',
    outlineVariant: 'rgba(255, 107, 53, 0.1)',
    inverseSurface: '#F5F5F5',
    inverseOnSurface: '#1A1A1A',
    scrim: 'rgba(0, 0, 0, 0.7)',
    elevation: {
      level0: 'transparent',
      level1: 'rgba(42, 26, 21, 0.4)',
      level2: 'rgba(42, 26, 21, 0.5)',
      level3: 'rgba(42, 26, 21, 0.6)',
      level4: 'rgba(42, 26, 21, 0.7)',
      level5: 'rgba(42, 26, 21, 0.8)',
    },
  },
  roundness: 16,
};

// Sky Blue Theme - Light mode with blue accents
export const skyBlueTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: '#4A90E2',
    primaryContainer: 'rgba(74, 144, 226, 0.15)',
    secondary: '#6AA8E8',
    secondaryContainer: 'rgba(106, 168, 232, 0.15)',
    surface: '#FFFFFF',
    surfaceVariant: '#F8FAFC',
    background: '#F4F9FF',
    error: '#DC2626',
    errorContainer: 'rgba(220, 38, 38, 0.15)',
    onPrimary: '#FFFFFF',
    onSurface: '#1A2332',
    onSurfaceVariant: '#64748B',
    outline: 'rgba(74, 144, 226, 0.2)',
    outlineVariant: 'rgba(74, 144, 226, 0.1)',
    inverseSurface: '#1A2332',
    inverseOnSurface: '#F4F9FF',
    scrim: 'rgba(0, 0, 0, 0.5)',
    elevation: {
      level0: 'transparent',
      level1: '#FFFFFF',
      level2: '#FFFFFF',
      level3: '#FFFFFF',
      level4: '#FFFFFF',
      level5: '#FFFFFF',
    },
  },
  roundness: 16,
};

// Default to Dark Ember theme
export const theme = darkEmberTheme;

// Color constants for both themes
export const colors = {
  // Dark Ember
  darkEmber: {
    primary: '#FF6B35',
    primaryDark: '#E85A28',
    primaryLight: '#FF7F52',
    background: '#1A1A1A',
    backgroundGradientStart: '#1A1A1A',
    backgroundGradientEnd: '#2A1A15',
    cardBg: 'rgba(42, 26, 21, 0.6)',
    navBg: 'rgba(26, 26, 26, 0.9)',
    textPrimary: '#F5F5F5',
    textSecondary: '#A0A0A0',
    border: 'rgba(255, 107, 53, 0.1)',
    inputBg: 'rgba(42, 26, 21, 0.8)',
    shadow: 'rgba(0, 0, 0, 0.3)',
    buttonShadow: 'rgba(255, 107, 53, 0.3)',
  },
  // Sky Blue
  skyBlue: {
    primary: '#4A90E2',
    primaryDark: '#3A7BC8',
    primaryLight: '#6AA8E8',
    background: '#F4F9FF',
    backgroundGradientStart: '#F4F9FF',
    backgroundGradientEnd: '#E6F2FF',
    cardBg: '#FFFFFF',
    navBg: 'rgba(255, 255, 255, 0.9)',
    textPrimary: '#1A2332',
    textSecondary: '#64748B',
    border: 'rgba(74, 144, 226, 0.1)',
    inputBg: '#F8FAFC',
    shadow: 'rgba(74, 144, 226, 0.08)',
    buttonShadow: 'rgba(74, 144, 226, 0.2)',
  },
  // Common
  success: '#16A34A',
  warning: '#F59E0B',
  error: '#DC2626',
  info: '#4A90E2',
};

// Current theme colors (Dark Ember by default)
export const currentColors = colors.darkEmber;
