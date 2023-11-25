from django.db.models import Count
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ball.models import Reason
from common.models import ClassName
from common.serializers import ClassNamesSerializer, ClassNameCreateSerializer
from user.models import User, Pupil


class ClassNamesView(ListAPIView):
    serializer_class = ClassNamesSerializer
    pagination_class = None

    def get_queryset(self):
        return ClassName.objects.prefetch_related('pupil_to_class_name').annotate(
            pupils_count=Count('pupil_to_class_name', distinct=True)
        )


class ClassNameCreateView(CreateAPIView):
    serializer_class = ClassNameCreateSerializer


class StatView(APIView):
    def get(self, request):
        teachers_count = User.objects.filter(userType=User.UserTypeChoices.TEACHER).count()
        pupils_count = Pupil.objects.count()
        class_names_count = ClassName.objects.count()
        reasons_count = Reason.objects.count()

        return Response({
            'teachers': teachers_count,
            'pupils': pupils_count,
            'class_names': class_names_count,
            'reasons': reasons_count
        })
