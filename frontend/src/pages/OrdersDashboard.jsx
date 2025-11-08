import React, { useEffect, useState } from "react";
import { orderApi } from "../api/orderApi";

const OrdersDashboard = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const data = await orderApi.getAll();
        setOrders(data);
      } catch (err) {
        setError("Failed to load orders.");
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!orders.length) return <p>No orders yet.</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Orders</h2>
      {orders.map((order) => (
        <div key={order.id} style={{ borderBottom: "1px solid #ccc", marginBottom: "10px" }}>
          <p><strong>Product:</strong> {order.product}</p>
          <p><strong>Quantity:</strong> {order.quantity}</p>
          <p><strong>Status:</strong> {order.status}</p>
        </div>
      ))}
    </div>
  );
};

export default OrdersDashboard;
