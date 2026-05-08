from django.shortcuts import render
from .models import SwitchMetric

def dashboard_view(request):
    # Get last 50 entries from database
    logs = SwitchMetric.objects.all()[:50]
    
    return render(request, 'monitor/dashboard.html', {'logs': logs})