from django.db.models import Count, RestrictedError
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ClassName
from common.serializers import ClassNameListSerializer, ClassNameCreateSerializer, ClassNameUpdateSerializer
from config.mixins import PaginationMixin
from config.permissions import IsAdmin
from score.models import Reason
from user.models import User, Pupil, Parent


class ClassNameListView(PaginationMixin, ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']
    serializer_class = ClassNameListSerializer

    def get_queryset(self):
        return ClassName.objects.prefetch_related('pupil_to_class_name').annotate(
            pupils_count=Count('pupil_to_class_name', distinct=True)
        ).order_by('name')


class ClassNameCreateView(CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ClassNameCreateSerializer


class ClassNameUpdateView(UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ClassNameUpdateSerializer
    queryset = ClassName.objects.all()


class ClassNameDestroyView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = ClassName.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except RestrictedError as e:
            return Response('Sinfga bog\'langan o\'quvchilar bor', status=status.HTTP_400_BAD_REQUEST)


class StatView(APIView):
    permission_classes = [IsAdmin]

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
