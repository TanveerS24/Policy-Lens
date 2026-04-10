import { useEffect, useRef, useState } from "react";
import { FlatList, KeyboardAvoidingView, Platform, Text, TextInput, TouchableOpacity, View } from "react-native";
import { useRoute } from "@react-navigation/native";

import ChatBubble from "../components/ChatBubble";
import Loader from "../components/Loader";
import { askQuestion } from "../services/policyService";

type RouteParams = {
  policyId: string;
};

type Message = {
  id: string;
  fromUser: boolean;
  text: string;
};

export default function AskAiScreen() {
  const route = useRoute();
  const { policyId } = route.params as RouteParams;
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const flatRef = useRef<FlatList>(null);

  useEffect(() => {
    setMessages([
      {
        id: "welcome",
        fromUser: false,
        text: "Ask a question about this policy and get an AI answer.",
      },
    ]);
  }, []);

  const send = async () => {
    if (!input.trim()) return;
    const messageId = `${Date.now()}`;

    setMessages((prev) => [...prev, { id: messageId, fromUser: true, text: input.trim() }]);
    setLoading(true);
    setInput("");

    try {
      const response = await askQuestion(policyId, input.trim());
      setMessages((prev) => [...prev, { id: `${messageId}-reply`, fromUser: false, text: response.answer }]);
    } catch (err) {
      setMessages((prev) => [...prev, { id: `${messageId}-reply`, fromUser: false, text: "Unable to get an answer right now." }]);
    } finally {
      setLoading(false);
      flatRef.current?.scrollToEnd({ animated: true });
    }
  };

  return (
    <KeyboardAvoidingView
      className="flex-1 bg-background"
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={90}
    >
      <View className="flex-1 px-4 py-6">
        <Text className="text-2xl font-semibold text-slate-900">Ask AI</Text>
        <Text className="mt-1 text-sm text-slate-600">Ask anything about the policy and receive explainable answers.</Text>

        <FlatList
          ref={flatRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <ChatBubble message={item.text} fromUser={item.fromUser} />}
          contentContainerStyle={{ paddingTop: 16 }}
        />

        {loading && <Loader message="Thinking..." />}

        <View className="mt-auto flex-row items-center gap-2">
          <TextInput
            className="flex-1 rounded-2xl bg-white px-4 py-3 text-base text-slate-900 shadow-soft"
            placeholder="Ask a question..."
            value={input}
            onChangeText={setInput}
          />
          <TouchableOpacity onPress={send} className="rounded-full bg-primary px-4 py-3">
            <Text className="text-white">Send</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
