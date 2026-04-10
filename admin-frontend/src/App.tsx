import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Policies from "./pages/Policies";
import Pending from "./pages/Pending";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/policies" element={<Policies />} />
        <Route path="/pending" element={<Pending />} />
      </Routes>
    </Layout>
  );
}
