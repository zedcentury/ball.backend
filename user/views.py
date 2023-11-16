from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from user.models import Pupil
from user.serializers import PupilsSerializer


class PupilsView(ListAPIView):
    serializer_class = PupilsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        return Pupil.objects.prefetch_related('user')
