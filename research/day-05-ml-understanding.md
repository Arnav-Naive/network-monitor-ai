# Day 05 — ML Understanding (Isolation Forest)

**Date:** 2026-05-09 to 2026-05-11

## What I Learned

### Anomaly Detection Basics
- System for identifying rare events or outliers
- Deviates significantly from norm in dataset
- Can signal: isolated issues, interesting patterns in data

### Why Isolation Forest?
- **Unsupervised algorithm** - checks on clusters
- Particularly effective in identifying outliers/anomalies
- Dataset outliers are easier to isolate

### How It Works

**Core Concept:**
Anomalies are easier to isolate (separate) than normal points.

**Process:**
1. Build multiple isolation trees (random forest)
2. For each data point, measure path length (how many splits needed to isolate it)
3. Anomalies have **shorter paths** (isolated at depth 2-3)
4. Normal points have **longer paths** (isolated at depth 6-12)

**Scoring:**
- Average path length across 100 trees
- Score close to 1 → highly anomalous
- Score < 0.5 → normal
- Score ≈ 0.5 → cannot decide (need to spend on ≈0.5 on that part)

### Key Parameters

**contamination = 0.1**
- Tells model: "expect roughly 10% of data points to be anomalies"
- Controls sensitivity
- Example: If 1000 data points, model treats ~100 as potential anomalies
- Can adjust: 0.02 for stricter (2%), 0.05 for moderate (5%)

**random_state = 42**
- Ensures reproducibility
- Same results each time model runs

### Advantages
- Linear time complexity → O(n)
- Process will be faster
- Works well with high-dimensional data
- No need for labeled training data

### Limitations
- Cannot detect anomalies if dataset is small
- Difficult to setup "contamination" hyperparameter
- May give false positives in borderline cases

### In My Project

**Training (`train_model.py`):**
```python
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)  # X = 341 samples, 7 features each
```

**Prediction (`monitor_db.py`):**
```python
prediction = model.predict(new_data)
# Returns: -1 = anomaly, +1 = normal
```

---

**What I understand:**
- Anomalies are isolated faster (shorter path in tree)
- Model builds random trees and averages their decisions
- Contamination controls how strict the detection is
- Works without labeled data (unsupervised)

**What I need to learn more:**
- Deep mathematical calculations behind tree building
- Other algorithms like DBSCAN, Local Outlier Factor (not needed for this project)