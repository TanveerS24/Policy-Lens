import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Text, TextInput, Button, Snackbar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { RootState, AppDispatch } from '../../redux/store';
import { login, clearError } from '../../redux/slices/authSlice';
import { theme, currentColors } from '../../theme';
import { AppLogo } from '../../components/AppLogo';

type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Login'>;

export const LoginScreen: React.FC = () => {
  const navigation = useNavigation<LoginScreenNavigationProp>();
  const dispatch = useDispatch<AppDispatch>();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  const [mobileOrEmail, setMobileOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [snackbarVisible, setSnackbarVisible] = useState(false);

  const handleLogin = async () => {
    if (!mobileOrEmail || !password) {
      return;
    }

    try {
      await dispatch(login({ mobileOrEmail, password })).unwrap();
    } catch (err) {
      setSnackbarVisible(true);
    }
  };

  const handleRegister = () => {
    navigation.navigate('Register');
  };

  return (
    <View style={styles.gradient}>
      <SafeAreaView style={styles.container}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <ScrollView
            contentContainerStyle={styles.scrollContent}
            keyboardShouldPersistTaps="handled"
          >
            {/* Logo & Header */}
            <View style={styles.header}>
              <AppLogo size="large" />
              <Text style={styles.title}>Welcome Back</Text>
              <Text style={styles.subtitle}>
                Sign in to explore dental health schemes
              </Text>
            </View>

            {/* Glassmorphism Card */}
            <View style={styles.card}>
              <View style={styles.form}>
                <TextInput
                  label="Mobile or Email"
                  value={mobileOrEmail}
                  onChangeText={setMobileOrEmail}
                  mode="outlined"
                  keyboardType="email-address"
                  autoCapitalize="none"
                  style={styles.input}
                  outlineColor={currentColors.border}
                  activeOutlineColor={currentColors.primary}
                  textColor={currentColors.textPrimary}
                  theme={{
                    colors: {
                      surface: currentColors.inputBg,
                      onSurface: currentColors.textPrimary,
                      onSurfaceVariant: currentColors.textSecondary,
                      primary: currentColors.primary,
                    },
                  }}
                />

                <TextInput
                  label="Password"
                  value={password}
                  onChangeText={setPassword}
                  mode="outlined"
                  secureTextEntry={!showPassword}
                  right={
                    <TextInput.Icon
                      icon={showPassword ? 'eye-off' : 'eye'}
                      onPress={() => setShowPassword(!showPassword)}
                      color={currentColors.textSecondary}
                    />
                  }
                  style={styles.input}
                  outlineColor={currentColors.border}
                  activeOutlineColor={currentColors.primary}
                  textColor={currentColors.textPrimary}
                  theme={{
                    colors: {
                      surface: currentColors.inputBg,
                      onSurface: currentColors.textPrimary,
                      onSurfaceVariant: currentColors.textSecondary,
                      primary: currentColors.primary,
                    },
                  }}
                />

                <TouchableOpacity style={styles.forgotPassword}>
                  <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[
                    styles.loginButton,
                    styles.buttonGradient,
                    (isLoading || !mobileOrEmail || !password) && styles.loginButtonDisabled,
                  ]}
                  onPress={handleLogin}
                  disabled={isLoading || !mobileOrEmail || !password}
                >
                  <Text style={styles.buttonText}>
                    {isLoading ? 'Signing In...' : 'Sign In'}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Register Link */}
            <View style={styles.registerContainer}>
              <Text style={styles.registerText}>Don't have an account?</Text>
              <TouchableOpacity onPress={handleRegister}>
                <Text style={styles.registerLink}>Create Account</Text>
              </TouchableOpacity>
            </View>
          </ScrollView>
        </KeyboardAvoidingView>

        <Snackbar
          visible={snackbarVisible || !!error}
          onDismiss={() => {
            setSnackbarVisible(false);
            dispatch(clearError());
          }}
          duration={3000}
          style={styles.snackbar}
        >
          {error || 'Login failed. Please try again.'}
        </Snackbar>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
    backgroundColor: currentColors.background,
  },
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: currentColors.textPrimary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: currentColors.textSecondary,
    textAlign: 'center',
  },
  card: {
    backgroundColor: currentColors.cardBg,
    borderRadius: 24,
    padding: 24,
    borderWidth: 1,
    borderColor: currentColors.border,
    shadowColor: currentColors.shadow,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.5,
    shadowRadius: 24,
    elevation: 10,
  },
  form: {
    gap: 16,
  },
  input: {
    backgroundColor: currentColors.inputBg,
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginTop: -8,
  },
  forgotPasswordText: {
    color: currentColors.primary,
    fontSize: 14,
    fontWeight: '500',
  },
  loginButton: {
    marginTop: 8,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: currentColors.buttonShadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 6,
  },
  loginButtonDisabled: {
    opacity: 0.6,
  },
  buttonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
    backgroundColor: currentColors.primary,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  registerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 24,
    gap: 4,
  },
  registerText: {
    color: currentColors.textSecondary,
    fontSize: 14,
  },
  registerLink: {
    color: currentColors.primary,
    fontSize: 14,
    fontWeight: '600',
  },
  snackbar: {
    backgroundColor: currentColors.cardBg,
    borderRadius: 12,
  },
});
