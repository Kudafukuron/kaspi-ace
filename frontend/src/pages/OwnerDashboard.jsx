// frontend/src/pages/OwnerDashboard.jsx
import { useEffect, useState } from "react";
import productApi from "../api/productApi";
import { useNavigate } from "react-router-dom";

function OwnerDashboard() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", price: "", stock: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Login check
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user || user.role !== "owner") {
    navigate("/");
  }

  // Loading products
  const fetchProducts = async () => {
    try {
      const data = await productApi.getAll();
      setProducts(data);
    } catch (err) {
      console.error("Error while loading products", err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  // Add product
  const handleAdd = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await productApi.create({
        name: form.name,
        description: form.description,
        price: parseFloat(form.price),
        stock: parseInt(form.stock),
      });
      setForm({ name: "", description: "", price: "", stock: "" });
      fetchProducts(); // Updating the list
    } catch (err) {
      console.error("Error while adding the product", err);
    }
    setLoading(false);
  };

  // Delete product
  const handleDelete = async (id) => {
    if (window.confirm("Delete this product?")) {
      await productApi.delete(id);
      fetchProducts();
    }
  };

  return (
    <div style={styles.container}>
      <h2>Owner Dashboard</h2>
      <p>Our products:</p>

      {/* Date of addition */}
      <form onSubmit={handleAdd} style={styles.form}>
        <input
          type="text"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <input
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Amount"
          value={form.stock}
          onChange={(e) => setForm({ ...form, stock: e.target.value })}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add product"}
        </button>
      </form>

      {/* List of products */}
      <ul style={styles.list}>
        {products.map((p) => (
          <li key={p.id} style={styles.item}>
            <div>
              <strong>{p.name}</strong> — {p.price}₸ ({p.stock} pcs.)
            </div>
            <button onClick={() => handleDelete(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  container: { padding: "30px" },
  form: { display: "flex", flexDirection: "column", width: "300px", marginBottom: "20px" },
  list: { listStyle: "none", padding: 0 },
  item: {
    display: "flex",
    justifyContent: "space-between",
    borderBottom: "1px solid #ddd",
    padding: "8px 0",
  },
};

export default OwnerDashboard;
