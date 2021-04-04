from .renderers import JSONRenderer


class JSONRendererMixin:
    renderer_classes = [JSONRenderer]
