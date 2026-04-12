import { useEffect, useState } from "react";
import { getPolicies, uploadPdf } from "../services/api";

export default function Policies() {
  const [policies, setPolicies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [showUpload, setShowUpload] = useState(false);

  useEffect(() => {
    void (async () => {
      try {
        const data = await getPolicies();
        setPolicies(data);
      } catch (err) {
        setError("Failed to load policies");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setUploadError("Only PDF files are supported");
      return;
    }

    setUploading(true);
    setUploadError(null);

    try {
      await uploadPdf(file);
      setShowUpload(false);
      // Reload policies
      const data = await getPolicies();
      setPolicies(data);
    } catch (err: any) {
      setUploadError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }
  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-900">Policies</h2>
        <button
          onClick={() => setShowUpload(!showUpload)}
          className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
        >
          {showUpload ? "Cancel" : "Upload Policy"}
        </button>
      </div>

      {showUpload && (
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Upload PDF Policy</h3>
          {uploadError && <p className="mt-2 text-red-600">{uploadError}</p>}
          <div className="mt-4">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              disabled={uploading}
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
            <p className="mt-2 text-sm text-slate-500">Only PDF files are supported</p>
          </div>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {policies.map((policy) => (
          <div key={policy._id} className="rounded-xl bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">{policy.title}</h3>
                <p className="mt-1 text-sm text-slate-600">{policy.short_description}</p>
              </div>
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${
                  policy.approved ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"
                }`}
              >
                {policy.approved ? "Published" : "Draft"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
