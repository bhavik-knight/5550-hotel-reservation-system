"""
URL configuration for reservation_system project.

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
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse

# drf-spectacular schema + UI
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    # API endpoints
    path("api/", include("reservations.urls")),
    path("api/", include("hotels.urls")),
    # Schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Root redirect to Swagger UI
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
]


def json_404(request, exception=None):
    return JsonResponse({"error": "Endpoint not found", "status": 404}, status=404)


# Point Django's handler404 to the JSON handler
handler404 = "reservation_system.urls.json_404"
