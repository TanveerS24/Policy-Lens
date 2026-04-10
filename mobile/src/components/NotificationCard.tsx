import { Text, View } from "react-native";

export default function NotificationCard({ title, message }: { title: string; message: string }) {
  return (
    <View className="mb-3 rounded-xl bg-white p-4 shadow-soft">
      <Text className="text-base font-semibold text-slate-900">{title}</Text>
      <Text className="mt-1 text-sm text-slate-600">{message}</Text>
    </View>
  );
}
