import { Text, View } from "react-native";

export default function EligibilityCard({
  eligible,
  reason,
  missing,
}: {
  eligible: boolean;
  reason: string;
  missing: string[];
}) {
  return (
    <View className="rounded-xl bg-white p-5 shadow-soft">
      <View className="flex-row items-center justify-between">
        <Text className="text-lg font-semibold text-slate-900">Eligibility</Text>
        <View
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            eligible ? "bg-emerald-100" : "bg-rose-100"
          }`}
        >
          <Text className={`${eligible ? "text-emerald-700" : "text-rose-700"}`}>
            {eligible ? "Eligible" : "Not eligible"}
          </Text>
        </View>
      </View>
      <View className="mt-3">
        <Text className="text-sm font-medium text-slate-700">Reason</Text>
        <Text className="mt-1 text-sm text-slate-600">{reason}</Text>
      </View>
      {missing.length ? (
        <View className="mt-3">
          <Text className="text-sm font-medium text-slate-700">Missing requirements</Text>
          {missing.map((item) => (
            <Text key={item} className="mt-1 text-sm text-slate-600">
              • {item}
            </Text>
          ))}
        </View>
      ) : null}
    </View>
  );
}
