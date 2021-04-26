from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("location/", include("apps.location.urls")),
    path("partners/", include("apps.partners.urls")),
    path("orders/", include("apps.orders.urls")),
    path("users/", include("apps.users.urls")),
]
