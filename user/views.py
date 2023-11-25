from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView

from user.models import Pupil, User
from user.serializers import PupilsSerializer, PupilCreateSerializer, \
    TeachersSerializer, TeacherCreateSerializer, ParentsSerializer, \
    ParentCreateSerializer


class TeachersView(ListAPIView):
    serializer_class = TeachersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']

    def get_queryset(self):
        return User.objects.filter(userType=User.UserTypeChoices.TEACHER)


class TeacherCreateView(CreateAPIView):
    serializer_class = TeacherCreateSerializer


class ParentsView(ListAPIView):
    serializer_class = ParentsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']

    def get_queryset(self):
        return User.objects.filter(userType=User.UserTypeChoices.PARENT)


class ParentCreateView(CreateAPIView):
    serializer_class = ParentCreateSerializer


class PupilsView(ListAPIView):
    serializer_class = PupilsSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    filterset_fields = ['class_name_id']
    pagination_class = None

    def get_queryset(self):
        return Pupil.objects.prefetch_related('user')


class PupilCreateView(CreateAPIView):
    serializer_class = PupilCreateSerializer
