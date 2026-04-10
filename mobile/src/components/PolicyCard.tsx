import { Pressable, Text, View } from "react-native";
import { Policy } from "../types";

type Props = {
  policy: Policy;
  onPress: () => void;
};

export default function PolicyCard({ policy, onPress }: Props) {
  return (
    <Pressable onPress={onPress} className="mb-4 rounded-xl bg-white p-4 shadow-soft">
      <View className="flex-row items-start justify-between">
        <View className="flex-1">
          <Text className="text-base font-semibold text-slate-900">{policy.title}</Text>
          {policy.short_description ? (
            <Text className="mt-2 text-sm text-slate-600">{policy.short_description}</Text>
          ) : null}
        </View>
        <View className="ml-3 items-end">
          <Text className="rounded-full bg-primary/15 px-3 py-1 text-xs font-semibold text-primary">
            {policy.category ?? "General"}
          </Text>
          {policy.state ? (
            <Text className="mt-2 text-xs text-slate-500">{policy.state}</Text>
          ) : null}
        </View>
      </View>
    </Pressable>
  );
}
