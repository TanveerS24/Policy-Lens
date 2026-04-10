import { Text, View } from "react-native";

export default function EmptyState({ message }: { message: string }) {
  return (
    <View className="flex-1 items-center justify-center px-6">
      <View className="mb-4 h-20 w-20 items-center justify-center rounded-full bg-primary/10">
        <Text className="text-3xl">📄</Text>
      </View>
      <Text className="text-center text-base font-medium text-slate-600">{message}</Text>
    </View>
  );
}
