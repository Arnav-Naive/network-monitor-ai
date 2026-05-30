# Git Professional Workflow — Zero to Hero

**Date:** 2026-05-31  
**Project:** Network Monitor AI — Tata Steel Internship

---

## The Old Way (What I Was Doing)

```bash
code → git add . → git commit → git push origin main
```

Problem: Pushing directly to main means one mistake breaks the entire stable codebase. No review, no isolation, no history of what changed and why.

---

## The Professional Way
main branch    = always stable, always working, never broken
feature branch = isolated workspace for one feature or fix

Every piece of work gets its own branch. Main never breaks.

---

## Complete Workflow — Step by Step

### Step 1 — Start new work
```bash
git checkout main              # always start from main
git pull origin main           # get latest code first
git checkout -b feature/name   # create isolated branch
```

### Step 2 — Work and commit
```bash
git add .
git commit -m "day-17: per-switch detail page with charts"
```

**Branch naming conventions:**
feature/switch-detail-page   → new feature
fix/memory-column-dash        → bug fix
docs/readme-update            → documentation
refactor/clean-views          → code improvement

**Commit message format:**
day-XX: short description of what changed
Examples:
day-16: real switch support — community_string per switch
day-17: per-switch detail page with bandwidth bar chart
fix: memory column showing dash in WebSocket rows
feat: demo/live mode indicator in dashboard header

### Step 3 — Push the branch
```bash
git push origin feature/name
```

### Step 4 — Create Pull Request on GitHub
1. Go to your GitHub repo
2. Click "Compare & pull request" (yellow banner)
3. Write a clear title
4. Add bullet point description of changes
5. Click "Create pull request"

### Step 5 — Merge
1. Click "Merge pull request"
2. Click "Confirm merge"
3. Optionally delete the branch after merge (keeps history clean)

### Step 6 — Update local main
```bash
git checkout main
git pull origin main
```

---

## Useful Commands

### Check status
```bash
git status              # what changed
git log --oneline -5    # last 5 commits
git branch              # all local branches
git branch -a           # local + remote branches
git diff                # exact line-by-line changes
```

### Branch management
```bash
git checkout -b feature/name          # create new branch
git checkout existing-branch          # switch to branch
git branch -d feature/name            # delete local branch
git push origin --delete feature/name # delete remote branch
```

### Undo mistakes
```bash
# Wrong commit message
git commit --amend -m "correct message"

# Forgot to add a file to last commit
git add forgotten-file.py
git commit --amend --no-edit

# Undo last commit but keep changes
git reset --soft HEAD~1

# Discard changes in one file
git checkout -- filename.py
```

---

## Merge Conflicts

Happens when two branches change the same line in the same file.
<<<<<<< HEAD
x = 10          ← current branch code
x = 20          ← incoming branch code







feature/name








**How to fix:**
1. Open the file, decide which code to keep
2. Delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Save the file
4. `git add .`
5. `git commit -m "resolve merge conflict"`

---

