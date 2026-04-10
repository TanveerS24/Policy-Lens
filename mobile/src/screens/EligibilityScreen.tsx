import { useEffect, useMemo, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import { useRoute } from "@react-navigation/native";
import { useSelector } from "react-redux";

import Button from "../components/Button";
import EligibilityCard from "../components/EligibilityCard";
import InputField from "../components/InputField";
import Loader from "../components/Loader";
import { checkEligibility } from "../services/policyService";
import { RootState } from "../redux/store";

type RouteParams = {
  policyId: string;
};

export default function EligibilityScreen() {
  const route = useRoute();
  const { policyId } = route.params as RouteParams;
  const auth = useSelector((state: RootState) => state.auth);

  const [mode, setMode] = useState<"me" | "someone">("me");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("male");
  const [state, setState] = useState("");
  const [income, setIncome] = useState("");
  const [result, setResult] = useState<{ eligible: boolean; reason: string; missing_requirements: string[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const profile = useMemo(() => {
    if (mode === "me") {
      return {
        age: Number(age) || 0,
        gender,
        state,
        income: income ? Number(income) : undefined,
      };
    }
    return {
      age: Number(age) || 0,
      gender,
      state,
      income: income ? Number(income) : undefined,
    };
  }, [age, gender, state, income, mode]);

  useEffect(() => {
    // populate defaults from auth if available
    if (auth.user) {
      setState((prev) => prev || "");
    }
  }, [auth.user]);

  const runCheck = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await checkEligibility(policyId, profile);
      setResult(response);
    } catch (err) {
      setError("Unable to check eligibility.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView className="bg-background" contentContainerStyle={{ padding: 16, paddingBottom: 32 }}>
      <Text className="text-2xl font-semibold text-slate-900">Check eligibility</Text>
      <Text className="mt-1 text-sm text-slate-600">Answer a few questions and see results instantly.</Text>

      <View className="mt-6 flex-row gap-3">
        <Button label="For me" onPress={() => setMode("me")} variant={mode === "me" ? "primary" : "outline"} style={{ flex: 1 }} />
        <Button label="For someone else" onPress={() => setMode("someone")} variant={mode === "someone" ? "primary" : "outline"} style={{ flex: 1 }} />
      </View>

      <View className="mt-6 rounded-xl bg-white p-4 shadow-soft">
        <Text className="text-base font-semibold text-slate-900">Profile</Text>
        <InputField label="Age" value={age} onChangeText={setAge} placeholder="e.g. 32" keyboardType="numeric" />
        <InputField label="Gender" value={gender} onChangeText={setGender} placeholder="male / female" />
        <InputField label="State" value={state} onChangeText={setState} placeholder="e.g. California" />
        <InputField label="Income" value={income} onChangeText={setIncome} placeholder="Optional" keyboardType="numeric" />
      </View>

      {error ? <Text className="mt-3 text-sm text-rose-600">{error}</Text> : null}

      <View className="mt-6">
        <Button label="Check eligibility" onPress={runCheck} variant="primary" />
      </View>

      {loading ? (
        <Loader />
      ) : result ? (
        <View className="mt-6">
          <EligibilityCard eligible={result.eligible} reason={result.reason} missing={result.missing_requirements} />
        </View>
      ) : null}
    </ScrollView>
  );
}
