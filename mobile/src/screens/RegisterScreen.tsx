import { useState } from "react";
import { Text, View, TouchableOpacity, ScrollView } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { requestOTP, verifyOTP, register } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import type { AuthStackParamList } from "../navigation/types";

export default function RegisterScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  const [step, setStep] = useState(1); // 1: Details, 2: OTP, 3: Password
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [timer, setTimer] = useState(0);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [termsAccepted, setTermsAccepted] = useState(false);

  // Patient details per PRD
  const [fullName, setFullName] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [gender, setGender] = useState("");
  const [email, setEmail] = useState("");
  const [stateId, setStateId] = useState("");
  const [districtId, setDistrictId] = useState("");
  const [pinCode, setPinCode] = useState("");

  const handleRequestOTP = () => {
    dispatch(requestOTP({ mobile, purpose: "registration" }));
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
    dispatch(verifyOTP({ mobile, otp, purpose: "registration" }));
    setStep(3);
  };

  const handleRegister = () => {
    if (password !== confirmPassword) {
      dispatch({ type: "auth/register/failed", error: "Passwords do not match" });
      return;
    }
    dispatch(register({
      mobile,
      password,
      full_name: fullName,
      date_of_birth: dateOfBirth,
      gender,
      email,
      state_id: stateId,
      district_id: districtId,
      pin_code: pinCode,
    }));
  };

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="px-6 pt-12 pb-8">
        <Text className="text-3xl font-semibold text-slate-900">Create account</Text>
        <Text className="mt-2 text-sm text-slate-600">Fill in your details to get started with DentalSchemes India.</Text>

        {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}

        {loading ? (
          <Loader />
        ) : (
          <>
            {step === 1 && (
              <View className="mt-8">
                <InputField
                  label="Mobile Number *"
                  value={mobile}
                  onChangeText={setMobile}
                  placeholder="+91 XXXXX XXXXX"
                  keyboardType="phone-pad"
                  maxLength={13}
                />
                <InputField
                  label="Full Name *"
                  value={fullName}
                  onChangeText={setFullName}
                  placeholder="Your full name"
                />
                <InputField
                  label="Date of Birth *"
                  value={dateOfBirth}
                  onChangeText={setDateOfBirth}
                  placeholder="YYYY-MM-DD"
                />
                <InputField
                  label="Gender *"
                  value={gender}
                  onChangeText={setGender}
                  placeholder="Male / Female / Other"
                />
                <InputField
                  label="Email (Optional)"
                  value={email}
                  onChangeText={setEmail}
                  placeholder="you@example.com"
                  keyboardType="email-address"
                />
                <InputField
                  label="State *"
                  value={stateId}
                  onChangeText={setStateId}
                  placeholder="Select state"
                />
                <InputField
                  label="District *"
                  value={districtId}
                  onChangeText={setDistrictId}
                  placeholder="Select district"
                />
                <InputField
                  label="Pin Code *"
                  value={pinCode}
                  onChangeText={setPinCode}
                  placeholder="6-digit pin code"
                  keyboardType="numeric"
                  maxLength={6}
                />

                <TouchableOpacity onPress={() => setTermsAccepted(!termsAccepted)} className="mt-4 flex-row items-center">
                  <View className={`h-5 w-5 rounded border ${termsAccepted ? "bg-primary border-primary" : "border-slate-300"}`}>
                    {termsAccepted && <Text className="text-white text-xs">✓</Text>}
                  </View>
                  <Text className="ml-2 text-sm text-slate-600">I accept the Terms & Conditions</Text>
                </TouchableOpacity>

                <Button
                  label="Send OTP"
                  onPress={handleRequestOTP}
                  variant="primary"
                  disabled={!mobile || !fullName || !dateOfBirth || !gender || !stateId || !districtId || !pinCode || !termsAccepted}
                  className="mt-6"
                />
              </View>
            )}

            {step === 2 && (
              <View className="mt-8">
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
                  className="mt-6"
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
              <View className="mt-8">
                <InputField
                  label="Password *"
                  value={password}
                  onChangeText={setPassword}
                  placeholder="Min 8 chars, 1 uppercase, 1 number, 1 special"
                  secureTextEntry
                />
                <InputField
                  label="Confirm Password *"
                  value={confirmPassword}
                  onChangeText={setConfirmPassword}
                  placeholder="Re-enter password"
                  secureTextEntry
                />

                <Button
                  label="Create Account"
                  onPress={handleRegister}
                  variant="primary"
                  disabled={!password || !confirmPassword || password.length < 8}
                  className="mt-6"
                />
              </View>
            )}
          </>
        )}

        <View className="mt-5 flex-row justify-center">
          <Text className="text-sm text-slate-600">Already have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate("Login")}>
            <Text className="ml-2 text-sm font-semibold text-primary">Sign in</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}
