import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { currentColors } from '../theme';

interface AppLogoProps {
  size?: 'small' | 'default' | 'large';
  showSparkle?: boolean;
}

const sizeMap = {
  small: { container: 40, emoji: 20, sparkle: 10 },
  default: { container: 80, emoji: 40, sparkle: 16 },
  large: { container: 120, emoji: 60, sparkle: 22 },
};

export const AppLogo: React.FC<AppLogoProps> = ({ 
  size = 'default',
  showSparkle = true 
}) => {
  const dimensions = sizeMap[size];
  const halfContainer = dimensions.container / 2;

  return (
    <View style={[styles.container, { width: dimensions.container, height: dimensions.container }]}>
      {/* Main circle with tooth emoji */}
      <View 
        style={[
          styles.logoCircle, 
          { 
            width: dimensions.container, 
            height: dimensions.container,
            borderRadius: halfContainer,
            backgroundColor: currentColors.primary,
          }
        ]}
      >
        <Text style={[styles.emoji, { fontSize: dimensions.emoji }]}>🦷</Text>
      </View>

      {/* Sparkle */}
      {showSparkle && (
        <View style={[styles.sparkle, { top: -2, right: -2 }]}>
          <Text style={[styles.sparkleEmoji, { fontSize: dimensions.sparkle }]}>✨</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'relative',
  },
  logoCircle: {
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: currentColors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  emoji: {
    textAlign: 'center',
  },
  sparkle: {
    position: 'absolute',
  },
  sparkleEmoji: {
    textAlign: 'center',
  },
});

export default AppLogo;
