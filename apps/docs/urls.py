from django.urls import path

from .views import DocumentView, DocumentListView, ContactListView

urlpatterns = [
    path("", DocumentListView.as_view()),
    # path("contacts/", ContactListView.as_view()),
    path("<str:document_slug>/", DocumentView.as_view(), name="render-by-slug"),
]
