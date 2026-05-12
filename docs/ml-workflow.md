# ML Anomaly Detection Workflow

## Training Phase (One-time / Periodic)

```mermaid
flowchart LR
    A[Database<br/>341 samples] -->|Extract Features| B[Feature Matrix<br/>7 columns x 341 rows]
    B -->|Feed to Algorithm| C[Isolation Forest<br/>contamination=0.1]
    C -->|Learn Patterns| D[Trained Model]
    D -->|Save to Disk| E[anomaly_model.pkl]
    
    style A fill:#e1f5ff,color:#000
    style C fill:#ffe1e1,color:#000
    style E fill:#fff4e1,color:#000
```

**Features Used:**
- CPU Usage (%)
- Memory Usage (%)
- Temperature (°C)
- Bandwidth (Mbps)
- CRC Errors (count)
- TX Rate (Mbps)
- RX Rate (Mbps)

---

## Prediction Phase (Real-time)

```mermaid
flowchart TD
    A[New Switch Reading] -->|Extract Same 7 Features| B[Feature Vector]
    B -->|Load Model| C[anomaly_model.pkl]
    C -->|Predict| D{Prediction Result}
    D -->|1 = Normal| E[No Alert<br/>Continue Monitoring]
    D -->|-1 = Anomaly| F[Trigger Alert<br/>ML DETECTED ANOMALY]
    F -->|Save to DB| G[Dashboard Shows Alert]
    E -->|Save to DB| G
    
    style A fill:#e1f5ff,color:#000
    style D fill:#ffe1e1,color:#000
    style F fill:#ffcccc,color:#000
    style G fill:#e1ffe1,color:#000
```

## How Isolation Forest Works (Simplified)

**Concept:** Anomalies are easier to isolate (separate) than normal points.

**Example:**
- Normal data: clustered together (like a crowd)
- Anomaly: standing alone (easy to isolate with 1-2 cuts)

**Algorithm:**
1. Build random decision trees
2. Count how many cuts needed to isolate each point
3. Anomalies need fewer cuts (low score) → flag as -1
4. Normal points need many cuts (high score) → return 1

**Why contamination=0.1?**
- Tells algorithm: "expect 10% of data to be anomalies"
- Adjusts sensitivity threshold