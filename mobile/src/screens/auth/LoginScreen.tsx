import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Text, TextInput, Snackbar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { RootState, AppDispatch } from '../../redux/store';
import { login, clearError } from '../../redux/slices/authSlice';
import { useTheme } from '../../contexts/ThemeContext';
import { AppLogo } from '../../components/AppLogo';

type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Login'>;

export const LoginScreen: React.FC = () => {
  const navigation = useNavigation<LoginScreenNavigationProp>();
  const dispatch = useDispatch<AppDispatch>();
  const { colors } = useTheme();
  const styles = createStyles(colors);
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
                <View style={styles.inputGroup}>
                  <Text variant="titleSmall" style={styles.inputLabel}>
                    Mobile or Email
                  </Text>
                  <TextInput
                    placeholder="Enter mobile or email"
                    value={mobileOrEmail}
                    onChangeText={setMobileOrEmail}
                    mode="outlined"
                    keyboardType="email-address"
                    autoCapitalize="none"
                    style={styles.input}
                    outlineColor={colors.border}
                    activeOutlineColor={colors.primary}
                    textColor={colors.textPrimary}
                    placeholderTextColor={colors.textSecondary}
                    theme={{
                      colors: {
                        surface: colors.inputBg,
                        onSurface: colors.textPrimary,
                        onSurfaceVariant: colors.textSecondary,
                        primary: colors.primary,
                      },
                    }}
                  />
                </View>

                <View style={styles.inputGroup}>
                  <Text variant="titleSmall" style={styles.inputLabel}>
                    Password
                  </Text>
                  <TextInput
                    placeholder="Enter password"
                    value={password}
                    onChangeText={setPassword}
                    mode="outlined"
                    secureTextEntry={!showPassword}
                    right={
                      <TextInput.Icon
                        icon={showPassword ? 'eye-off' : 'eye'}
                        onPress={() => setShowPassword(!showPassword)}
                        color={colors.textSecondary}
                      />
                    }
                    style={styles.input}
                    outlineColor={colors.border}
                    activeOutlineColor={colors.primary}
                    textColor={colors.textPrimary}
                    placeholderTextColor={colors.textSecondary}
                    theme={{
                      colors: {
                        surface: colors.inputBg,
                        onSurface: colors.textPrimary,
                        onSurfaceVariant: colors.textSecondary,
                        primary: colors.primary,
                      },
                    }}
                  />
                </View>

                <TouchableOpacity style={styles.forgotPassword} activeOpacity={0.7}>
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
              <TouchableOpacity onPress={handleRegister} activeOpacity={0.7} style={styles.registerTouch}>
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

const createStyles = (colors: any) => StyleSheet.create({
  gradient: {
    flex: 1,
    backgroundColor: colors.background,
  },
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 16,
    paddingVertical: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 6,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    textAlign: 'center',
    paddingHorizontal: 12,
  },
  card: {
    backgroundColor: colors.cardBg,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 20,
    borderWidth: 1,
    borderColor: colors.border,
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  form: {
    gap: 14,
  },
  inputGroup: {
    gap: 4,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 2,
  },
  input: {
    backgroundColor: colors.inputBg,
    fontSize: 15,
  },
  forgotPassword: {
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
    width: '100%',
    marginVertical: 6,
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  forgotPasswordText: {
    color: colors.primary,
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
  loginButton: {
    marginTop: 6,
    borderRadius: 14,
    overflow: 'hidden',
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  loginButtonDisabled: {
    opacity: 0.6,
  },
  buttonGradient: {
    paddingVertical: 14,
    paddingHorizontal: 16,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    width: '100%',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    textAlign: 'center',
  },
  registerContainer: {
    marginTop: 24,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    paddingHorizontal: 12,
  },
  registerTouch: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  registerText: {
    color: colors.textSecondary,
    fontSize: 14,
    textAlign: 'center',
  },
  registerLink: {
    color: colors.primary,
    fontSize: 14,
    fontWeight: '700',
    textAlign: 'center',
  },
  snackbar: {
    backgroundColor: colors.error,
    borderRadius: 12,
  },
});
