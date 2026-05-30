"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from monitor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('export/', views.export_csv, name='export_csv'),
    path('switch/<int:switch_id>/', views.switch_detail_view, name='switch_detail'),  # added switch detail view
    path('api/metrics/', views.api_metrics, name='api_metrics'),
    path('api/switches/', views.api_switches, name='api_switches'),
    path('api/anomalies/', views.api_anomalies, name='api_anomalies'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)