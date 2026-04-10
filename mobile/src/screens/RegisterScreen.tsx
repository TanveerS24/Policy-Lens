import { useState } from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import Button from "../components/Button";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { register } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import type { AuthStackParamList } from "../navigation/types";

export default function RegisterScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<AuthStackParamList>>();
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("male");
  const [state, setState] = useState("");
  const [income, setIncome] = useState("");

  const handleRegister = () => {
    dispatch(
      register({
        name,
        email,
        password,
        age: Number(age),
        gender,
        state,
        income: income ? Number(income) : undefined,
      })
    );
  };

  return (
    <View className="flex-1 bg-background px-6 pt-12">
      <Text className="text-3xl font-semibold text-slate-900">Create account</Text>
      <Text className="mt-2 text-sm text-slate-600">Fill in your details to get started.</Text>

      <View className="mt-8">
        <InputField label="Full name" value={name} onChangeText={setName} placeholder="Your name" />
        <InputField label="Email" value={email} onChangeText={setEmail} placeholder="you@example.com" keyboardType="email-address" />
        <InputField label="Password" value={password} onChangeText={setPassword} placeholder="••••••••" secureTextEntry />
        <InputField label="Age" value={age} onChangeText={setAge} placeholder="e.g. 30" keyboardType="numeric" />
        <InputField label="Gender" value={gender} onChangeText={setGender} placeholder="male / female / other" />
        <InputField label="State" value={state} onChangeText={setState} placeholder="e.g. California" />
        <InputField label="Income (optional)" value={income} onChangeText={setIncome} placeholder="e.g. 56000" keyboardType="numeric" />

        {error ? <Text className="mb-2 text-sm text-rose-600">{error}</Text> : null}

        {loading ? (
          <Loader />
        ) : (
          <Button label="Create account" onPress={handleRegister} variant="primary" />
        )}

        <View className="mt-5 flex-row justify-center">
          <Text className="text-sm text-slate-600">Already have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate("Login") }>
            <Text className="ml-2 text-sm font-semibold text-primary">Sign in</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
