# Day 14 — WebSocket Debugging Log

**Date:** 2026-05-21  
**Time spent debugging:** ~2 hours

---

## Problem 1: Static Files 404 with Daphne

### What happened
Switched from `manage.py runserver` to `daphne`.  
CSS and JS immediately broke — 404 errors in terminal:
Not Found: /static/monitor/css/dashboard.css
Not Found: /static/monitor/js/dashboard.js

### Why it happened
`manage.py runserver` serves static files automatically in development.  
Daphne does not — it's a production ASGI server, not a dev tool.  
Static files need to be explicitly collected and served.

### How I fixed it
Added to `settings.py`:
```python
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'monitor', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

Added to `urls.py`:
```python
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Ran:
```bash
python manage.py collectstatic --noinput
```

This copies all static files into `staticfiles/` folder so Daphne can find them.

---

## Problem 2: WebSocket Connected but No Messages

### What happened
WebSocket status showed 101 (connected) in browser Network tab.  
Daphne logs showed `WSCONNECT /ws/metrics/` — connection confirmed.  
Monitor script showed `📡 WebSocket push sent` every poll.  
But browser received nothing. Dashboard not updating.

### Why it happened
`InMemoryChannelLayer` stores messages in RAM **within a single process**.  
`monitor_snmp.py` and `daphne` are **two separate processes**.  
They each have their own memory — they cannot see each other's channel layer.

monitor_snmp.py  →  its own InMemory instance  (process A)
daphne           →  its own InMemory instance  (process B)
group_send() writes to process A's memory.
Consumer reads from process B's memory.
They never overlap. Messages disappear into the void.

This is a known limitation of `InMemoryChannelLayer` — it's documented as  
"for testing only, single process only." The code looked correct. The bug  
was architectural, not syntactic.

### How I found it
Added `console.log` to `ws.onmessage` — console stayed empty even though  
monitor was pushing. Ruled out JS bug. The send was succeeding but receive  
was never triggering — pointed to the channel layer being the disconnect.

### How I fixed it
Replaced `InMemoryChannelLayer` with Redis:

```bash
docker run -d -p 6379:6379 --name redis redis:alpine
pip install channels-redis redis
```

Updated `settings.py`:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    }
}
```

Redis is an external message broker — both processes connect to it.  
Now `monitor_snmp.py` writes to Redis, Daphne reads from Redis.  
They share state without being in the same process.

monitor_snmp.py  →  Redis  ←  daphne  →  browser

After this change: rows appeared in dashboard automatically, no reload needed.

---

## Key Lesson

**"It worked in one process" is not the same as "it works across processes."**

InMemoryChannelLayer is not a bug — it's a tool for the wrong job.  
The Day 14 code was architecturally correct for production  
but used a dev-only component (`InMemoryChannelLayer`) that made it  
silently fail in a multi-process setup.

Real-world systems always use Redis (or similar) for inter-process messaging.  
This is now how the project is configured.

---

## Final Working Setup (4 terminals)

Terminal 1: docker start switch-core-01 switch-access-02 switch-dist-03
docker start redis
Terminal 2: python src/monitor_snmp.py
Terminal 3: daphne -p 8000 dashboard.asgi:application
Browser:    http://localhost:8000

---

## What I Learned From This

- Daphne ≠ Django dev server. Different rules for static files.
- `collectstatic` is not optional when using Daphne.
- InMemoryChannelLayer only works inside one Python process.
- Redis = shared message bus that multiple processes can read/write.
- Silent failures (no error, just nothing happening) are harder to debug  
  than crashes. Adding `try/except` with prints was the key debugging move.
- WebSocket architecture: sender → channel layer → consumer → browser.  
  If any link is broken, the whole chain silently fails.