# Day 15 — Deployment Attempt + Production Setup

**Date:** 2026-05-22

## What I Did

### Production Settings Added
- `ALLOWED_HOSTS` updated for Railway domain
- `CSRF_TRUSTED_ORIGINS` added for HTTPS
- `whitenoise` for static file serving
- `gunicorn` as production WSGI server
- `Procfile` created for Railway

### Deployment Attempt — Railway
- Deployed successfully, dashboard loaded
- Issue: Supabase IPv6 incompatibility with Railway network
- Switched to Railway Postgres — worked but empty database
- Decided to revert — too much time spent, not critical for demo

### Key Learning
- Deployment is not just "push and it works"
- Database connections, environment variables, static files
  all need separate configuration for production
- InMemoryChannelLayer doesn't work across processes (why we switched to Redis)
- gunicorn replaces Django dev server in production

## Current Status

Local setup fully working:
- 3 Docker switches (SNMP)
- Redis (WebSocket channel layer)
- Daphne (ASGI server)
- Supabase PostgreSQL
- ML anomaly detection
- Email alerts
- REST API
- Live WebSocket updates

## What I'd Do Differently

Use Render instead of Railway — better Django support on free tier.

## Next Steps

- LinkedIn post (Week 2-3 update)
- Demo video recording
- Show mentor complete system
- Render deployment when time permits