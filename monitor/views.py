import csv
import os
from django.shortcuts import render

def dashboard_view(request):
    # Read CSV file
    logs = []
    csv_path = 'data/logs.csv'
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
    
    # Send data to HTML template
    return render(request, 'monitor/dashboard.html', {'logs': logs})