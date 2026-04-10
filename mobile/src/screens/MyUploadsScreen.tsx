import { useEffect, useState } from "react";
import { FlatList, Text, View } from "react-native";

import Button from "../components/Button";
import EmptyState from "../components/EmptyState";
import Loader from "../components/Loader";
import { listMyUploads, deleteUpload, publishUpload } from "../services/uploadService";
import { UploadItem } from "../types";

export default function MyUploadsScreen() {
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listMyUploads();
      setUploads(data);
    } catch (err) {
      setError("Unable to load uploads.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const onDelete = async (id: string) => {
    await deleteUpload(id);
    await load();
  };

  const onPublish = async (id: string) => {
    await publishUpload(id);
    await load();
  };

  return (
    <View className="flex-1 bg-background px-4 py-6">
      <Text className="text-2xl font-semibold text-slate-900">My uploads</Text>
      <Text className="mt-1 text-sm text-slate-600">Manage your policy uploads and publish requests.</Text>

      <View className="mt-6 flex-1">
        {loading ? (
          <Loader />
        ) : error ? (
          <Text className="mt-4 text-sm text-rose-600">{error}</Text>
        ) : uploads.length === 0 ? (
          <EmptyState message="No uploads yet. Use Upload to submit a policy." />
        ) : (
          <FlatList
            data={uploads}
            keyExtractor={(item) => item._id}
            renderItem={({ item }) => (
              <View className="mb-4 rounded-xl bg-white p-4 shadow-soft">
                <Text className="text-base font-semibold text-slate-900">{item.filename}</Text>
                <Text className="mt-2 text-sm text-slate-600">Status: {item.status}</Text>
                <View className="mt-4 flex-row gap-3">
                  <Button label="Delete" onPress={() => onDelete(item._id)} variant="outline" />
                  <Button label="Publish" onPress={() => onPublish(item._id)} variant="primary" />
                </View>
              </View>
            )}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={{ paddingBottom: 40 }}
          />
        )}
      </View>
    </View>
  );
}
