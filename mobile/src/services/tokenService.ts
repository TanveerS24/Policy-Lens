import AsyncStorage from "@react-native-async-storage/async-storage";
import { AuthResponse } from "../types";

const ACCESS_TOKEN_KEY = "PolicyLens.AccessToken";
const REFRESH_TOKEN_KEY = "PolicyLens.RefreshToken";

export async function storeTokens(tokens: AuthResponse): Promise<void> {
  await AsyncStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  await AsyncStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

export async function getAccessToken(): Promise<string | null> {
  return AsyncStorage.getItem(ACCESS_TOKEN_KEY);
}

export async function getRefreshToken(): Promise<string | null> {
  return AsyncStorage.getItem(REFRESH_TOKEN_KEY);
}

export async function removeTokens(): Promise<void> {
  await AsyncStorage.multiRemove([ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY]);
}
