import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  TextInput,
} from 'react-native';
import { COLORS } from '../../config/api';

export const Button = ({
  title,
  onPress,
  loading = false,
  disabled = false,
  variant = 'primary',
  size = 'medium',
}) => {
  const getBackgroundColor = () => {
    if (disabled) return '#CCCCCC';
    return variant === 'primary' ? COLORS.primary : COLORS.secondary;
  };

  const getPadding = () => {
    switch (size) {
      case 'small':
        return 8;
      case 'large':
        return 16;
      default:
        return 12;
    }
  };

  return (
    <TouchableOpacity
      style={[styles.button, { padding: getPadding(), backgroundColor: getBackgroundColor() }]}
      onPress={onPress}
      disabled={disabled || loading}
    >
      {loading ? (
        <ActivityIndicator color="#fff" />
      ) : (
        <Text style={styles.buttonText}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

export const Card = ({ children, style }) => {
  return <View style={[styles.card, style]}>{children}</View>;
};

export const Input = ({ placeholder, value, onChangeText, secureTextEntry, multiline, numberOfLines }) => {
  return (
    <View style={styles.inputContainer}>
      <TextInput
        style={[styles.input, multiline && { height: numberOfLines ? numberOfLines * 40 : 100 }]}
        placeholder={placeholder}
        value={value}
        onChangeText={onChangeText}
        secureTextEntry={secureTextEntry}
        multiline={multiline}
        numberOfLines={numberOfLines}
        placeholderTextColor="#999"
      />
    </View>
  );
};

export const Badge = ({ label, value, variant = 'primary' }) => {
  const getColor = () => {
    switch (variant) {
      case 'success':
        return COLORS.success;
      case 'error':
        return COLORS.error;
      case 'warning':
        return COLORS.warning;
      default:
        return COLORS.primary;
    }
  };

  return (
    <View style={[styles.badge, { backgroundColor: getColor() + '20', borderColor: getColor() }]}>
      <Text style={[styles.badgeLabel, { color: getColor() }]}>
        {label}: {value}
      </Text>
    </View>
  );
};

export const Loading = () => {
  return (
    <View style={styles.loadingContainer}>
      <ActivityIndicator size="large" color={COLORS.primary} />
    </View>
  );
};

export const EmptyState = ({ message, icon }) => {
  return (
    <View style={styles.emptyStateContainer}>
      <Text style={styles.emptyStateMessage}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  inputContainer: {
    marginVertical: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    backgroundColor: COLORS.card,
  },
  badge: {
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    marginRight: 8,
    marginBottom: 8,
  },
  badgeLabel: {
    fontSize: 12,
    fontWeight: '600',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyStateContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  emptyStateMessage: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});

export default {
  Button,
  Card,
  Input,
  Badge,
  Loading,
  EmptyState,
};
