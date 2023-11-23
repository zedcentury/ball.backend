from rest_framework.generics import ListAPIView

from common.models import ClassName
from common.serializers import ClassNamesSerializer


class ClassNamesView(ListAPIView):
    serializer_class = ClassNamesSerializer
    queryset = ClassName.objects.all()
    pagination_class = None
