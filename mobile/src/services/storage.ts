import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';

/**
 * Cross-platform storage utility.
 * Uses Expo SecureStore on native devices (iOS/Android) for secure token storage,
 * and falls back to AsyncStorage on Web platforms.
 */
export const storage = {
  async getItemAsync(key: string): Promise<string | null> {
    try {
      if (Platform.OS === 'web') {
        return await AsyncStorage.getItem(key);
      }
      return await SecureStore.getItemAsync(key);
    } catch (error) {
      console.error(`Error getting ${key} from secure storage:`, error);
      // Fallback attempt with AsyncStorage if SecureStore fails
      try {
        return await AsyncStorage.getItem(key);
      } catch {
        return null;
      }
    }
  },

  async setItemAsync(key: string, value: string): Promise<void> {
    try {
      if (Platform.OS === 'web') {
        await AsyncStorage.setItem(key, value);
      } else {
        await SecureStore.setItemAsync(key, value);
      }
    } catch (error) {
      console.error(`Error setting ${key} in secure storage:`, error);
      try {
        await AsyncStorage.setItem(key, value);
      } catch (fallbackError) {
        console.error(`Fallback AsyncStorage set failed for ${key}:`, fallbackError);
      }
    }
  },

  async deleteItemAsync(key: string): Promise<void> {
    try {
      if (Platform.OS === 'web') {
        await AsyncStorage.removeItem(key);
      } else {
        await SecureStore.deleteItemAsync(key);
      }
    } catch (error) {
      console.error(`Error deleting ${key} from secure storage:`, error);
      try {
        await AsyncStorage.removeItem(key);
      } catch (fallbackError) {
        console.error(`Fallback AsyncStorage remove failed for ${key}:`, fallbackError);
      }
    }
  },
};
