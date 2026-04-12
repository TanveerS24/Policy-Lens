import { useState } from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { requestOTP, verifyOTP } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import type { AuthStackParamList } from "../navigation/types";

export default function LoginScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [timer, setTimer] = useState(0);

  const handleRequestOTP = () => {
    dispatch(requestOTP({ mobile, purpose: "login" }));
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
    dispatch(verifyOTP({ mobile, otp, purpose: "login" }));
  };

  return (
    <View className="flex-1 bg-background px-6 pt-16">
      <Text className="text-3xl font-semibold text-slate-900">Welcome back</Text>
      <Text className="mt-2 text-sm text-slate-600">Log in with your mobile number to access your policies and eligibility assistant.</Text>

      <View className="mt-10">
        <InputField
          label="Mobile Number"
          value={mobile}
          onChangeText={setMobile}
          placeholder="+91 XXXXX XXXXX"
          keyboardType="phone-pad"
          maxLength={13}
          editable={!otpSent}
        />

        {otpSent && (
          <InputField
            label="OTP"
            value={otp}
            onChangeText={setOtp}
            placeholder="Enter 6-digit OTP"
            keyboardType="numeric"
            maxLength={6}
          />
        )}

        {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}

        {loading ? (
          <Loader />
        ) : (
          <>
            {!otpSent ? (
              <Button
                label="Send OTP"
                onPress={handleRequestOTP}
                variant="primary"
                disabled={!mobile || mobile.length < 10}
              />
            ) : (
              <>
                <Button
                  label="Verify & Login"
                  onPress={handleVerifyOTP}
                  variant="primary"
                  disabled={!otp || otp.length < 6}
                />
                {timer > 0 ? (
                  <Text className="mt-3 text-center text-sm text-slate-500">Resend OTP in {timer}s</Text>
                ) : (
                  <TouchableOpacity onPress={handleRequestOTP}>
                    <Text className="mt-3 text-center text-sm font-semibold text-primary">Resend OTP</Text>
                  </TouchableOpacity>
                )}
              </>
            )}
          </>
        )}

        <View className="mt-5 flex-row justify-center">
          <Text className="text-sm text-slate-600">New to DentalSchemes?</Text>
          <TouchableOpacity onPress={() => navigation.navigate("Register")}>
            <Text className="ml-2 text-sm font-semibold text-primary">Sign up</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity onPress={() => navigation.navigate("ForgotPassword")} className="mt-4">
          <Text className="text-center text-sm text-primary">Forgot Password?</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
