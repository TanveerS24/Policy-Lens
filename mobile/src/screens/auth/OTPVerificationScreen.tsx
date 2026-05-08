import React, { useState, useRef, useEffect } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, TextInput as RNTextInput } from 'react-native';
import { Text, Button, Snackbar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { verifyOTP, clearError } from '../../redux/slices/authSlice';
import { RootState, AppDispatch } from '../../redux/store';
import { useTheme } from '../../contexts/ThemeContext';
import { useToast } from 'react-native-toast-notifications';

type OTPVerificationRouteProp = RouteProp<RootStackParamList, 'OTPVerification'>;
type OTPVerificationNavigationProp = StackNavigationProp<RootStackParamList, 'OTPVerification'>;

export const OTPVerificationScreen: React.FC = () => {
  const navigation = useNavigation<OTPVerificationNavigationProp>();
  const route = useRoute<OTPVerificationRouteProp>();
  const dispatch = useDispatch<AppDispatch>();
  const { colors } = useTheme();
  const styles = createStyles(colors);
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  const toast = useToast();

  const { mobile, purpose, nextScreen, userData } = route.params;

  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [timer, setTimer] = useState(60);
  const [snackbarVisible, setSnackbarVisible] = useState(false);

  const inputRefs = useRef<(RNTextInput | null)[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleOtpChange = (index: number, value: string) => {
    if (value.length <= 1 && /^[0-9]*$/.test(value)) {
      const newOtp = [...otp];
      newOtp[index] = value;
      setOtp(newOtp);

      // Move to next input
      if (value && index < 5) {
        inputRefs.current[index + 1]?.focus();
      }

      // Check if OTP is complete
      if (index === 5 && value) {
        handleVerify(newOtp.join(''));
      }
    }
  };

  const handleKeyPress = (index: number, key: string) => {
    if (key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleVerify = async (otpCode: string) => {
    if (otpCode.length !== 6) {
      toast.show('Please enter a 6-digit OTP', {
        type: 'danger',
        placement: 'top',
      });
      return;
    }

    try {
      const result = await dispatch(verifyOTP({ 
        mobile, 
        otp: otpCode, 
        purpose, 
        userData: purpose === 'registration' ? userData : undefined 
      }) as any).unwrap();
      
      if (result.verified) {
        toast.show('OTP verified successfully! Redirecting...', {
          type: 'success',
          placement: 'top',
        });
        
        // Add 3-second delay before navigation
        setTimeout(() => {
          if (nextScreen === 'Main') {
            navigation.replace('Main');
          } else {
            navigation.replace(nextScreen as any);
          }
        }, 3000);
      }
    } catch (err: any) {
      toast.show('Invalid or expired OTP. Please try again.', {
        type: 'danger',
        placement: 'top',
      });
    }
  };

  const handleResend = async () => {
    if (timer > 0) return;

    try {
      // TODO: Implement resend OTP functionality
      // For now, just show a message
      toast.show('OTP resent successfully', {
        type: 'success',
        placement: 'top',
      });
      setTimer(60);
    } catch (error) {
      toast.show('Failed to resend OTP. Please try again.', {
        type: 'danger',
        placement: 'top',
      });
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <View style={styles.content}>
          <View style={styles.header}>
            <Text variant="displaySmall" style={styles.title}>
              Verify OTP
            </Text>
            <Text variant="bodyLarge" style={styles.subtitle}>
              Enter the 6-digit code sent to {mobile}
            </Text>
          </View>

          <View style={styles.otpContainer}>
            {otp.map((digit, index) => (
              <RNTextInput
                key={index}
                ref={(ref) => { inputRefs.current[index] = ref; }}
                style={styles.otpInput}
                value={digit}
                onChangeText={(value) => handleOtpChange(index, value)}
                onKeyPress={({ nativeEvent }) => handleKeyPress(index, nativeEvent.key)}
                keyboardType="number-pad"
                maxLength={1}
                selectTextOnFocus
              />
            ))}
          </View>

          <Button
            mode="contained"
            onPress={() => handleVerify(otp.join(''))}
            loading={isLoading}
            disabled={isLoading || otp.some(d => !d)}
            style={styles.verifyButton}
            contentStyle={styles.buttonContent}
          >
            Verify
          </Button>

          <View style={styles.resendContainer}>
            <Text variant="bodyMedium" style={styles.resendText}>
              Didn't receive the code?
            </Text>
            <Button
              mode="text"
              onPress={handleResend}
              disabled={timer > 0}
            >
              {timer > 0 ? `Resend in ${timer}s` : 'Resend'}
            </Button>
          </View>
        </View>
      </KeyboardAvoidingView>

      <Snackbar
        visible={snackbarVisible || !!error}
        onDismiss={() => {
          setSnackbarVisible(false);
          dispatch(clearError());
        }}
        duration={3000}
      >
        {error || 'Invalid OTP. Please try again.'}
      </Snackbar>
    </SafeAreaView>
  );
};

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  keyboardView: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    color: colors.primary,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    color: colors.textSecondary,
    textAlign: 'center',
  },
  otpContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 32,
  },
  otpInput: {
    width: 48,
    height: 56,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: 8,
    textAlign: 'center',
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.textPrimary,
    backgroundColor: colors.surface,
  },
  verifyButton: {
    marginBottom: 16,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  resendContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  resendText: {
    color: colors.textSecondary,
  },
});
