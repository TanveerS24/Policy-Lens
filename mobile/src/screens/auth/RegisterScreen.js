import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  FlatList,
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useDispatch, useSelector } from 'react-redux';
import { register } from '../../store/authSlice';
import { Button, Card, Loading } from '../../components/ui';
import { COLORS, STATES } from '../../config/api';

const RegisterScreen = ({ navigation }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [state, setState] = useState('');
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state) => state.auth);

  const handleRegister = async () => {
    if (!name || !email || !password) {
      Alert.alert('Validation', 'Name, email, and password are required');
      return;
    }

    const result = await dispatch(
      register({
        name,
        email,
        password,
        age: age ? parseInt(age) : null,
        gender: gender || null,
        state: state || null,
      })
    );

    if (register.fulfilled.match(result)) {
      Alert.alert('Success', 'OTP sent to your email', [
        {
          text: 'OK',
          onPress: () => navigation.navigate('OTPVerification', { email }),
        },
      ]);
    }
  };

  if (loading) return <Loading />;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={styles.title}>Create Account</Text>
      </View>

      <Card style={styles.formCard}>
        <TextInput
          style={styles.input}
          placeholder="Full Name"
          value={name}
          onChangeText={setName}
          editable={!loading}
        />

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
          placeholder="Password (min 8 characters)"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={!loading}
        />

        <TextInput
          style={styles.input}
          placeholder="Age (optional)"
          value={age}
          onChangeText={setAge}
          keyboardType="numeric"
          editable={!loading}
        />

        <Picker
          selectedValue={gender}
          onValueChange={setGender}
          style={styles.picker}
          enabled={!loading}
        >
          <Picker.Item label="Select Gender (optional)" value="" />
          <Picker.Item label="Male" value="male" />
          <Picker.Item label="Female" value="female" />
          <Picker.Item label="Other" value="other" />
        </Picker>

        <Picker
          selectedValue={state}
          onValueChange={setState}
          style={styles.picker}
          enabled={!loading}
        >
          <Picker.Item label="Select State (optional)" value="" />
          {STATES.map((s) => (
            <Picker.Item key={s} label={s} value={s} />
          ))}
        </Picker>

        {error && <Text style={styles.errorText}>{error}</Text>}

        <Button
          title="Register"
          onPress={handleRegister}
          loading={loading}
          disabled={loading}
        />

        <TouchableOpacity
          onPress={() => navigation.navigate('Login')}
          disabled={loading}
        >
          <Text style={styles.linkText}>
            Already have an account? <Text style={styles.linkBold}>Login</Text>
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
    paddingTop: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  formCard: {
    marginHorizontal: 16,
    marginBottom: 32,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  picker: {
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
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

export default RegisterScreen;
