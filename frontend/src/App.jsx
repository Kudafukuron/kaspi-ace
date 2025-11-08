import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import OwnerDashboard from "./pages/OwnerDashboard";
import OrdersDashboard from "./pages/OrdersDashboard";
import ConsumerPage from "./pages/ConsumerPage";
import SuppliersList from "./pages/SuppliersList";
import LinkRequestsDashboard from "./pages/LinkRequestsDashboard";
import SupplierDashboard from "./pages/SupplierDashboard";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/owner" element={<OwnerDashboard />} />
          <Route path="/orders" element={<OrdersDashboard />} />
          <Route path="/consumer" element={<ConsumerPage />} />
          <Route path="/suppliers" element={<SuppliersList />} />
          <Route path="/dashboard/links" element={<LinkRequestsDashboard />} />
          <Route path="/dashboard/orders" element={<OrdersDashboard />} />
          <Route path="/dashboard/supplier" element={<SupplierDashboard />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
