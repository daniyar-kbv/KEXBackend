from constance import config
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView

from config.constants.contacts import CONTACTS
from apps.common.mixins import PublicAPIMixin, PublicJSONRendererMixin

from .models import Document
from .serializers import DocumentListSerializer


class DocumentView(PublicAPIMixin, APIView):
    queryset = Document.objects.all()

    def get(self, request, document_slug):
        content = None
        document = self.queryset.filter(slug=document_slug)
        if document.exists():
            content = document.first().template
            content = getattr(content, request.headers.get('Language'))
        return render(request, 'docs/template_page.html', {'content': content})


class DocumentListViewOld(PublicJSONRendererMixin, ListAPIView):
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


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "for_web",
                openapi.IN_QUERY,
                description="Defines the docs for footer in website: 1, 0",
                type=openapi.TYPE_BOOLEAN,
            )
        ]
    ),
)
class DocumentListView(PublicJSONRendererMixin, ListAPIView):
    queryset = Document.objects.all().order_by('priority')
    serializer_class = DocumentListSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.GET.get('for_web') == 'true':
            return super().get_queryset().filter(for_web=True)
        return super().get_queryset().filter(for_web=False)


class ContactListView(PublicJSONRendererMixin, APIView):
    def get(self, request, *args, **kwargs):  # noqa
        return Response([
            {"name": contact, "value": getattr(config, contact)}
            for contact in CONTACTS.keys()
        ])
