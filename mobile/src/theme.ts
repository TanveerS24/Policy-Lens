import { MD3DarkTheme, MD3LightTheme } from 'react-native-paper';

// Get the Paper theme dynamically based on current theme mode
export const getPaperTheme = (isDark: boolean) => {
  const base = isDark ? MD3DarkTheme : MD3LightTheme;

  if (isDark) {
    return {
      ...base,
      colors: {
        ...base.colors,
        primary: '#66D9EF',
        primaryContainer: 'rgba(102, 217, 239, 0.15)',
        secondary: '#A6E22E',
        secondaryContainer: 'rgba(166, 226, 46, 0.15)',
        surface: '#2D2D2D',
        surfaceVariant: '#3D3D3D',
        background: '#1E1E1E',
        error: '#FF5370',
        errorContainer: 'rgba(255, 83, 112, 0.15)',
        onPrimary: '#FFFFFF',
        onSurface: '#FFFFFF',
        onSurfaceVariant: '#B4B4B4',
        outline: 'rgba(102, 217, 239, 0.2)',
        outlineVariant: 'rgba(102, 217, 239, 0.1)',
        inverseSurface: '#FFFFFF',
        inverseOnSurface: '#1E1E1E',
        scrim: 'rgba(0, 0, 0, 0.7)',
        elevation: {
          level0: 'transparent',
          level1: '#2D2D2D',
          level2: '#333333',
          level3: '#383838',
          level4: '#3D3D3D',
          level5: '#424242',
        },
      },
      roundness: 16,
    };
  }

  return {
    ...base,
    colors: {
      ...base.colors,
      primary: '#2563EB',
      primaryContainer: 'rgba(37, 99, 235, 0.15)',
      secondary: '#60A5FA',
      secondaryContainer: 'rgba(96, 165, 250, 0.15)',
      surface: '#FFFFFF',
      surfaceVariant: '#F3F4F6',
      background: '#F5F7FA',
      error: '#DC2626',
      errorContainer: 'rgba(220, 38, 38, 0.15)',
      onPrimary: '#FFFFFF',
      onSurface: '#111827',
      onSurfaceVariant: '#4B5563',
      outline: 'rgba(37, 99, 235, 0.2)',
      outlineVariant: 'rgba(37, 99, 235, 0.1)',
      inverseSurface: '#111827',
      inverseOnSurface: '#F5F7FA',
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
};

// Default export for backward compatibility (light theme)
export const theme = getPaperTheme(false);

// Color constants for both themes
export const colors = {
  // Dark Ember (kept for reference, not actively used)
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
  // Sky Blue (kept for reference, not actively used)
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

// Current theme colors (Dark Ember by default — kept for backward compat)
export const currentColors = colors.darkEmber;
