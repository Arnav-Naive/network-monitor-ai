# Day 21 — React + Vite + Tailwind Setup

**Date:** 2026-06-03

## What I Built

Django ke saath ek alag React frontend setup kiya.
URL: `localhost:5173` (React) talks to `localhost:8000` (Django API)

## Tech Stack Added
- **Vite** — React project bundler (faster than Create React App)
- **Tailwind CSS v4** — utility-first CSS framework
- **CORS** — Cross-Origin Resource Sharing fix

## Why Separate Frontend?

Django templates = server renders HTML, sends to browser
React = browser renders UI, fetches data from API

React approach is what real companies use:
- Frontend aur backend independently deploy ho sakte hain
- API koi bhi consume kar sakta hai (mobile app, React, Vue)
- Better developer experience

## CORS — Kyun Zaruri Tha?

Browser security rule: ek origin (localhost:5173) doosre 
origin (localhost:8000) se data nahi maang sakta by default.

CORS headers Django ko batate hain: "localhost:5173 ko 
allow karo data fetch karne ke liye."

```python
# settings.py
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
```

`django-cors-headers` middleware yeh headers automatically 
add karta hai har API response mein.

## Vite Proxy — Kyun?

```js
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

React se `/api/switches/` call karo → Vite forward karta 
hai `localhost:8000/api/switches/` pe. CORS issue bypass.

## Key Concept — useEffect + fetch

```jsx
useEffect(() => {
  fetch('/api/switches/')
    .then(r => r.json())
    .then(data => setSwitches(data.results))
}, [])  // [] = sirf ek baar run karo (component mount pe)
```

`useEffect` = side effects ke liye (API calls, timers, etc.)
`[]` dependency array empty = component load hone pe ek baar

## Result
- 3 switch cards dikh rahe hain
- Metrics table with ML anomaly badges working
- Data DRF API se aa raha hai directly