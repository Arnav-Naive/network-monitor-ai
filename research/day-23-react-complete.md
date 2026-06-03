# Day 23 — React Dashboard Complete

**Date:** 2026-06-03

## What I Built

3 nayi components add ki — full professional dashboard ready.

### MetricsLineChart.jsx
Recharts LineChart — CPU, Temp, Memory trends last 20 readings.
3 alag colored lines, responsive, dark theme.

### LiveFeed.jsx
WebSocket se aane wale live rows dikhata hai.
Green pulsing dot — connected indicator.
Max 20 rows rakhta hai memory mein.

### App.jsx (final)
- Alert History + Export CSV buttons header mein
- 2-column grid: Line chart + Bar chart side by side
- LiveFeed WebSocket component
- Full metrics table neeche

## WebSocket in React

```jsx
const ws = new WebSocket(`ws://localhost:8000/ws/metrics/`)

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  setLiveRows(prev => [data, ...prev].slice(0, 20))
}

return () => ws.close()  // cleanup on unmount
```

`useRef` se WebSocket instance store kiya — 
re-renders pe naya connection nahi banta.

Cleanup function (`return () => ws.close()`) — 
component unmount hone pe connection band hota hai.
Memory leak nahi hoti.

## Git Lesson — .vite/ Cache Issue

`frontend/.vite/` accidentally track ho gaya — 
51,149 unnecessary files commit mein.

**Fix:**
```bash
git rm -r --cached frontend/.vite/
```

`--cached` flag = sirf Git tracking se remove karo,
actual files disk pe rehne do.

Phir `.gitignore` mein add karo:
frontend/.vite/

**Rule:** Koi bhi generated/cache folder `.gitignore` mein 
pehle se add karo — `node_modules/`, `.vite/`, `staticfiles/`, 
`__pycache__/`, `*.pkl`

## Final React Component Tree
App.jsx
├── SummaryCards — total, anomalies, health%
├── Switch Cards — 3 cards with location/IP
├── MetricsLineChart — CPU/Temp/Memory trends
├── BandwidthChart — per-switch bandwidth bars
├── LiveFeed — WebSocket live rows
└── Metrics Table — last 100 readings

## Project Status
✅ Django backend (SNMP + ML + WebSocket + API)
✅ React frontend (Recharts + Tailwind + WebSocket)
⬜ Deployment (Render) — next