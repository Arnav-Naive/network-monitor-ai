# Day 12 — Multi-Switch Support

**Date:** 2026-05-18

## What I Built

Added support for monitoring 3 virtual switches simultaneously,
each with different behavior profiles.

## Switch Profiles

| Switch | CPU Range | Temp Range | Location |
|--------|-----------|------------|----------|
| Core Switch 01 | 60-90% | 55-80°C | Server Room A |
| Access Switch 02 | 20-50% | 30-55°C | Floor 2 |
| Distribution Switch 03 | 40-75% | 40-70°C | Server Room B |

Different ranges = different baselines = ML learns per-switch behavior.

## Key Concepts

**Docker Compose** — runs multiple containers with one command.
`docker compose up -d` starts all 3 switches simultaneously.

**asyncio.gather()** — polls all 3 switches in parallel, not one by one.
```python
tasks = [poll_switch(switch) for switch in switches]
results = await asyncio.gather(*tasks)
```
Faster than sequential polling.

**ForeignKey** — links SwitchMetric to Switch:
```python
switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
```
Each metric row now knows which switch it came from.

**select_related()** — fetches switch data in same DB query:
```python
SwitchMetric.objects.select_related('switch').all()
```
Without this, Django makes a separate DB query per row (slow).

## Dashboard Updates

- Switch filter added (filter by individual switch)
- Switch name column added to table
- All existing filters still work

## Fixes Applied

- SECRET_KEY moved to .env
- Fragile anomaly check fixed in template
- Broken test_snmp.py deleted

## Next Steps

- PostgreSQL to replace SQLite
- Django REST Framework API