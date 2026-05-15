# Day 07 — Finalized ML Understanding

**Date:** 2026-05-11

## Isolation Forest — My Understanding

**Core idea:** Anomalies are easier to isolate than normal points.

Normal data points are clustered together — hard to separate.
Anomalies are alone — easy to separate with fewer cuts.

**How the algorithm works:**
1. Build random decision trees
2. For each data point, count how many cuts needed to isolate it
3. Anomalies need fewer cuts → flagged as -1
4. Normal points need many cuts → flagged as +1

**In my project:**
```python
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)         # learns normal patterns from 341 samples
model.predict(new)   # returns -1 (anomaly) or 1 (normal)
```

**contamination=0.1** → expects 10% of data to be anomalies  
**random_state=42** → same results every run (reproducibility)

## What I Still Don't Know

- Deep math behind tree building
- DBSCAN and LOF algorithms (not needed for this project)

## Key Insight

Model doesn't need labeled data (unsupervised).
It learns what normal looks like, then flags anything different.
This is better than thresholds because each switch has its own baseline.