from django.shortcuts import render
from django.urls import resolve


from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import Document
from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin
from .serializers import DocumentListSerializer


class DocumentView(PublicAPIMixin, APIView):
    queryset = Document.objects.all()

    def get(self, request, document_slug):
        content = None
        document = self.queryset.filter(slug=document_slug)
        if document.exists():
            print('exists baby')
            content = document.first().template
            content = getattr(content, request.headers.get('Language'))
        return render(request, 'docs/template_page.html', {'content': content})


class DocumentListView(JSONPublicAPIMixin, ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer

    def get_queryset(self):
        app_name = self.request.path
        print("app_name: ", app_name)
        queryset = self.queryset.all()

        for doc in queryset:
            link = self.request.build_absolute_uri(app_name + doc.slug)
            setattr(doc, 'link', link)

        return queryset