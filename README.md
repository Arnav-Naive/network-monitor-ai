# Network Monitor AI

AI-powered network switch monitoring system using SNMP and machine learning.

## Features
- Real-time SNMP data collection
- ML-based anomaly detection (Isolation Forest)
- Auto-refreshing web dashboard
- Threshold + pattern-based alerts

## Tech Stack
- Python, Django, scikit-learn, SQLite
- Future: pysnmp for real switch integration

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start monitor (collect data)
python src/monitor_db.py

# Train ML model (after 50+ samples)
python src/train_model.py

# Start web server
python manage.py runserver
```

Visit: http://localhost:8000

## Project Status
- ✅ Database integration
- ✅ ML anomaly detection
- 🔄 Real SNMP integration (planned Week 2)
- 🔄 Advanced visualizations (planned Week 3)