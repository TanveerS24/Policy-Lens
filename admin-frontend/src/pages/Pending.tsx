import { useEffect, useState } from "react";
import { approvePolicy, getPending, rejectPolicy } from "../services/api";

export default function Pending() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void load();
  }, []);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getPending();
      setItems(data);
    } catch (err) {
      setError("Unable to load pending requests");
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string) => {
    await approvePolicy(id);
    await load();
  };

  const handleReject = async (id: string) => {
    await rejectPolicy(id);
    await load();
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }
  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-slate-900">Pending Approvals</h2>
      {items.length === 0 ? (
        <div className="rounded-xl bg-white p-6 text-center text-slate-600 shadow-sm">No pending policies.</div>
      ) : (
        <div className="grid gap-4">
          {items.map((item) => (
            <div key={item._id} className="rounded-xl bg-white p-5 shadow-sm">
              <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
                  <p className="mt-1 text-sm text-slate-600">{item.short_description}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => void handleApprove(item._id)}
                    className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-blue-600"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => void handleReject(item._id)}
                    className="rounded-md bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-200"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
