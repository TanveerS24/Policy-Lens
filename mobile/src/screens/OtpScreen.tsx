import { useState } from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import api from "../services/api";
import type { AuthStackParamList } from "../navigation/types";

export default function OtpScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const verify = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      await api.post("/auth/verify-otp", { email, otp });
      setMessage("Verification successful. You can now use the app.");
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Unable to verify OTP");
    } finally {
      setLoading(false);
    }
  };

  const resend = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      await api.post("/auth/register", { email, password: "", name: "", age: 0, gender: "", state: "" });
      setMessage("OTP resent. Check your email.");
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Unable to resend OTP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-background px-6 pt-16">
      <Text className="text-3xl font-semibold text-slate-900">Verify your account</Text>
      <Text className="mt-2 text-sm text-slate-600">Enter the code sent to your email.</Text>

      <View className="mt-10">
        <InputField label="Email" value={email} onChangeText={setEmail} placeholder="you@example.com" keyboardType="email-address" />
        <InputField label="OTP" value={otp} onChangeText={setOtp} placeholder="123456" keyboardType="numeric" />

        {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}
        {message ? <Text className="mb-2 text-sm text-emerald-600">{message}</Text> : null}

        <Button label="Verify" onPress={verify} variant="primary" />
        <TouchableOpacity onPress={resend} className="mt-4">
          <Text className="text-center text-sm font-semibold text-primary">Resend OTP</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.navigate("Login")} className="mt-6">
          <Text className="text-center text-sm text-slate-600">Back to login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
