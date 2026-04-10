import { useEffect, useState } from "react";
import { getPolicies } from "../services/api";

export default function Policies() {
  const [policies, setPolicies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }
  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-slate-900">Policies</h2>
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
