import { UploadItem } from "../types";
import api from "./api";

export async function uploadPdf(fileUri: string, filename: string): Promise<UploadItem> {
  const form = new FormData();
  form.append("file", {
    uri: fileUri,
    name: filename,
    type: "application/pdf",
  } as any);
  const response = await api.post<UploadItem>("/uploads/pdf", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function listMyUploads(): Promise<UploadItem[]> {
  const response = await api.get<UploadItem[]>("/uploads/my");
  return response.data;
}

export async function deleteUpload(id: string): Promise<void> {
  await api.delete(`/uploads/${id}`);
}

export async function publishUpload(uploadId: string): Promise<{ policy_id: string }> {
  const response = await api.post<{ policy_id: string }>("/uploads/publish", { upload_id: uploadId });
  return response.data;
}
