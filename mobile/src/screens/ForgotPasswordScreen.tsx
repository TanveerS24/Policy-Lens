import { useState } from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { requestOTP, verifyOTP, resetPassword } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import type { AuthStackParamList } from "../navigation/types";

export default function ForgotPasswordScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  const [step, setStep] = useState(1); // 1: Mobile, 2: OTP, 3: New Password
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [timer, setTimer] = useState(0);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleRequestOTP = () => {
    dispatch(requestOTP({ mobile, purpose: "password_reset" }));
    setOtpSent(true);
    setTimer(60);
    const interval = setInterval(() => {
      setTimer((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleVerifyOTP = () => {
    dispatch(verifyOTP({ mobile, otp, purpose: "password_reset" }));
    setStep(3);
  };

  const handleResetPassword = () => {
    if (newPassword !== confirmPassword) {
      dispatch({ type: "auth/resetPassword/failed", error: "Passwords do not match" });
      return;
    }
    dispatch(resetPassword({ mobile, new_password: newPassword }));
  };

  return (
    <View className="flex-1 bg-background px-6 pt-16">
      <Text className="text-3xl font-semibold text-slate-900">Reset Password</Text>
      <Text className="mt-2 text-sm text-slate-600">Enter your mobile number to reset your password.</Text>

      {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}

      {loading ? (
        <Loader />
      ) : (
        <>
          {step === 1 && (
            <View className="mt-10">
              <InputField
                label="Mobile Number"
                value={mobile}
                onChangeText={setMobile}
                placeholder="+91 XXXXX XXXXX"
                keyboardType="phone-pad"
                maxLength={13}
              />

              <Button
                label="Send OTP"
                onPress={handleRequestOTP}
                variant="primary"
                disabled={!mobile || mobile.length < 10}
              />
            </View>
          )}

          {step === 2 && (
            <View className="mt-10">
              <InputField
                label="Enter OTP"
                value={otp}
                onChangeText={setOtp}
                placeholder="6-digit OTP"
                keyboardType="numeric"
                maxLength={6}
              />

              <Button
                label="Verify OTP"
                onPress={handleVerifyOTP}
                variant="primary"
                disabled={!otp || otp.length < 6}
              />

              {timer > 0 ? (
                <Text className="mt-3 text-center text-sm text-slate-500">Resend OTP in {timer}s</Text>
              ) : (
                <TouchableOpacity onPress={handleRequestOTP} className="mt-3">
                  <Text className="text-center text-sm font-semibold text-primary">Resend OTP</Text>
                </TouchableOpacity>
              )}
            </View>
          )}

          {step === 3 && (
            <View className="mt-10">
              <InputField
                label="New Password"
                value={newPassword}
                onChangeText={setNewPassword}
                placeholder="Min 8 chars, 1 uppercase, 1 number, 1 special"
                secureTextEntry
              />
              <InputField
                label="Confirm New Password"
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                placeholder="Re-enter new password"
                secureTextEntry
              />

              <Button
                label="Reset Password"
                onPress={handleResetPassword}
                variant="primary"
                disabled={!newPassword || !confirmPassword || newPassword.length < 8}
              />
            </View>
          )}
        </>
      )}

      <TouchableOpacity onPress={() => navigation.goBack()} className="mt-5">
        <Text className="text-center text-sm text-primary">Back to Login</Text>
      </TouchableOpacity>
    </View>
  );
}
