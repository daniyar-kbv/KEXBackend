from django.conf import settings
from django.urls import include, path

from apps.views import index_view

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("location/", include("apps.location.urls")),
    path("partners/", include("apps.partners.urls")),
    path("common/", include("apps.common.urls")),
    path("orders/", include("apps.orders.urls")),
    path("users/", include("apps.users.urls")),
    path('', index_view),
]
