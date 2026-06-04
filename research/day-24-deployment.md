# Day 24 — Render Deployment

**Date:** 2026-06-04

## Live URL
https://network-monitor-ai.onrender.com

## What I Did
- Render pe Django dashboard deploy kiya
- Supabase PostgreSQL Session Pooler URL use kiya (IPv4 fix)
- Environment variables set kiye
- Migrations automatically run hui deploy pe

## Key Settings for Deployment
- `ALLOWED_HOSTS = ['*']`
- `ssl_require` removed from DATABASES
- `gunicorn` as production server
- `whitenoise` for static files

## Free Tier Limitation
- 50 second spin-up delay after inactivity
- Charts empty — Chart.js CDN issue (minor fix needed)

## Architecture Now
Local: Docker switches → monitor_snmp.py → Supabase
Deployed: https://network-monitor-ai.onrender.com → Supabase (same DB)