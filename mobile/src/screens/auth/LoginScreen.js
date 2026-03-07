import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../../store/authSlice';
import { Button, Card, Loading } from '../../components/ui';
import { COLORS } from '../../config/api';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state) => state.auth);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Validation', 'Please enter email and password');
      return;
    }

    try {
      const result = await dispatch(login({ email, password })).unwrap();
      // Navigation happens automatically on auth state change
    } catch (err) {
      Alert.alert('Login Failed', err.message || 'Invalid credentials');
    }
  };

  if (loading) return <Loading />;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={styles.title}>Healthcare Policy Intelligence</Text>
        <Text style={styles.subtitle}>Understand Your Healthcare Policies</Text>
      </View>

      <Card style={styles.formCard}>
        <Text style={styles.formTitle}>Login</Text>

        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          editable={!loading}
        />

        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={!loading}
        />

        {error && <Text style={styles.errorText}>{error}</Text>}

        <Button
          title="Login"
          onPress={handleLogin}
          loading={loading}
          disabled={loading}
        />

        <TouchableOpacity
          onPress={() => navigation.navigate('Register')}
          disabled={loading}
        >
          <Text style={styles.linkText}>
            Don't have an account? <Text style={styles.linkBold}>Register</Text>
          </Text>
        </TouchableOpacity>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  headerContainer: {
    padding: 24,
    paddingTop: 48,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  formCard: {
    marginHorizontal: 16,
    marginBottom: 32,
  },
  formTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 16,
    color: COLORS.text,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 16,
    fontSize: 16,
  },
  errorText: {
    color: COLORS.error,
    marginBottom: 12,
    fontSize: 14,
  },
  linkText: {
    textAlign: 'center',
    marginTop: 16,
    color: COLORS.textSecondary,
    fontSize: 14,
  },
  linkBold: {
    fontWeight: '600',
    color: COLORS.primary,
  },
});

export default LoginScreen;
