from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView
from users.admin import custom_admin_site


schema_view = get_schema_view(
    openapi.Info(
        title="GEO auth-service API",
        default_version="v1",
        description="Auth-service for GEOPAY",
        terms_of_service="https://www.geo.com/policies/terms/",
        contact=openapi.Contact(email="contact@geo.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path("api/v1/", include("users.urls")),  # Add trailing slash here
    path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-documentation",
    ),
    path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "",
        RedirectView.as_view(url="api/v1/docs/", permanent=False),
        name="api_documentation",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)