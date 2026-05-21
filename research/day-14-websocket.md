# Day 14 — WebSocket Live Updates

**Date:** 2026-05-20

## What I Built

Replaced 10-second page refresh with real-time WebSocket connection.

## What is WebSocket (Simple)

Normal refresh: Browser asks server every 10 seconds — "any new data?"
WebSocket: Server pushes to browser instantly when new data arrives.

Like WhatsApp — you don't refresh manually, messages arrive automatically.

## How It Works in the Project

monitor_snmp.py polls switch
→ saves to database
→ pushes to WebSocket channel group 'metrics'
→ all connected browsers receive data instantly
→ JavaScript adds new row to table without reload

## New Files Created

- `monitor/consumers.py` — WebSocket handler (connect/disconnect/receive)
- `monitor/routing.py` — WebSocket URL routing (`ws/metrics/`)

## Key Concepts

**Django Channels** — adds WebSocket support to Django (normally HTTP only)

**Daphne** — ASGI server that handles both HTTP and WebSocket.
Replaces `manage.py runserver` which only handles HTTP.

**ASGI vs WSGI:**
- WSGI = old standard, handles one request at a time (synchronous)
- ASGI = new standard, handles WebSocket + async (what Channels needs)

**Channel Layer** — message bus between monitor script and browser.
```python
# Monitor script sends:
channel_layer.group_send('metrics', {'type': 'metrics_update', 'data': {...}})

# Consumer receives and forwards to browser:
async def metrics_update(self, event):
    await self.send(text_data=json.dumps(event['data']))
```

**InMemoryChannelLayer** — stores messages in RAM.
Fine for single server. For production with multiple servers, use Redis.

## Static Files Fix

Daphne doesn't serve static files automatically in dev mode.
Fixed by:
- Running `python manage.py collectstatic`
- Adding `+ static(...)` to `urls.py`
- Setting `STATICFILES_DIRS` and `STATIC_ROOT` in settings

## Verified Working

- WebSocket status 101 in Network tab = handshake successful
- "Pending" status = connection open, waiting for messages
- `WSCONNECT /ws/metrics/` in Daphne logs = browser connected

## What I Didn't Understand

- async/await internals in consumers.py
- Channel layer internals
- Difference between group_send and send

## Next Steps

- Railway deployment (public URL)
- Docker Compose for one-command startup