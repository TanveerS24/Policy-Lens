import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import * as Font from 'expo-font';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Provider } from 'react-redux';
import store from './src/store';

// Screens
import LoginScreen from './src/screens/auth/LoginScreen';
import RegisterScreen from './src/screens/auth/RegisterScreen';
import OTPVerificationScreen from './src/screens/auth/OTPVerificationScreen';
import HomeScreen from './src/screens/client/HomeScreen';
import {
  PoliciesScreen,
  PolicyDetailsScreen,
  UploadScreen,
  MyUploadsScreen,
  ProfileScreen,
  AdminDashboardScreen,
  AdminPoliciesScreen,
  AdminUploadsScreen,
} from './src/screens/PlaceholderScreens';

import { useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Auth Navigation
const AuthNavigator = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animationEnabled: true,
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="OTPVerification" component={OTPVerificationScreen} />
    </Stack.Navigator>
  );
};

// Client Tab Navigation
const ClientTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          
          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Policies') iconName = 'file-document-multiple';
          else if (route.name === 'Upload') iconName = 'cloud-upload';
          else if (route.name === 'MyUploads') iconName = 'history';
          else if (route.name === 'Profile') iconName = 'account';
          
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#1E88E5',
        tabBarInactiveTintColor: '#999',
        headerShown: true,
        headerStyle: {
          backgroundColor: '#1E88E5',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
      <Tab.Screen
        name="Policies"
        component={PoliciesScreen}
        options={{ title: 'Policies' }}
      />
      <Tab.Screen
        name="Upload"
        component={UploadScreen}
        options={{ title: 'Upload Policy' }}
      />
      <Tab.Screen
        name="MyUploads"
        component={MyUploadsScreen}
        options={{ title: 'My Uploads' }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

// Client Stack Navigator
const ClientNavigator = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#1E88E5',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen
        name="ClientTabs"
        component={ClientTabNavigator}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="PolicyDetails"
        component={PolicyDetailsScreen}
        options={{ title: 'Policy Details' }}
      />
    </Stack.Navigator>
  );
};

// Admin Navigator
const AdminNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          
          if (route.name === 'Dashboard') iconName = 'view-dashboard';
          else if (route.name === 'Policies') iconName = 'file-document-multiple';
          else if (route.name === 'Uploads') iconName = 'folder-check';
          else if (route.name === 'Profile') iconName = 'account';
          
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#1E88E5',
        tabBarInactiveTintColor: '#999',
        headerShown: true,
        headerStyle: {
          backgroundColor: '#1E88E5',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen
        name="Dashboard"
        component={AdminDashboardScreen}
        options={{ title: 'Dashboard' }}
      />
      <Tab.Screen
        name="Policies"
        component={AdminPoliciesScreen}
        options={{ title: 'Policies' }}
      />
      <Tab.Screen
        name="Uploads"
        component={AdminUploadsScreen}
        options={{ title: 'Pending Uploads' }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

// Root Navigator
const RootNavigator = () => {
  const authState = useSelector((state) => state.auth);

  const isAuthenticated = !!authState.accessToken;
  const isAdmin = authState.role === 'admin';

  return (
    <NavigationContainer>
      {isAuthenticated ? (
        isAdmin ? <AdminNavigator /> : <ClientNavigator />
      ) : (
        <AuthNavigator />
      )}
    </NavigationContainer>
  );
};

// Main App Component
export default function App() {
  const [appIsReady, setAppIsReady] = useState(false);

  useEffect(() => {
    const prepare = async () => {
      try {
        // Load fonts if needed
        // await Font.loadAsync({...});
      } catch (e) {
        console.warn(e);
      } finally {
        setAppIsReady(true);
      }
    };

    prepare();
  }, []);

  if (!appIsReady) {
    return null;
  }

  return (
    <Provider store={store}>
      <RootNavigator />
    </Provider>
  );
}
