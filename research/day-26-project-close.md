# Day 26 — Final Fixes + Project Close

**Date:** 2026-06-06

## Fixes Applied

**Fix 1: CSRF_TRUSTED_ORIGINS**
Railway delete kar diya tha. Setting purani URL point kar rahi thi.
Updated to: `https://network-monitor-ai.onrender.com`

**Fix 2: Chart.js CDN — switch_detail.html**
dashboard.html pe CDN fix kiya tha Day 24 mein but
switch_detail.html pe miss ho gaya tha.
jsdelivr → cloudflare (more reliable on deployed version)

**Fix 3: AlertHistory in admin.py**
Model bana tha Day 18 mein but admin mein register karna
bhool gaya. Ab `/admin/` pe visible hai.

**Fix 4: day-25 docs update**
React deployed on Vercel — docs outdated the.

## Final Project URLs

| Version | URL |
|---------|-----|
| Django Dashboard | https://network-monitor-ai.onrender.com |
| React Dashboard | https://network-monitor-ai.vercel.app |
| GitHub | https://github.com/Arnav-Naive/network-monitor-ai |

## What I Built — 6 Week Summary

25 working days. Solo project. Zero prior experience with
most of this stack when I started.

Stack learned and shipped:
Python, Django, DRF, Docker, SNMP, scikit-learn,
Redis, WebSocket, Channels, Daphne, PostgreSQL,
Supabase, React, Vite, Tailwind, Recharts,
Render, Vercel, Git branching, PRs

## Honest Assessment

Strong: Architecture, Git workflow, documentation,
feature completeness, deployment.

Weak: async/await internals not fully understood,
React filters missing vs Django dashboard,
WebSocket doesn't work on Render free tier.

## Interview One-Liner
"AI-powered network switch monitoring system —
SNMP polling, Isolation Forest ML, WebSocket live
dashboard, REST API, React frontend. Deployed on
Render + Vercel with PostgreSQL on Supabase."