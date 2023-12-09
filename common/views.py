from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ClassName
from common.serializers import ClassNameListSerializer, ClassNameCreateSerializer, ClassNameUpdateSerializer
from config.mixins import PaginationMixin
from score.models import Reason
from user.models import User, Pupil, Parent


class ClassNameListView(PaginationMixin, ListAPIView):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    serializer_class = ClassNameListSerializer

    def get_queryset(self):
        return ClassName.objects.prefetch_related('pupil_to_class_name').annotate(
            pupils_count=Count('pupil_to_class_name', distinct=True)
        ).order_by('name')


class ClassNameCreateView(CreateAPIView):
    serializer_class = ClassNameCreateSerializer


class ClassNameUpdateView(UpdateAPIView):
    serializer_class = ClassNameUpdateSerializer
    queryset = ClassName.objects.all()


class ClassNameDestroyView(DestroyAPIView):
    queryset = ClassName.objects.all()


class StatView(APIView):
    def get(self, request):
        teachers_count = User.objects.filter(user_type=User.UserTypeChoices.TEACHER).count()
        parents_count = Parent.objects.count()
        pupils_count = Pupil.objects.count()
        class_names_count = ClassName.objects.count()
        reasons_count = Reason.objects.count()

        return Response({
            'teachers': teachers_count,
            'parents': parents_count,
            'pupils': pupils_count,
            'class_names': class_names_count,
            'reasons': reasons_count
        })
