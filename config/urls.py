from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Shop",
        default_version="v1",
        description="Shop anything",
        contact=openapi.Contact(email="jamisays@gmail.com"),
        license=openapi.License(name="IUT_License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.user.urls")),
]

admin.site.site_header = "Shop Admin"
admin.site.site_title = "Shop admin portal"
admin.site.index_title = "Welcome to Shop admin portal"