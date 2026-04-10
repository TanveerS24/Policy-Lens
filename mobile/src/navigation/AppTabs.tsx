import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { MaterialIcons } from "@expo/vector-icons";

import HomeScreen from "../screens/HomeScreen";
import PoliciesScreen from "../screens/PoliciesScreen";
import UploadScreen from "../screens/UploadScreen";
import MyUploadsScreen from "../screens/MyUploadsScreen";
import ProfileScreen from "../screens/ProfileScreen";
import type { AppTabsParamList } from "./types";

const Tab = createBottomTabNavigator<AppTabsParamList>();

export default function AppTabs() {
  return (
    <Tab.Navigator
      id="AppTabs"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: { backgroundColor: "#ffffff" },
        tabBarActiveTintColor: "#1E88E5",
        tabBarInactiveTintColor: "#64748b",
        tabBarIcon: ({ color, size }) => {
          let iconName: keyof typeof MaterialIcons.glyphMap = "home";
          if (route.name === "Policies") iconName = "description";
          if (route.name === "Upload") iconName = "cloud-upload";
          if (route.name === "MyUploads") iconName = "folder";
          if (route.name === "Profile") iconName = "person";
          return <MaterialIcons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Policies" component={PoliciesScreen} />
      <Tab.Screen name="Upload" component={UploadScreen} />
      <Tab.Screen name="MyUploads" component={MyUploadsScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
