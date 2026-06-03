# Day 22 — React Dashboard — Components

**Date:** 2026-06-03

## What I Built

3 React components banaye jo DRF API se data lete hain:

### SummaryCards.jsx
Total readings, ML anomalies, system health % — 
same jo Django dashboard pe tha but React mein.

### BandwidthChart.jsx
Recharts BarChart — teeno switches ka bandwidth, TX, RX 
side by side. Same data, better looking.

### App.jsx (updated)
- useEffect se 2 API calls: /api/switches/ + /api/metrics/
- Data teeno components mein props ke through bheja
- CPU > 85% aur Temp > 78°C red highlight

## New Concepts

### Props
```jsx
<SummaryCards metrics={metrics} switches={switches} />
```
Parent se child component mein data bhejne ka tarika.
Like function arguments — component ko data do, 
component display kare.

### Conditional Styling (Tailwind)
```jsx
className={`p-3 ${m.cpu_usage > 85 ? 'text-red-400 font-bold' : ''}`}
```
Template literal mein condition — agar CPU high hai 
toh red color, warna normal.

### Recharts
```jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, 
         ResponsiveContainer } from 'recharts'
```
Chart library for React. Data array do, chart ban jaata hai.
`ResponsiveContainer` = chart automatically resize hota hai 
screen size ke saath.

## Component Tree
App.jsx
├── SummaryCards (total, anomalies, health)
├── Switch Cards (3 cards, inline)
├── BandwidthChart (Recharts BarChart)
└── Metrics Table (inline)

## Next Steps
- Line chart (CPU/temp/memory trends)
- WebSocket live updates React mein
- Deployment