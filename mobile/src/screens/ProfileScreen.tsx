import { Alert, Text, View } from "react-native";

import Button from "../components/Button";
import { logout } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";

export default function ProfileScreen() {
  const dispatch = useAppDispatch();
  const auth = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  const handleDelete = () => {
    Alert.alert(
      "Delete account",
      "This will remove your account from the app. This action cannot be undone.",
      [
        { text: "Cancel", style: "cancel" },
        { text: "Delete", style: "destructive", onPress: () => handleLogout() },
      ]
    );
  };

  return (
    <View className="flex-1 bg-background px-6 py-8">
      <Text className="text-2xl font-semibold text-slate-900">Profile</Text>
      <Text className="mt-1 text-sm text-slate-600">Manage your account details and preferences.</Text>

      <View className="mt-8 rounded-xl bg-white p-5 shadow-soft">
        <Text className="text-base font-semibold text-slate-900">Account</Text>
        <View className="mt-4 space-y-3">
          <View>
            <Text className="text-xs font-semibold text-slate-500">Email</Text>
            <Text className="text-base text-slate-900">{auth.user?.email ?? "—"}</Text>
          </View>
          <View>
            <Text className="text-xs font-semibold text-slate-500">Name</Text>
            <Text className="text-base text-slate-900">{auth.user?.name ?? "—"}</Text>
          </View>
        </View>
      </View>

      <View className="mt-8 space-y-3">
        <Button label="Edit profile" onPress={() => {}} variant="outline" />
        <Button label="Logout" onPress={handleLogout} variant="secondary" />
        <Button label="Delete account" onPress={handleDelete} variant="outline" />
      </View>
    </View>
  );
}
