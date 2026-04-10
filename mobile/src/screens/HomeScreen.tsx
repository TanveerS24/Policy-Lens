import { useEffect, useState } from "react";
import { FlatList, Text, View } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

import NotificationCard from "../components/NotificationCard";
import PolicyCard from "../components/PolicyCard";
import Loader from "../components/Loader";
import { fetchPolicies } from "../services/policyService";
import { Policy } from "../types";
import type { MainStackParamList } from "../navigation/types";

export default function HomeScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<MainStackParamList>>();
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        const data = await fetchPolicies();
        setPolicies(data.slice(0, 5));
      } catch (err) {
        setError("Unable to load policies");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <View className="flex-1 bg-background px-4 py-6">
      <Text className="text-2xl font-semibold text-slate-900">PolicyLens</Text>
      <Text className="mt-1 text-sm text-slate-600">Stay informed. Verify eligibility. Ask AI.</Text>

      <View className="mt-6">
        <Text className="text-lg font-semibold text-slate-900">Notifications</Text>
        <NotificationCard title="New policy available" message="A new healthcare policy has been published." />
      </View>

      <View className="mt-6 flex-1">
        <View className="flex-row items-center justify-between">
          <Text className="text-lg font-semibold text-slate-900">New policies</Text>
          <Text className="text-sm font-medium text-primary">View all</Text>
        </View>
        {loading ? (
          <Loader />
        ) : error ? (
          <Text className="mt-4 text-sm text-rose-600">{error}</Text>
        ) : (
          <FlatList
            data={policies}
            keyExtractor={(item) => item._id}
            renderItem={({ item }) => (
              <PolicyCard
                policy={item}
                onPress={() => navigation.navigate("PolicyDetails", { policyId: item._id })}
              />
            )}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={{ paddingTop: 12 }}
          />
        )}
      </View>
    </View>
  );
}
