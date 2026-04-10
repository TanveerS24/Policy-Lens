import { useState } from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { login } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import type { AuthStackParamList } from "../navigation/types";

export default function LoginScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <View className="flex-1 bg-background px-6 pt-16">
      <Text className="text-3xl font-semibold text-slate-900">Welcome back</Text>
      <Text className="mt-2 text-sm text-slate-600">Log in to access your policies and eligibility assistant.</Text>

      <View className="mt-10">
        <InputField label="Email" value={email} onChangeText={setEmail} placeholder="you@example.com" keyboardType="email-address" />
        <InputField
          label="Password"
          value={password}
          onChangeText={setPassword}
          placeholder="••••••••"
          secureTextEntry
        />

        {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}

        {loading ? (
          <Loader />
        ) : (
          <Button
            label="Log in"
            onPress={() => dispatch(login({ email, password }))}
            variant="primary"
          />
        )}

        <View className="mt-5 flex-row justify-center">
          <Text className="text-sm text-slate-600">Don’t have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate("Register") }>
            <Text className="ml-2 text-sm font-semibold text-primary">Sign up</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
