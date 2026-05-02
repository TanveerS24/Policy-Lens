import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { Text, TextInput, Button, HelperText, Snackbar, Menu } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { RootState } from '../../redux/store';
import { requestOTP, clearError } from '../../redux/slices/authSlice';
import { theme } from '../../theme';

type RegisterScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Register'>;

const INDIAN_STATES = [
  'Andhra Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
  'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Odisha', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telangana',
  'Uttar Pradesh', 'West Bengal', 'Delhi',
];

const GENDERS = ['male', 'female', 'other'];

export const RegisterScreen: React.FC = () => {
  const navigation = useNavigation<RegisterScreenNavigationProp>();
  const dispatch = useDispatch();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    mobile: '',
    dateOfBirth: '',
    gender: '',
    state: '',
    district: '',
    pinCode: '',
    password: '',
    confirmPassword: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showStateMenu, setShowStateMenu] = useState(false);
  const [showGenderMenu, setShowGenderMenu] = useState(false);
  const [snackbarVisible, setSnackbarVisible] = useState(false);

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      return 'Passwords do not match';
    }
    if (formData.mobile.length !== 10) {
      return 'Mobile number must be 10 digits';
    }
    if (formData.pinCode.length !== 6) {
      return 'PIN code must be 6 digits';
    }
    return null;
  };

  const handleRegister = async () => {
    const error = validateForm();
    if (error) {
      dispatch(clearError());
      setSnackbarVisible(true);
      return;
    }

    // Request OTP
    try {
      await dispatch(requestOTP({ mobile: formData.mobile, purpose: 'registration' })).unwrap();
      navigation.navigate('OTPVerification', {
        mobile: formData.mobile,
        purpose: 'registration',
        nextScreen: 'Main',
      });
    } catch (err) {
      setSnackbarVisible(true);
    }
  };

  const handleLogin = () => {
    navigation.navigate('Login');
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.header}>
            <Text variant="displaySmall" style={styles.title}>
              Create Account
            </Text>
            <Text variant="bodyLarge" style={styles.subtitle}>
              Sign up to explore dental health schemes
            </Text>
          </View>

          <View style={styles.form}>
            <TextInput
              label="Full Name *"
              value={formData.name}
              onChangeText={(text) => updateForm('name', text)}
              mode="outlined"
              style={styles.input}
            />

            <TextInput
              label="Mobile Number *"
              value={formData.mobile}
              onChangeText={(text) => updateForm('mobile', text.replace(/[^0-9]/g, '').slice(0, 10))}
              mode="outlined"
              keyboardType="phone-pad"
              style={styles.input}
            />

            <TextInput
              label="Email (optional)"
              value={formData.email}
              onChangeText={(text) => updateForm('email', text)}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
            />

            <TextInput
              label="Date of Birth (YYYY-MM-DD) *"
              value={formData.dateOfBirth}
              onChangeText={(text) => updateForm('dateOfBirth', text)}
              mode="outlined"
              placeholder="1990-01-01"
              style={styles.input}
            />

            <Menu
              visible={showGenderMenu}
              onDismiss={() => setShowGenderMenu(false)}
              anchor={
                <TextInput
                  label="Gender *"
                  value={formData.gender}
                  onFocus={() => setShowGenderMenu(true)}
                  mode="outlined"
                  style={styles.input}
                  right={<TextInput.Icon icon="menu-down" />}
                />
              }
            >
              {GENDERS.map((gender) => (
                <Menu.Item
                  key={gender}
                  onPress={() => {
                    updateForm('gender', gender);
                    setShowGenderMenu(false);
                  }}
                  title={gender.charAt(0).toUpperCase() + gender.slice(1)}
                />
              ))}
            </Menu>

            <Menu
              visible={showStateMenu}
              onDismiss={() => setShowStateMenu(false)}
              anchor={
                <TextInput
                  label="State *"
                  value={formData.state}
                  onFocus={() => setShowStateMenu(true)}
                  mode="outlined"
                  style={styles.input}
                  right={<TextInput.Icon icon="menu-down" />}
                />
              }
            >
              {INDIAN_STATES.map((state) => (
                <Menu.Item
                  key={state}
                  onPress={() => {
                    updateForm('state', state);
                    setShowStateMenu(false);
                  }}
                  title={state}
                />
              ))}
            </Menu>

            <TextInput
              label="District *"
              value={formData.district}
              onChangeText={(text) => updateForm('district', text)}
              mode="outlined"
              style={styles.input}
            />

            <TextInput
              label="PIN Code *"
              value={formData.pinCode}
              onChangeText={(text) => updateForm('pinCode', text.replace(/[^0-9]/g, '').slice(0, 6))}
              mode="outlined"
              keyboardType="number-pad"
              style={styles.input}
            />

            <TextInput
              label="Password * (min 8 chars)"
              value={formData.password}
              onChangeText={(text) => updateForm('password', text)}
              mode="outlined"
              secureTextEntry={!showPassword}
              right={
                <TextInput.Icon
                  icon={showPassword ? 'eye-off' : 'eye'}
                  onPress={() => setShowPassword(!showPassword)}
                />
              }
              style={styles.input}
            />

            <TextInput
              label="Confirm Password *"
              value={formData.confirmPassword}
              onChangeText={(text) => updateForm('confirmPassword', text)}
              mode="outlined"
              secureTextEntry={!showPassword}
              style={styles.input}
            />

            <Button
              mode="contained"
              onPress={handleRegister}
              loading={isLoading}
              disabled={isLoading}
              style={styles.registerButton}
              contentStyle={styles.buttonContent}
            >
              Continue
            </Button>

            <View style={styles.loginContainer}>
              <Text variant="bodyMedium">Already have an account?</Text>
              <Button mode="text" onPress={handleLogin}>
                Sign In
              </Button>
            </View>
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
      >
        {error || validateForm() || 'Registration failed. Please try again.'}
      </Snackbar>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    padding: 24,
  },
  header: {
    marginTop: 24,
    marginBottom: 24,
  },
  title: {
    color: theme.colors.primary,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    color: theme.colors.onSurfaceVariant,
  },
  form: {
    gap: 12,
  },
  input: {
    backgroundColor: theme.colors.surface,
  },
  registerButton: {
    marginTop: 16,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  loginContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 16,
  },
});
