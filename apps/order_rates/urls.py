from django.urls import path

from .views import RateStarListView, CreateRateOrderView

urlpatterns = [
    path('', CreateRateOrderView.as_view()),
    path('stars/', RateStarListView.as_view()),
]