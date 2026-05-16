# Day 09 — Docker + SNMP Integration

**Date:** 2026-05-14

## What I Built

Replaced simulated Python random data with real SNMP polling
using a Docker container running Net-SNMP agent.

## What is Docker (Simple)

Docker creates isolated "containers" — lightweight virtual machines.
Instead of installing software on Windows directly, you run it
inside a container.

Like this:
- Before: Python generates fake data internally
- After: Python sends real SNMP request → Docker container responds

The communication is real network protocol (UDP port 161).
Values inside container are simulated, but the protocol is real.
Same architecture as polling a real Cisco switch.

## What is SNMP (Reminder)

Simple Network Management Protocol.
Python asks: "What is your CPU usage?" (GET request)
Switch/container answers: "67%"
Uses UDP port 161.
Password called "community string" — we used "public".

## Files Created

docker-snmp/
├── Dockerfile          — instructions to build container
├── snmpd.conf          — SNMP agent configuration
└── scripts/
├── cpu.sh          — generates random CPU value
├── memory.sh       — generates random memory value
├── temperature.sh  — generates random temperature value
└── bandwidth.sh    — generates random bandwidth value

## How Docker Container Works
Dockerfile → docker build → Image (blueprint)
Image → docker run → Container (running instance)

Same relationship as:
Python file → run → Running process

## Obstacles Faced (Important)

### Obstacle 1: snmpsim not working on Windows
**Problem:** Original plan was snmpsim package.
Commands tried:
- `snmpsimd.py` — not recognized
- `python -m snmpsim.commands.snmpsimd` — module not found
- `snmpsim-command-responder` — wrong parameter syntax

**Solution:** Switched to Docker Net-SNMP entirely.
More professional, better for resume anyway.

### Obstacle 2: pysnmp import error
**Problem:** Had `pysnmp-lextudio` (deprecated old package).
ImportError: cannot import name 'getCmd' from 'pysnmp.hlapi'

**Solution:**
```bash
pip uninstall pysnmp pysnmp-lextudio -y
pip install pysnmp==7.1.10
```

### Obstacle 3: pysnmp v7 changed API completely
**Problem:** v7 uses async/await. Old code used `getCmd`, new uses `get_cmd`.

**Solution:** Rewrote monitor_snmp.py using async/await pattern:
```python
# Old (v6):
from pysnmp.hlapi import getCmd, SnmpEngine...

# New (v7):
from pysnmp.hlapi.v3arch.asyncio import *
errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(...)
```

### Obstacle 4: Django can't be called from async context
**Problem:**
SynchronousOnlyOperation: You cannot call this from an async context

Django ORM is synchronous. Our monitor loop became async (because of pysnmp v7).

**Solution:** `sync_to_async` wrapper from asgiref:
```python
from asgiref.sync import sync_to_async

@sync_to_async
def create_metric():
    return SwitchMetric.objects.create(...)

metric = await create_metric()
```

### Obstacle 5: Docker container returning static values
**Problem:** Shell scripts used `$RANDOM` which doesn't work in `/bin/sh`.
Every poll returned: CPU 40%, Temp 35°C, Memory 50%.

**Diagnosis:** Connected to running container:
```bash
docker exec -it virtual-switch /bin/bash
/usr/local/bin/cpu.sh  # always returned 40
```

**Solution:** Replaced `$RANDOM` with `/dev/urandom`:
```bash
# Old (broken):
echo $((40 + RANDOM % 51))

# New (working):
echo $((40 + $(od -An -N2 -tu2 /dev/urandom) % 51))
```

`/dev/urandom` is a Linux file that outputs random bytes.
Works in all shells, not just bash.

## Docker Commands Reference

| Command | What it does |
|---------|-------------|
| `docker build -t snmp-switch .` | Build image from Dockerfile |
| `docker run -d -p 161:161/udp --name virtual-switch snmp-switch` | Start container |
| `docker ps` | List running containers |
| `docker stop virtual-switch` | Stop container |
| `docker start virtual-switch` | Start stopped container |
| `docker rm virtual-switch` | Delete container |
| `docker logs virtual-switch` | See container output |
| `docker exec -it virtual-switch /bin/bash` | Enter container shell |

## To Run This Project

```bash
# Start Docker Desktop first
docker start virtual-switch
python src/monitor_snmp.py  # Terminal 1
python manage.py runserver  # Terminal 2
```

## What I Understood vs Didn't

**Understood:**
- Why Docker (isolation, portability, resume value)
- SNMP protocol flow (GET request → response)
- Why /dev/urandom works but $RANDOM doesn't

**Didn't fully understand (copy-paste):**
- async/await internals
- sync_to_async mechanics
- pysnmp v7 API details

## Key Interview Answer — Challenges Faced

"We tried snmpsim initially but it had Windows compatibility issues.
Switched to Docker Net-SNMP which was actually a better choice —
it's more professional and taught me containerization.
The biggest technical challenge was pysnmp v7 breaking changes —
the entire API switched to async/await, which required wrapping
Django ORM calls in sync_to_async to avoid SynchronousOnlyOperation errors.
Also learned that $RANDOM doesn't work in /bin/sh — had to use
/dev/urandom for generating dynamic values in the container."