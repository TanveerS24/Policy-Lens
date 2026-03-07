import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  Alert,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { verifyOTP } from '../../store/authSlice';
import { Button, Card, Loading } from '../../components/ui';
import { COLORS } from '../../config/api';

const OTPVerificationScreen = ({ route, navigation }) => {
  const [otp, setOtp] = useState('');
  const [timer, setTimer] = useState(300); // 5 minutes
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state) => state.auth);
  const email = route.params?.email || '';

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((t) => (t > 0 ? t - 1 : 0));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleVerifyOTP = async () => {
    if (!otp || otp.length !== 6) {
      Alert.alert('Validation', 'Please enter a valid 6-digit OTP');
      return;
    }

    const result = await dispatch(
      verifyOTP({
        email,
        otp,
      })
    );

    if (verifyOTP.fulfilled.match(result)) {
      Alert.alert('Success', 'Account created successfully!');
      // Navigation happens automatically on auth state change
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  if (loading) return <Loading />;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={styles.title}>Verify OTP</Text>
        <Text style={styles.subtitle}>
          We've sent a verification code to {email}
        </Text>
      </View>

      <Card style={styles.formCard}>
        <Text style={styles.label}>Enter OTP</Text>
        <TextInput
          style={styles.otpInput}
          placeholder="000000"
          value={otp}
          onChangeText={setOtp}
          keyboardType="numeric"
          maxLength={6}
          editable={!loading && timer > 0}
        />

        <Text style={styles.timerText}>
          {timer > 0 ? `Expires in: ${formatTime(timer)}` : 'OTP Expired'}
        </Text>

        {error && <Text style={styles.errorText}>{error}</Text>}

        <Button
          title="Verify OTP"
          onPress={handleVerifyOTP}
          loading={loading}
          disabled={loading || timer === 0 || otp.length !== 6}
        />

        <Button
          title="Resend OTP"
          onPress={() => {
            setOtp('');
            setTimer(300);
          }}
          disabled={loading || timer > 250}
          variant="secondary"
        />
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
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
    color: COLORS.text,
  },
  otpInput: {
    borderWidth: 2,
    borderColor: COLORS.primary,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 16,
    marginBottom: 16,
    fontSize: 24,
    textAlign: 'center',
    letterSpacing: 8,
    fontWeight: '600',
  },
  timerText: {
    textAlign: 'center',
    fontSize: 14,
    color: COLORS.warning,
    marginBottom: 16,
    fontWeight: '600',
  },
  errorText: {
    color: COLORS.error,
    marginBottom: 12,
    fontSize: 14,
    textAlign: 'center',
  },
});

export default OTPVerificationScreen;
