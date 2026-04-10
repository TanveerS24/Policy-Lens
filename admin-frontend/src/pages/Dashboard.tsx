import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const resp = await getDashboard();
        setData(resp);
      } catch (err) {
        setError("Unable to load dashboard");
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
      <h2 className="text-2xl font-semibold text-slate-900">Dashboard</h2>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <div className="text-sm font-semibold text-slate-500">Total Policies</div>
          <div className="mt-2 text-3xl font-bold text-slate-900">{data.total_policies}</div>
        </div>
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <div className="text-sm font-semibold text-slate-500">Pending Approvals</div>
          <div className="mt-2 text-3xl font-bold text-slate-900">{data.pending_approvals}</div>
        </div>
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <div className="text-sm font-semibold text-slate-500">Total Users</div>
          <div className="mt-2 text-3xl font-bold text-slate-900">{data.total_users}</div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-slate-900">Recent Policies</h3>
        <div className="mt-3 grid gap-4 md:grid-cols-2">
          {data.recent_policies.map((policy: any) => (
            <div key={policy._id} className="rounded-xl bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <h4 className="text-base font-semibold text-slate-900">{policy.title}</h4>
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
                  {policy.approved ? "Published" : "Draft"}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-600">{policy.short_description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
