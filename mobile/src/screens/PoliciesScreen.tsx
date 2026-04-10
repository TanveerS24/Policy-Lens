import { useEffect, useState } from "react";
import { FlatList, Text, View, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import PolicyCard from "../components/PolicyCard";
import Loader from "../components/Loader";
import EmptyState from "../components/EmptyState";
import { fetchPolicies } from "../services/policyService";
import { Policy } from "../types";
import type { MainStackParamList } from "../navigation/types";

export default function PoliciesScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<MainStackParamList>>();
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        const data = await fetchPolicies();
        setPolicies(data);
      } catch (err) {
        setError("Unable to load policies");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <View className="flex-1 bg-background px-4 py-6">
      <View className="flex-row items-center justify-between">
        <Text className="text-2xl font-semibold text-slate-900">Policies</Text>
        <TouchableOpacity className="rounded-xl bg-white px-4 py-2 shadow-soft">
          <Text className="text-sm font-semibold text-primary">Filter</Text>
        </TouchableOpacity>
      </View>
      <Text className="mt-1 text-sm text-slate-600">Browse policies and check your eligibility.</Text>

      <View className="mt-6 flex-1">
        {loading ? (
          <Loader />
        ) : error ? (
          <Text className="mt-4 text-sm text-rose-600">{error}</Text>
        ) : policies.length === 0 ? (
          <EmptyState message="No policies found. Try again later." />
        ) : (
          <FlatList
            data={policies.slice(0, 10)}
            keyExtractor={(item) => item._id}
            renderItem={({ item }) => (
              <PolicyCard
                policy={item}
                onPress={() => navigation.navigate("PolicyDetails", { policyId: item._id })}
              />
            )}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={{ paddingTop: 12, paddingBottom: 24 }}
          />
        )}
      </View>
    </View>
  );
}
