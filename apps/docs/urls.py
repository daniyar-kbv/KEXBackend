from django.urls import path

from .views import DocumentView, DocumentListView

urlpatterns = [
    path("", DocumentListView.as_view()),
    path("<str:document_slug>/", DocumentView.as_view()),
]
