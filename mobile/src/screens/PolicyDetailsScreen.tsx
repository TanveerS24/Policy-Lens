import { useEffect, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { RouteProp } from "@react-navigation/native";

import Button from "../components/Button";
import Loader from "../components/Loader";
import { fetchPolicy } from "../services/policyService";
import { Policy } from "../types";
import type { MainStackParamList } from "../navigation/types";

export default function PolicyDetailsScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<MainStackParamList>>();
  const route = useRoute<RouteProp<MainStackParamList, "PolicyDetails">>();
  const { policyId } = route.params;

  const [policy, setPolicy] = useState<Policy | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        const data = await fetchPolicy(policyId);
        setPolicy(data);
      } catch (err) {
        setError("Unable to load policy details.");
      } finally {
        setLoading(false);
      }
    })();
  }, [policyId]);

  if (loading) {
    return <Loader />;
  }

  if (error || !policy) {
    return (
      <View className="flex-1 items-center justify-center px-6">
        <Text className="text-base font-semibold text-rose-600">{error ?? "Policy not found."}</Text>
      </View>
    );
  }

  return (
    <ScrollView className="bg-background" contentContainerStyle={{ padding: 16, paddingBottom: 32 }}>
      <Text className="text-2xl font-semibold text-slate-900">{policy.title}</Text>
      <Text className="mt-2 text-sm text-slate-600">{policy.short_description}</Text>

      <View className="mt-6 rounded-xl bg-white p-4 shadow-soft">
        <Text className="text-lg font-semibold text-slate-900">Summary</Text>
        <Text className="mt-2 text-sm text-slate-600">{policy.summary}</Text>
      </View>

      <View className="mt-4 rounded-xl bg-white p-4 shadow-soft">
        <Text className="text-lg font-semibold text-slate-900">Eligibility Criteria</Text>
        <Text className="mt-2 text-sm text-slate-600">{policy.eligibility_criteria}</Text>
      </View>

      <View className="mt-4 rounded-xl bg-white p-4 shadow-soft">
        <Text className="text-lg font-semibold text-slate-900">Benefits</Text>
        <Text className="mt-2 text-sm text-slate-600">{policy.benefits}</Text>
      </View>

      <View className="mt-6 flex-row gap-3">
        <Button
          label="Check eligibility"
          onPress={() => navigation.navigate("Eligibility", { policyId })}
          variant="primary"
          style={{ flex: 1 }}
        />
        <Button
          label="Ask AI"
          onPress={() => navigation.navigate("AskAi", { policyId })}
          variant="secondary"
          style={{ flex: 1 }}
        />
      </View>
    </ScrollView>
  );
}
