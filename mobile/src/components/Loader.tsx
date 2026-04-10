import { ActivityIndicator, Text, View } from "react-native";

export default function Loader({ message }: { message?: string }) {
  return (
    <View className="flex-1 items-center justify-center bg-background px-6">
      <ActivityIndicator size="large" color="#1E88E5" />
      {message ? (
        <View className="mt-3">
          <Text className="text-sm text-slate-600">{message}</Text>
        </View>
      ) : null}
    </View>
  );
}
