import React, { useEffect, useState, useMemo } from "react";
import { BarChart, Bar } from "recharts";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [costData, setCostData] = useState([]);
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [selectedDay, setSelectedDay] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  /* ================================
     API Fetch
  ================================= */

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `http://127.0.0.1:8000/api/cost?days=${days}`
      );
      const data = await response.json();
      setCostData(data);
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Backend error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [days]);

  // Auto refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 60000);
    return () => clearInterval(interval);
  }, [days]);

  const exportCSV = () => {
    const headers = ["Date", "Total Cost", "Anomaly"];
    const rows = costData.map(item => [
      item.date,
      item.total_cost,
      item.anomaly,
    ]);
  
    const csvContent =
      [headers, ...rows]
        .map(e => e.join(","))
        .join("\n");
  
    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;",
    });
  
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "cost_report.csv";
    link.click();
  };
  <button onClick={exportCSV}>Export CSV</button>

  /* ================================
     Metrics
  ================================= */

  const totalCost = useMemo(() => {
    return costData.reduce((sum, item) => sum + item.total_cost, 0);
  }, [costData]);

  const costTrend = useMemo(() => {
    if (costData.length < 2) return 0;
    const first = costData[0].total_cost;
    const last = costData[costData.length - 1].total_cost;
    return (((last - first) / first) * 100).toFixed(1);
  }, [costData]);

  const anomalyCount = useMemo(() => {
    return costData.filter((item) => item.anomaly).length;
  }, [costData]);

  const highestAnomaly = useMemo(() => {
    return costData
      .filter((item) => item.anomaly)
      .sort((a, b) => b.total_cost - a.total_cost)[0];
  }, [costData]);

  const formatCurrency = (value) =>
    `₹${value.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;

  /* ================================
     Theme Styles
  ================================= */

  const theme = {
    background: darkMode ? "#0f172a" : "#f8fafc",
    card: darkMode ? "#1e293b" : "#ffffff",
    text: darkMode ? "#f1f5f9" : "#0f172a",
    border: darkMode ? "#334155" : "#e2e8f0",
  };

  /* ================================
     UI
  ================================= */

  return (
    <div
      style={{
        background: theme.background,
        color: theme.text,
        minHeight: "100vh",
        padding: "40px",
        fontFamily: "Inter, sans-serif",
        transition: "0.3s",
      }}
    >
      <h1 style={{ marginBottom: "10px" }}>
        Cloud Cost Intelligence Dashboard
      </h1>

      <div style={{ marginBottom: "20px", display: "flex", gap: "15px" }}>
        <select
          value={days}
          onChange={(e) => setDays(e.target.value)}
          style={{ padding: "6px 10px" }}
        >
          <option value="7">7 Days</option>
          <option value="30">30 Days</option>
          <option value="90">90 Days</option>
        </select>

        <button onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>

        <button onClick={fetchData}>Refresh</button>
      </div>

      {lastUpdated && (
        <p style={{ fontSize: "12px", opacity: 0.7 }}>
          Last updated: {lastUpdated.toLocaleTimeString()}
        </p>
      )}

      {/* Summary Cards */}
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        <Card theme={theme} title="Total Cost">
          {formatCurrency(totalCost)}
        </Card>

        <Card theme={theme} title="Trend">
  <span style={{ color: costTrend > 0 ? "#ef4444" : "#16a34a" }}>
    {costTrend > 0 ? "↑" : "↓"} {costTrend}%
  </span>
</Card>

        <Card
          theme={theme}
          title="Anomalies"
          highlight={anomalyCount > 0}
        >
          {anomalyCount}
        </Card>

        {highestAnomaly && (
          <Card theme={theme} title="Biggest Spike">
            <div>{highestAnomaly.date}</div>
            <div>{formatCurrency(highestAnomaly.total_cost)}</div>
          </Card>
        )}
      </div>

      {/* Legend */}
      <div style={{ marginTop: "25px", fontSize: "14px" }}>
        <strong>Severity Legend:</strong>{" "}
        <span style={{ color: "#facc15" }}>● Low</span>{" "}
        <span style={{ color: "#f97316" }}>● Medium</span>{" "}
        <span style={{ color: "#ef4444" }}>● High</span>
      </div>

      {/* Chart */}
      <div style={{ width: "100%", height: "400px", marginTop: "20px" }}>
      <ResponsiveContainer width="100%" height="100%">
          <LineChart data={costData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip
              formatter={(value) => formatCurrency(value)}
            />
            <Line
              type="monotone"
              dataKey="total_cost"
              stroke="#6366f1"
              strokeWidth={2}
              dot={(props) => {
                const { payload, cx, cy } = props;

                if (!payload.anomaly) {
                  return (
                    <circle cx={cx} cy={cy} r={4} fill="#6366f1" />
                  );
                }

                let color = "#ef4444";
                if (payload.severity === "low") color = "#facc15";
                if (payload.severity === "medium") color = "#f97316";

                return (
                  <circle
                    cx={cx}
                    cy={cy}
                    r={7}
                    fill={color}
                    onClick={() => setSelectedDay(payload)}
                    style={{ cursor: "pointer" }}
                  />
                );
              }}
            />
          </LineChart>
<div style={{ width: "100%", height: "350px", marginTop: "40px" }}>
<h2>Service Cost Distribution</h2>
<ResponsiveContainer width="100%" height="100%">
  <BarChart
    data={
      highestAnomaly?.services?.filter(s => s.cost > 0) || []
    }
  >
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip formatter={(value) => formatCurrency(value)} />
    <Bar dataKey="cost" fill="#6366f1" />
  </BarChart>
</ResponsiveContainer>
</div>
        </ResponsiveContainer>
      </div>

      {/* Service Breakdown Modal */}
      {selectedDay && (
        <Modal
          theme={theme}
          data={selectedDay}
          onClose={() => setSelectedDay(null)}
          formatCurrency={formatCurrency}
        />
      )}

      {loading && (
        <div style={loadingOverlay}>
          <div>Loading...</div>
        </div>
      )}
    </div>
  );
}

/* ================================
   Reusable Card
================================= */

function Card({ title, children, theme, highlight }) {
  return (
    <div
      style={{
        background: theme.card,
        padding: "20px",
        borderRadius: "12px",
        width: "220px",
        border: `1px solid ${theme.border}`,
        boxShadow: highlight
          ? "0 0 15px rgba(239,68,68,0.4)"
          : "0 4px 10px rgba(0,0,0,0.05)",
      }}
    >
      <h3>{title}</h3>
      <div style={{ fontSize: "22px", fontWeight: "bold" }}>
        {children}
      </div>
    </div>
  );
}

/* ================================
   Modal
================================= */

function Modal({ data, onClose, theme, formatCurrency }) {
  console.log("Services data:", data.services);
  return (
    <div style={modalOverlay}>
      <div
        style={{
          background: theme.card,
          padding: "25px",
          borderRadius: "12px",
          width: "400px",
        }}
      >
        <h2>Service Breakdown</h2>
        <p><strong>Date:</strong> {data.date}</p>
        <p><strong>Total:</strong> {formatCurrency(data.total_cost)}</p>

        <div style={{ marginTop: "15px" }}>
        {data.services &&
          Array.isArray(data.services) &&
          data.services
            .filter(service => service.cost > 0)
            .map((service, index) => (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "8px",
                  padding: "6px 0",
                  borderBottom: "1px solid #e2e8f0"
                }}
              >
                <span>{service.name}</span>
                <span>{formatCurrency(service.cost)}</span>
              </div>
            ))}
        </div>

        {data.severity && (
  <div
    style={{
      marginTop: "10px",
      padding: "6px 10px",
      borderRadius: "20px",
      display: "inline-block",
      background:
        data.severity === "high"
          ? "#fee2e2"
          : data.severity === "medium"
          ? "#ffedd5"
          : "#fef9c3",
      color:
        data.severity === "high"
          ? "#dc2626"
          : data.severity === "medium"
          ? "#ea580c"
          : "#ca8a04",
    }}
  >
    {data.severity.toUpperCase()} Severity
  </div>
)}

        {data.explanation && (
          <p style={{ marginTop: "15px", color: "#ef4444" }}>
            {data.explanation}
          </p>
        )}

        <button
          style={{ marginTop: "15px" }}
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
}

/* ================================
   Styles
================================= */

const modalOverlay = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  background: "rgba(0,0,0,0.5)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};

const loadingOverlay = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  background: "rgba(0,0,0,0.3)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  color: "#fff",
  fontSize: "20px",
};

export default App;