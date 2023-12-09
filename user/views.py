from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from user.models import Pupil, Parent, Teacher, User
from user.serializers import UserListSerializer, UserCreateSerializer, \
    UserUpdateSerializer


class UserListView(ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_type']
    search_fields = ['full_name', 'username']
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.user_type == User.UserTypeChoices.TEACHER:
            Teacher.objects.filter(user=user).delete()
        elif user.user_type == User.UserTypeChoices.PARENT:
            Parent.objects.filter(user=user).delete()
        elif user.user_type == User.UserTypeChoices.PUPIL:
            Pupil.objects.filter(user=user).delete()
        return super().destroy(request, *args, **kwargs)
