from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from django.db.models import Exists, OuterRef

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from . import BrandImageTypes, PlatformTypes
from .models import Brand, BrandImage, LocalBrand
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
        1: BrandImageTypes.IMAGE_SQUARE,
        2: BrandImageTypes.IMAGE_SHORT,
        3: BrandImageTypes.IMAGE_TALL,
        4: BrandImageTypes.IMAGE_SQUARE,
        5: BrandImageTypes.IMAGE_SQUARE,
        6: BrandImageTypes.IMAGE_LONG,
    }

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
                    blocks_amount = len(self.image_map)
                    imgs = BrandImage.objects.for_mobile().filter(
                        brand_id=brand.id,
                        image_type=self.image_map[(i + 1) % blocks_amount if (i + 1) != blocks_amount else blocks_amount]
                    )
                    # print(imgs)
                    img = imgs.first()
                    if img:
                        img = self.request.build_absolute_uri(img.image.url)
                    setattr(brand, 'image', img)
                    setattr(brand, 'position', i+1)

            elif platform == PlatformTypes.WEB:
                for i, brand in enumerate(queryset):
                    image_square = None
                    image_long = None
                    imgs = BrandImage.objects.for_web().filter(
                        brand_id=brand.id,
                        image_type__in=[BrandImageTypes.IMAGE_SQUARE, BrandImageTypes.IMAGE_LONG]
                    )
                    if imgs.image_longs().exists():
                        image_long = self.request.build_absolute_uri(imgs.image_longs().first().image.url)
                    if imgs.image_squares().exists():
                        image_square = self.request.build_absolute_uri(imgs.image_squares().first().image.url)
                    setattr(brand, 'image_square', image_square)
                    setattr(brand, 'image_long', image_long)
                    setattr(brand, 'position', i + 1)
            # print(queryset)
            return queryset
