from django.contrib import admin
from .models import SwitchMetric, Switch, AlertHistory

# Register your models here.

admin.site.register(SwitchMetric)
admin.site.register(Switch)
admin.site.register(AlertHistory)