import { createNativeStackNavigator } from "@react-navigation/native-stack";

import AppTabs from "./AppTabs";
import PolicyDetailsScreen from "../screens/PolicyDetailsScreen";
import EligibilityScreen from "../screens/EligibilityScreen";
import AskAiScreen from "../screens/AskAiScreen";
import type { MainStackParamList } from "./types";

const Stack = createNativeStackNavigator<MainStackParamList>();

export default function MainStack() {
  return (
    <Stack.Navigator id="MainStack" screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Tabs" component={AppTabs} />
      <Stack.Screen name="PolicyDetails" component={PolicyDetailsScreen} />
      <Stack.Screen name="Eligibility" component={EligibilityScreen} />
      <Stack.Screen name="AskAi" component={AskAiScreen} />
    </Stack.Navigator>
  );
}
