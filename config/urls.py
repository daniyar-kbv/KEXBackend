from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.site_header = "Kex"
admin.site.index_title = "Панель управления"

internal_schema_view = get_schema_view(
    openapi.Info(
        title="KEX API", default_version="v1", description="Kex",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view = get_schema_view(
    openapi.Info(
        title="FAST CASH API", default_version="v1", description="Trafficwave",
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "docs/internal/",
        internal_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", include("apps.urls")),
]

# if settings.DEBUG_TOOLBAR_ENABLED:
#     import debug_toolbar
#
#     urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
