import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { currentColors } from '../theme';
import { AppLogo } from '../components/AppLogo';

export const SplashScreen: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Logo */}
        <AppLogo size="large" showSparkle={true} />

        {/* App Name */}
        <View style={styles.textContainer}>
          <Text style={styles.logoText}>DentalSchemes</Text>
          <Text style={styles.subtitle}>India</Text>
        </View>

        {/* Loading Indicator */}
        <View style={styles.loaderContainer}>
          <ActivityIndicator size="large" color={currentColors.primary} />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: currentColors.background,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  textContainer: {
    alignItems: 'center',
    marginBottom: 48,
  },
  logoText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: currentColors.primary,
  },
  subtitle: {
    fontSize: 20,
    color: currentColors.textSecondary,
    marginTop: 4,
    letterSpacing: 4,
  },
  loaderContainer: {
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 14,
    color: currentColors.textSecondary,
  },
});
