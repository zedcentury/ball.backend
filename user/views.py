import time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Pupil, User
from user.serializers import PupilsSerializer, PupilCreateSerializer, \
    TeachersSerializer, TeacherCreateSerializer, ParentsSerializer, \
    ParentCreateSerializer


class BaseCreateView(APIView):
    create_serializer_class = None
    retrieve_serializer_class = None

    def post(self, request, *args, **kwargs):
        create_serializer = self.create_serializer_class(data=request.data)
        if create_serializer.is_valid():
            instance = create_serializer.save()
            retrieve_serializer = self.retrieve_serializer_class(instance)
            return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeachersView(ListAPIView):
    serializer_class = TeachersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']

    def get_queryset(self):
        return User.objects.filter(userType=User.UserTypeChoices.TEACHER)


class TeacherCreateView(BaseCreateView):
    create_serializer_class = TeacherCreateSerializer
    retrieve_serializer_class = TeachersSerializer


class ParentsView(ListAPIView):
    serializer_class = ParentsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']

    def get_queryset(self):
        return User.objects.filter(userType=User.UserTypeChoices.PARENT)


class ParentCreateView(BaseCreateView):
    create_serializer_class = ParentCreateSerializer
    retrieve_serializer_class = ParentsSerializer


class PupilsView(ListAPIView):
    serializer_class = PupilsSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    filterset_fields = ['class_name_id']

    def get_queryset(self):
        time.sleep(3)
        return Pupil.objects.prefetch_related('user')


class PupilCreateView(BaseCreateView):
    create_serializer_class = PupilCreateSerializer
    retrieve_serializer_class = PupilsSerializer
