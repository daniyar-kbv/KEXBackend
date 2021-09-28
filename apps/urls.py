from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.docs.views import ContactListView
from apps.views import index_view

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("location/", include("apps.location.urls")),
    path("partners/", include("apps.partners.urls")),
    path("payments/", include("apps.payments.urls")),
    path("common/", include("apps.common.urls")),
    path("orders/", include("apps.orders.urls")),
    path("users/", include("apps.users.urls")),
    path("promotions/", include("apps.promotions.urls")),
    path("documents/", include(("apps.docs.urls", "documents"), namespace="documents")),
    path("notifications/", include("apps.notifications.urls")),
    path("rates/", include("apps.order_rates.urls")),
    path("contacts/", ContactListView.as_view()),
    path('', index_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