## Real World Team Workflow
main        → production, protected (no direct push)
develop     → integration branch
feature/*   → individual developer branches
Flow:
feature/* → PR → develop → PR → main (release)

For solo projects (like this one):
main = stable
feature/* = all new work

---

## .gitignore — What to Never Commit

```gitignore
.env              # credentials and secrets — NEVER
*.pkl             # large ML model files
__pycache__/      # Python bytecode cache
.venv/            # virtual environment
staticfiles/      # collectstatic output (generated)
db.sqlite3        # local development database
```

Rule: Never commit sensitive data or generated files.

---

## Quick Reference

| Situation | Command |
|-----------|---------|
| Start new feature | `git checkout -b feature/name` |
| Save work | `git add . && git commit -m "message"` |
| Push branch | `git push origin feature/name` |
| Update main | `git checkout main && git pull` |
| See all branches | `git branch -a` |
| Last 5 commits | `git log --oneline -5` |
| Undo last commit | `git reset --soft HEAD~1` |
| What changed | `git status` |

---

## Key Principle

A pull request is not just a merge tool.  
It is a record of **what changed**, **why it changed**, and **when it changed**.  
Six months later, you (or anyone) can open PR #2 and understand exactly  
what "real switch support" meant and why those specific files changed.  
That is the real value of this workflow.


---------
---------

# Git Professional Workflow — Zero to Hero - Hinglish

**Date:** 2026-05-31

## Pehle Kya Karta Tha (YOLO Style)
```bash
code likho → git add . → git commit → git push
```
Problem: seedha main mein push, koi review nahi, kuch toot gaya toh 
main branch break ho jaati hai.

## Ab Kya Karta Hoon (Professional)

### Mental Model
main branch = hamesha stable, hamesha working
feature branch = experiments, new features, fixes

Main pe directly kabhi push mat karo.

---

## Complete Workflow — Har Feature Ke Liye

### Step 1 — Nayi feature shuru karna
```bash
git checkout main          # pehle main pe aao
git pull origin main       # latest code lo
git checkout -b feature/naam-likho   # naya branch banao
```

**Branch naming convention:**

feature/switch-detail-page   → naya feature
fix/memory-column-dash       → bug fix
docs/readme-update           → documentation
refactor/clean-views         → code cleanup

### Step 2 — Kaam karo, commit karo
```bash
# kuch code likho...
git add .
git commit -m "day-17: per switch detail page added"

# aur kuch karo...
git add .
git commit -m "day-17: bandwidth bar chart added"
```

**Commit message format:**

day-XX: kya kiya short mein
Examples:
day-16: real switch support — community_string per switch
day-17: per-switch detail page with charts
fix: memory column showing dash in WebSocket rows
feat: demo/live mode indicator in dashboard header

Examples:
day-16: real switch support — community_string per switch
day-17: per-switch detail page with charts
fix: memory column showing dash in WebSocket rows
feat: demo/live mode indicator in dashboard header

### Step 3 — Branch push karo
```bash
git push origin feature/naam-likho
```

### Step 4 — Pull Request banao GitHub pe
1. GitHub pe jao → tera repo
2. Yellow banner dikhega "Compare & pull request" → click karo
3. Title likho (commit message jaisa)
4. Description mein kya kiya woh likho (bullet points)
5. "Create pull request" click karo

### Step 5 — Merge karo
1. PR page pe "Merge pull request" click karo
2. "Confirm merge" click karo
3. Branch delete kar sakte ho (optional, clean history ke liye)

### Step 6 — Locally update karo
```bash
git checkout main
git pull origin main
```

---

## Useful Commands

### Status check karna
```bash
git status              # kya kya change hua
git log --oneline -5    # last 5 commits
git branch              # saari branches
git branch -a           # remote branches bhi
```

### Branch management
```bash
git checkout main                    # main pe jao
git checkout -b feature/naam         # nayi branch banao
git checkout feature/existing        # existing branch pe jao
git branch -d feature/naam           # local branch delete karo (merge ke baad)
git push origin --delete feature/naam  # remote branch delete karo
```

### Galti ho gayi? Fix karo
```bash
# Last commit message galat likha
git commit --amend -m "sahi message"

# File add karna bhool gaya last commit mein
git add bhool-gayi-file.py
git commit --amend --no-edit

# Last commit undo karo (changes rakhke)
git reset --soft HEAD~1

# Kisi specific file ko discard karo
git checkout -- filename.py
```

### Merge Conflict kaise hota hai
Tum feature branch pe kaam kar rahe ho
Koi aur (ya tum khud) main mein same file change kar deta hai
Jab merge karte ho → CONFLICT

Conflict dikhta hai aisa:
<<<<<<< HEAD (main branch ka code)
x = 10
x = 20







feature/naam (tera code)








Fix: manually decide karo kaunsa code rakhna hai, 
conflict markers hata do, phir:
```bash
git add .
git commit -m "resolve merge conflict"
```

---

## Real World Team Workflow
main → protected (direct push allowed nahi)
develop → integration branch
feature/* → individual features
Developer workflow:

git checkout develop
git pull origin develop
git checkout -b feature/naam
kaam karo, commits karo
git push origin feature/naam
PR banao: feature/naam → develop
Code review hoti hai
Approved → merge
develop → main (release ke time)

Abhi tere project mein sirf tum ho toh:
main = stable
feature/* = new work
Yahi kaafi hai.

---

## .gitignore — Kya Track Nahi Karna

```gitignore
.env              # credentials kabhi nahi
*.pkl             # ML models (bade files)
__pycache__/      # Python cache
.venv/            # virtual environment
staticfiles/      # collectstatic output
db.sqlite3        # local database
```

Rule: sensitive data aur generated files kabhi commit mat karo.

---

## GitHub Achievements Unlock Karte Jao

- YOLO → direct main push (already mila, ab avoid karo 😂)
- Pull Shark → 2+ PRs merge karo (almost there)
- Starstruck → 16 stars on a repo
- Arctic Code Vault → 2020 archive mein code tha

---

## Quick Reference Card

| Situation | Command |
|-----------|---------|
| Nayi feature shuru | `git checkout -b feature/naam` |
| Kaam save karo | `git add . && git commit -m "message"` |
| Branch push karo | `git push origin feature/naam` |
| Main update karo | `git checkout main && git pull` |
| Branches dekho | `git branch -a` |
| Last 5 commits | `git log --oneline -5` |
| Kya change hua | `git status` |
| Galti undo karo | `git reset --soft HEAD~1` |