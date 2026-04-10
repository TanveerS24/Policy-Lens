import { useState } from "react";
import { Text, View } from "react-native";
import * as DocumentPicker from "expo-document-picker";

import Button from "../components/Button";
import Loader from "../components/Loader";
import { uploadPdf } from "../services/uploadService";

export default function UploadScreen() {
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileUri, setFileUri] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const pickFile = async () => {
    const result = await DocumentPicker.getDocumentAsync({ type: "application/pdf" });
    if (!result.canceled && result.assets.length > 0) {
      const asset = result.assets[0];
      setFileName(asset.name);
      setFileUri(asset.uri);
      setStatus(null);
    }
  };

  const upload = async () => {
    if (!fileUri || !fileName) return;
    setLoading(true);
    setStatus("Uploading...");
    try {
      await uploadPdf(fileUri, fileName);
      setStatus("Submitted for approval");
    } catch (err) {
      setStatus("Upload failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-background px-6 py-8">
      <Text className="text-2xl font-semibold text-slate-900">Upload a policy</Text>
      <Text className="mt-1 text-sm text-slate-600">Upload a PDF to generate a summary and eligibility draft.</Text>

      <View className="mt-8 space-y-4">
        <Button label="Choose PDF" onPress={pickFile} variant="secondary" />
        {fileName ? (
          <View className="rounded-xl bg-white p-4 shadow-soft">
            <Text className="text-base font-medium text-slate-900">Selected file</Text>
            <Text className="mt-1 text-sm text-slate-600">{fileName}</Text>
          </View>
        ) : null}

        {status ? <Text className="text-sm text-slate-600">{status}</Text> : null}

        <Button label="Upload" onPress={upload} variant="primary" disabled={!fileUri} />

        {loading ? <Loader message={status ?? "Uploading..."} /> : null}
      </View>
    </View>
  );
}
