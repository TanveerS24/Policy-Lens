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

  const { email: paramEmail, mobile: paramMobile, purpose, nextScreen, userData, devOtp } = route.params;

  const targetEmail = paramEmail || userData?.email || '';
  const targetMobile = paramMobile || userData?.mobile || '';

  const [method, setMethod] = useState<'email' | 'mobile'>('email');
  const [otp, setOtp] = useState<string[]>(['', '', '', '', '', '']);
  const [timer, setTimer] = useState(60);
  const [snackbarVisible, setSnackbarVisible] = useState(false);

  const inputRefs = useRef<(RNTextInput | null)[]>([]);

  useEffect(() => {
    if (devOtp && devOtp.length === 6) {
      setOtp(devOtp.split(''));
    }
  }, [devOtp]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleSelectMobileMethod = () => {
    toast.show('Phone Number OTP verification is coming soon. Using Email OTP as primary.', {
      type: 'warning',
      placement: 'top',
      duration: 4000,
    });
  };

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
        email: method === 'email' ? targetEmail : undefined,
        mobile: method === 'mobile' ? targetMobile : undefined,
        otp: otpCode, 
        purpose, 
        userData: purpose === 'registration' ? userData : undefined 
      }) as any).unwrap();
      
      if (result.verified) {
        toast.show('OTP verified successfully! Redirecting...', {
          type: 'success',
          placement: 'top',
        });
        
        // Add 2-second delay before navigation
        setTimeout(() => {
          if (nextScreen === 'Main') {
            navigation.replace('Main');
          } else {
            navigation.replace(nextScreen as any);
          }
        }, 2000);
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
      toast.show(`OTP resent to ${targetEmail || 'your email'}`, {
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
              Enter the 6-digit code sent to{' '}
              <Text style={{ fontWeight: 'bold', color: colors.primary }}>
                {method === 'email' 
                  ? (targetEmail || 'your email') 
                  : (targetMobile || 'your mobile number')}
              </Text>
            </Text>

            {devOtp && (
              <View style={styles.devBanner}>
                <Text style={styles.devBannerText}>
                  Dev Mode OTP: <Text style={styles.devBannerCode}>{devOtp}</Text>
                </Text>
              </View>
            )}
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
            Verify & Proceed
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
              {timer > 0 ? `Resend in ${timer}s` : 'Resend Code'}
            </Button>
          </View>

          <View style={styles.switchMethodContainer}>
            {method === 'email' ? (
              <Button
                mode="text"
                onPress={handleSelectMobileMethod}
                icon="cellphone-message"
                textColor={colors.primary}
                labelStyle={{ fontSize: 13, fontWeight: '600' }}
              >
                {targetMobile ? `Send code to mobile (${targetMobile})` : 'Send code to mobile number'}
              </Button>
            ) : (
              <Button
                mode="text"
                onPress={() => setMethod('email')}
                icon="email-outline"
                textColor={colors.primary}
                labelStyle={{ fontSize: 13, fontWeight: '600' }}
              >
                {targetEmail ? `Send code to email (${targetEmail})` : 'Send code to email address'}
              </Button>
            )}
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
    paddingHorizontal: 16,
    paddingVertical: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 28,
  },
  title: {
    color: colors.primary,
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center',
  },
  subtitle: {
    color: colors.textSecondary,
    textAlign: 'center',
    paddingHorizontal: 8,
  },
  devBanner: {
    marginTop: 12,
    paddingVertical: 6,
    paddingHorizontal: 16,
    backgroundColor: colors.primaryContainer || 'rgba(37, 99, 235, 0.15)',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  devBannerText: {
    color: colors.primary,
    fontSize: 13,
    fontWeight: '500',
  },
  devBannerCode: {
    fontWeight: 'bold',
    fontSize: 14,
    letterSpacing: 2,
  },
  otpContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 28,
    paddingHorizontal: 4,
  },
  otpInput: {
    width: 44,
    height: 52,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: 8,
    textAlign: 'center',
    fontSize: 22,
    fontWeight: 'bold',
    color: colors.textPrimary,
    backgroundColor: colors.cardBg,
  },
  verifyButton: {
    marginBottom: 16,
    borderRadius: 14,
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
  switchMethodContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
});
