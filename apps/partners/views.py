from rest_framework.generics import ListAPIView
from django.db.models import Exists, OuterRef

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from . import BrandImageTypes
from .models import Brand, BrandImage, LocalBrand
from .serializers import BrandSerializer


class BrandListView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
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
        queryset = self.queryset
        if city_id:
            queryset = queryset.annotate(
                is_available=Exists(LocalBrand.objects.filter(brand_id=OuterRef('pk'), city_id=city_id))
            )
            for i, brand in enumerate(queryset):
                blocks_amount = len(self.image_map)
                img = BrandImage.objects.filter(brand_id=brand.id, image_type=self.image_map[(i + 1) % blocks_amount])
                if img.exists():
                    img = img.first().image
                    img = self.request.build_absolute_uri(img.url)
                setattr(brand, 'image', img)
                setattr(brand, 'position', i+1)

            return queryset
