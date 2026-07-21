import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

// Screens
import { SplashScreen } from '../screens/SplashScreen';
import { LoginScreen } from '../screens/auth/LoginScreen';
import { RegisterScreen } from '../screens/auth/RegisterScreen';
import { OTPVerificationScreen } from '../screens/auth/OTPVerificationScreen';
import { MainTabNavigator } from './MainTabNavigator';
import { NotificationsScreen } from '../screens/notifications/NotificationsScreen';
import { SchemeDetailScreen } from '../screens/schemes/SchemeDetailScreen';

export type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
  OTPVerification: { mobile: string; purpose: string; nextScreen: string; userData?: any };
  Main: undefined;
  Notifications: undefined;
  SchemeDetail: { schemeId: number };
};

const Stack = createStackNavigator<RootStackParamList>();

export const RootNavigator: React.FC = () => {
  const { isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          // Auth Stack
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
            <Stack.Screen name="OTPVerification" component={OTPVerificationScreen} />
          </>
        ) : (
          // Main App Stack
          <>
            <Stack.Screen name="Main" component={MainTabNavigator} />
            <Stack.Screen name="Notifications" component={NotificationsScreen} />
            <Stack.Screen name="SchemeDetail" component={SchemeDetailScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
