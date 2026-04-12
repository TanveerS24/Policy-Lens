import { useState } from "react";
import { Alert, Text, View, TouchableOpacity, ScrollView } from "react-native";

import Button from "../components/Button";
import InputField from "../components/InputField";
import { logout } from "../redux/slices/authSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import Loader from "../components/Loader";

const API_BASE_URL = "http://localhost:8000";

export default function ProfileScreen() {
  const dispatch = useAppDispatch();
  const auth = useAppSelector((state) => state.auth);
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);

  const [fullName, setFullName] = useState(auth.user?.name || "");
  const [email, setEmail] = useState(auth.user?.email || "");

  const handleLogout = () => {
    dispatch(logout());
  };

  const handleUpdateProfile = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/patients/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${auth.tokens?.access_token || ""}`,
        },
        body: JSON.stringify({
          full_name: fullName,
          email,
        }),
      });
      if (response.ok) {
        setEditing(false);
        Alert.alert("Success", "Profile updated successfully");
      } else {
        Alert.alert("Error", "Failed to update profile");
      }
    } catch (error) {
      Alert.alert("Error", "Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="px-6 py-8">
        <Text className="text-2xl font-semibold text-slate-900">Profile</Text>
        <Text className="mt-1 text-sm text-slate-600">Manage your account details and preferences.</Text>

        <View className="mt-8 rounded-xl bg-white p-5 shadow-soft">
          <View className="flex-row items-center justify-between">
            <Text className="text-base font-semibold text-slate-900">Account Details</Text>
            <TouchableOpacity onPress={() => setEditing(!editing)}>
              <Text className="text-sm font-semibold text-primary">{editing ? "Cancel" : "Edit"}</Text>
            </TouchableOpacity>
          </View>

          <View className="mt-4 space-y-3">
            {editing ? (
              <>
                <InputField label="Full Name" value={fullName} onChangeText={setFullName} placeholder="Your full name" />
                <InputField label="Email" value={email} onChangeText={setEmail} placeholder="you@example.com" keyboardType="email-address" />
                {loading ? <Loader /> : <Button label="Save Changes" onPress={handleUpdateProfile} variant="primary" />}
              </>
            ) : (
              <>
                <View>
                  <Text className="text-xs font-semibold text-slate-500">Name</Text>
                  <Text className="text-base text-slate-900">{auth.user?.name ?? "—"}</Text>
                </View>
                <View>
                  <Text className="text-xs font-semibold text-slate-500">Email</Text>
                  <Text className="text-base text-slate-900">{auth.user?.email ?? "—"}</Text>
                </View>
              </>
            )}
          </View>
        </View>

        <View className="mt-8 space-y-3">
          <Button label="Logout" onPress={handleLogout} variant="secondary" />
        </View>
      </View>
    </ScrollView>
  );
}
