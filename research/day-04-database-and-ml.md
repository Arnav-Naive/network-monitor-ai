# Day 04 — Database Migration + ML Integration

**Date:** 2026-05-08  
**Status:** Major milestone - AI working

## Part 1: Database Migration

Migrated from CSV file storage to SQLite database.

**Why database?**
- Better performance with large datasets
- Required for ML training (can't efficiently train on CSV)
- More professional architecture

**What I did:**
- Created Django model `SwitchMetric` with all monitoring fields
- Ran migrations to create database table
- Updated monitor script to save to database instead of CSV
- Updated dashboard view to read from database

**Technical learning:**
- Django ORM (Object-Relational Mapping)
- `models.py` defines database structure as Python classes
- `makemigrations` + `migrate` creates actual tables
- `objects.create()` saves data to database

## Part 2: ML Anomaly Detection

Added machine learning layer using Isolation Forest algorithm.

**How it works:**
1. Collect baseline data (50+ samples minimum)
2. Train model to learn "normal" patterns
3. Model predicts: 1 = normal, -1 = anomaly
4. Alerts triggered when patterns deviate

**Implementation:**
- `train_model.py` — trains model on existing data, saves to pickle file
- `monitor_db.py` — loads model, uses it for real-time detection
- Features used: CPU, memory, temperature, bandwidth, CRC errors, TX/RX rates

**Key insight:**
Threshold alerts say: "CPU > 80% is bad"
ML alerts say: "This pattern is unusual for this switch"

Much smarter — reduces false alarms, catches subtle issues.

## Technical Stack Update

**New dependencies:**
- scikit-learn (ML library)
- numpy (numerical operations)
- pickle (model persistence)

**Current architecture:**
Monitor Script → Collects data

↓

Database (SQLite) → Stores metrics

↓

ML Model → Detects anomalies

↓

Dashboard → Displays + highlights

## Next Steps

**Day 5:**
- Add data visualization (charts showing metrics over time)
- Improve dashboard UI
- Add statistics summary cards

**Week 2:**
- Research pysnmp for real switch connection
- Test with public SNMP servers
- Prepare for actual switch access

---

*AI-powered monitoring now functional. Core system complete.*
