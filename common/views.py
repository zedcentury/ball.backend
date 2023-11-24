from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ClassName
from common.serializers import ClassNamesSerializer
from user.models import User, Pupil


class ClassNamesView(ListAPIView):
    serializer_class = ClassNamesSerializer
    queryset = ClassName.objects.all()
    pagination_class = None


class StatView(APIView):
    def get(self, request):
        teachers_count = User.objects.filter(userType=User.UserTypeChoices.TEACHER).count()
        pupils_count = Pupil.objects.count()
        class_names_count = ClassName.objects.count()

        return Response({
            'teachers': teachers_count,
            'pupils': pupils_count,
            'class_names': class_names_count
        })
