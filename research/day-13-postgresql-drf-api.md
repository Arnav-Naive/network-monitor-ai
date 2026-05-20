# Day 13 — PostgreSQL + REST API

**Date:** 2026-05-19

## Part 1: PostgreSQL via Supabase

Replaced SQLite (file-based) with PostgreSQL (production database).

**Why PostgreSQL over SQLite?**
- SQLite = single file, one user, no concurrent writes
- PostgreSQL = real server, handles multiple connections, production-ready
- Every real company uses PostgreSQL or similar

**Supabase** = hosted PostgreSQL with nice UI dashboard.
Free tier, good for resume, Table Editor shows data visually.

**Key library:** `dj-database-url`
Parses connection string from .env into Django DATABASES dict:
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
```
One line replaces the entire DATABASES config.

### Part 2: Django REST Framework API

Added 3 REST API endpoints.

**Installed:** `djangorestframework`, added `rest_framework` to INSTALLED_APPS

**Endpoints:**
| URL | Returns |
|-----|---------|
| `/api/metrics/` | Last 100 metrics as JSON |
| `/api/switches/` | All switches as JSON |
| `/api/anomalies/` | Only anomaly records |

**What is a Serializer?**
Converts Django model → JSON automatically.
Without it you'd manually build dicts for every field.

**What is an API endpoint?**
A URL that returns data (JSON) instead of HTML.
Other apps/services can consume this data programmatically.

**Why REST API matters:**
- Frontend can be separate (React, mobile app)
- Other systems can integrate with your monitoring data
- Industry standard for backend development



**New concept — Serializer:**
Converts Django model objects → JSON automatically.
Without it, you'd manually build a dict for every field.

```python
class SwitchMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchMetric
        fields = ['id', 'cpu_usage', 'temperature', ...]
```

**New concept — @api_view decorator:**
Marks a function as a REST API view.
DRF handles content negotiation, error responses, and the browsable API.

**Browsable API:**
DRF auto-generates a web UI at each endpoint showing the JSON response.
The top heading "Django REST Framework" links to official docs at
`https://www.django-rest-framework.org/` — that's expected behavior, not an error.

## Files Changed

- `dashboard/settings.py` — DATABASES updated, `rest_framework` added
- `monitor/serializers.py` — new file
- `monitor/views.py` — 3 new API views added
- `dashboard/urls.py` — 3 new URL routes
- `requirements.txt` — psycopg2-binary, dj-database-url, djangorestframework
- `.env` — DATABASE_URL added

## Current Stack

SQLite → **Supabase PostgreSQL** ✅
Django views → **+ REST API (3 endpoints)** ✅


## Interview Answer

"I replaced SQLite with PostgreSQL hosted on Supabase for
production readiness. Added a REST API with Django REST Framework
exposing three endpoints — switches, metrics, and anomalies.
This means the monitoring data can be consumed by any frontend
or external system, not just the Django dashboard."

## Next Steps

- WebSocket live updates (replace 10-sec refresh)
- Docker Compose for one-command startup
- Deployment
