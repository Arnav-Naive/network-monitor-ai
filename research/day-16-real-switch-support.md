# Day 16 — Real Switch Support + Git Workflow

**Date:** 2026-05-30

## What I Built

### Feature 1: Real Switch Support
Ab system kisi bhi real switch se connect kar sakta hai — 
sirf Docker demo switches tak limited nahi hai.

**Kya change hua:**
- `Switch` model mein 2 nayi fields add ki:
  - `community_string` — har switch ka apna SNMP password
  - `is_demo` — True = Docker fake switch, False = real switch
- `get_snmp_value()` ab dynamic community string leta hai
- `poll_switch()` ab `switch.community_string` DB se use karta hai

**Real switch connect karna ho toh:**
Django admin pe jao → Switch → Add Switch:
- IP address: real switch ka IP
- Port: 161 (standard SNMP)
- Community string: switch ka read-only community string
- is_demo: False (uncheck)

### Feature 2: Demo/Live Mode Indicator
Dashboard header pe indicator dikhta hai:
- 🟡 Demo Mode — sirf Docker switches hain DB mein
- 🟢 Live Mode — koi real switch connected hai

## Git Workflow Seekha

### Pehle (YOLO style):
code likho → git add . → git commit → git push main

### Ab (Professional):

git checkout -b feature/naam     # naya branch
code likho
git add . → git commit           # branch pe commit
git push origin feature/naam     # branch push
GitHub pe PR banao               # Pull Request
Review → Merge                   # main mein merge
git checkout main → git pull     # locally update

**Kyun yeh better hai:**
- Main branch hamesha stable rehta hai
- Har feature isolated hoti hai
- Team mein kaam karte waqt conflicts avoid hote hain
- GitHub pe clean history dikhti hai (PR #1, PR #2...)

## Under The Hood

**community_string kya hota hai:**
Real switches pe ek password hota hai jo SNMP access control 
karta hai. "public" = default read-only password.
Production mein yeh change hota hai security ke liye.

**is_demo flag kyun:**
Same codebase demo aur production dono handle kar sake.
Interview mein Docker se demo karo, real environment mein 
real switch connect karo — code same rehta hai.

## Next Steps
- React frontend
- Bar charts add karna
- SolarWinds-style UI