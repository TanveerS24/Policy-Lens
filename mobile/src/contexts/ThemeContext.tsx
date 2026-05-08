import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export type ThemeType = 'light' | 'dark';

interface ThemeColors {
  background: string;
  surface: string;
  primary: string;
  secondary: string;
  accent: string;
  textPrimary: string;
  textSecondary: string;
  textMuted: string;
  border: string;
  cardBg: string;
  inputBg: string;
  shadow: string;
  error: string;
  success: string;
  warning: string;
}

interface ThemeContextType {
  theme: ThemeType;
  colors: ThemeColors;
  setTheme: (theme: ThemeType) => void;
  toggleTheme: () => void;
  isDark: boolean;
}

// Light Theme - Silver and Peach Blue (High Contrast)
const lightTheme: ThemeColors = {
  background: '#F5F7FA', // Silver white
  surface: '#FFFFFF',
  primary: '#2563EB', // Stronger blue for better contrast
  secondary: '#60A5FA', // Lighter blue
  accent: '#F97316', // Orange accent
  textPrimary: '#111827', // Near black for maximum readability
  textSecondary: '#4B5563', // Dark gray - much more readable
  textMuted: '#6B7280', // Medium gray
  border: '#D1D5DB',
  cardBg: '#FFFFFF',
  inputBg: '#F3F4F6',
  shadow: '#000000',
  error: '#DC2626',
  success: '#16A34A',
  warning: '#D97706',
};

// Dark Theme - Monokai (High Contrast)
const darkTheme: ThemeColors = {
  background: '#1E1E1E', // Darker background for better contrast
  surface: '#2D2D2D',
  primary: '#66D9EF', // Cyan
  secondary: '#A6E22E', // Green
  accent: '#FD971F', // Orange
  textPrimary: '#FFFFFF', // Pure white for maximum contrast
  textSecondary: '#B4B4B4', // Light gray - much more readable
  textMuted: '#808080', // Medium gray for muted text
  border: '#404040',
  cardBg: '#2D2D2D',
  inputBg: '#3D3D3D',
  shadow: '#000000',
  error: '#FF5370', // Brighter red
  success: '#A6E22E', // Green
  warning: '#E6DB74', // Yellow
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<ThemeType>('light');

  useEffect(() => {
    loadTheme();
  }, []);

  const loadTheme = async () => {
    try {
      const savedTheme = await AsyncStorage.getItem('app-theme');
      if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
        setThemeState(savedTheme);
      }
    } catch (error) {
      console.error('Failed to load theme:', error);
    }
  };

  const setTheme = async (newTheme: ThemeType) => {
    try {
      await AsyncStorage.setItem('app-theme', newTheme);
      setThemeState(newTheme);
    } catch (error) {
      console.error('Failed to save theme:', error);
    }
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const colors = theme === 'light' ? lightTheme : darkTheme;
  const isDark = theme === 'dark';

  return (
    <ThemeContext.Provider value={{ theme, colors, setTheme, toggleTheme, isDark }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export { lightTheme, darkTheme };
export type { ThemeColors };
