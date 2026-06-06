# Day 25 — Project Complete + Final Summary

**Date:** 2026-06-05

## Live URLs
https://network-monitor-ai.onrender.com — Django dashboard
https://network-monitor-ai.vercel.app — React dashboard

## What Got Built — Full 6 Week Summary

| Week | What |
|------|------|
| 1 | Django setup, SQLite, basic dashboard |
| 2 | Docker SNMP, ML model, email alerts |
| 3 | PostgreSQL, DRF API, WebSocket |
| 4 | Redis, multi-switch, Git workflow |
| 5 | Real switch support, detail pages, alert history |
| 6 | React frontend, Recharts, Render deployment |

## Final Tech Stack

**Backend:** Django, DRF, Channels, Daphne, Redis, Gunicorn
**Frontend (local):** React, Vite, Tailwind v4, Recharts
**Database:** PostgreSQL (Supabase)
**ML:** Isolation Forest (scikit-learn, 537 samples)
**Protocol:** SNMP via pysnmp v7 async
**Infrastructure:** Docker, Render, GitHub

## What Works on Deployed Version
- Full Django dashboard with filters
- ML anomaly detection badges
- Per-switch detail pages
- Alert history page
- REST API (3 endpoints)
- CSV export
- Auto-refresh fallback (WebSocket not supported on Render free tier)

## What Works Only Locally
- WebSocket live updates (Render free tier doesn't support it)
- Docker SNMP switches (local data collection)

## Known Limitations
- Render free tier — 50 sec spin up delay
- WebSocket falls back to 10 sec refresh on deployed version
- anomaly_model.pkl not in git — must run train_model.py on fresh setup

## Interview One-Liner
"AI-powered network switch monitoring system built during 
Tata Steel internship — real SNMP protocol, Isolation Forest 
ML anomaly detection, WebSocket live dashboard, REST API, 
deployed on Render with PostgreSQL on Supabase."