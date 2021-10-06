from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from django.db.models import Exists, OuterRef

from apps.common import ImageTypes, PlatformTypes
from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import Brand, LocalBrand
from .serializers import BrandSerializer


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "platform",
                openapi.IN_QUERY,
                description="Takes the platform type: WEB, MOBILE",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class BrandListView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    pagination_class = None
    image_map = {
        1: ImageTypes.IMAGE_SQUARE,
        2: ImageTypes.IMAGE_SHORT,
        3: ImageTypes.IMAGE_TALL,
        4: ImageTypes.IMAGE_SQUARE,
        5: ImageTypes.IMAGE_SQUARE,
        6: ImageTypes.IMAGE_LONG,
    }

    def get_image_type(self, index):
        index = index % len(self.image_map) if index % len(self.image_map) != 0 else len(self.image_map)
        print("index is: ", index)
        return self.image_map[index]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'city_id': self.kwargs.get("city_id", None)
        }

    def get_queryset(self):
        city_id = self.kwargs.get("city_id")
        platform = self.request.GET.get('platform') or PlatformTypes.MOBILE
        platform = platform.upper()
        queryset = self.queryset
        if city_id:
            queryset = queryset.annotate(
                is_available=Exists(LocalBrand.objects.filter(brand_id=OuterRef('pk'), city_id=city_id))
            )
            if platform == PlatformTypes.MOBILE:
                for i, brand in enumerate(queryset):
                    setattr(brand, 'position', i+1)
                    setattr(
                        brand, 'image',
                        self.request.build_absolute_uri(getattr(brand, f"mobile_{self.get_image_type(i+1)}").url)
                        if getattr(brand, f"mobile_{self.get_image_type(i+1)}") else None)
                    setattr(
                        brand, 'favicon',
                        self.request.build_absolute_uri(brand.mobile_image_square.url) if brand.mobile_image_square else None)

            elif platform == PlatformTypes.WEB:
                for i, brand in enumerate(queryset):
                    setattr(brand, 'position', i + 1)
                    setattr(
                        brand, 'image_square',
                        self.request.build_absolute_uri(brand.web_image_square.url) if brand.web_image_square else None
                    )
                    setattr(
                        brand, 'image_long',
                        self.request.build_absolute_uri(brand.web_image_long.url) if brand.web_image_long else None
                    )
            # print(queryset)
            return queryset
