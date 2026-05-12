# System Architecture

## High-Level Overview

```mermaid
flowchart TD
    A[Network Switch] -->|SNMP Polling<br/>Every 5 seconds| B[Monitor Script<br/>monitor_db.py]
    B -->|Collect Metrics| C[Data Processing]
    C -->|Save| D[(SQLite Database<br/>SwitchMetric Table)]
    D -->|Read Data| E[ML Training<br/>train_model.py]
    E -->|Generate| F[Trained Model<br/>anomaly_model.pkl]
    F -->|Load Model| B
    B -->|Detect Anomalies| G[Alert System]
    D -->|Query Data| H[Django Web Server]
    H -->|Render| I[Dashboard<br/>localhost:8000]
    I -->|Auto-refresh<br/>Every 10 sec| H
    
    style A fill:#e1f5ff
    style D fill:#fff4e1
    style F fill:#ffe1e1
    style I fill:#e1ffe1
    style D fill:#fff4e1,color:#000
    style F fill:#ffe1e1,color:#000
    style I fill:#e1ffe1,color:#000
```

## Data Flow

**Phase 1: Data Collection**
1. Monitor script polls switch metrics (simulated currently)
2. Collects: CPU, Memory, Temperature, Bandwidth, Interface status, CRC errors, TX/RX rates
3. Saves to database with timestamp

**Phase 2: ML Training**
1. Training script reads historical data (minimum 50 samples)
2. Trains Isolation Forest model
3. Saves trained model to pickle file

**Phase 3: Real-time Detection**
1. Monitor loads trained model
2. For each new reading: ML predicts normal (1) or anomaly (-1)
3. Threshold checks run in parallel (backup)
4. Anomalies saved to database

**Phase 4: Visualization**
1. Django reads latest data from database
2. Renders dashboard with metrics table
3. Highlights ML-detected anomalies in yellow
4. Page auto-refreshes every 10 seconds