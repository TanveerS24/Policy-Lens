import { Text, View } from "react-native";

export default function ChatBubble({ message, fromUser }: { message: string; fromUser?: boolean }) {
  return (
    <View className={`mb-3 flex-row ${fromUser ? "justify-end" : "justify-start"}`}>
      <View
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-soft ${
          fromUser ? "bg-primary" : "bg-white"
        }`}
      >
        <Text className={`${fromUser ? "text-white" : "text-slate-800"}`}>{message}</Text>
      </View>
    </View>
  );
}
