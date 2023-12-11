from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ClassName
from config.mixins import PaginationMixin
from user.filters import UserFilter
from user.models import Pupil, Parent, Teacher, User
from user.serializers import UserListSerializer, UserCreateSerializer, \
    UserUpdateSerializer, AttachParentToPupilSerializer, AttachClassNameToPupilSerializer


class UserListView(PaginationMixin, ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
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


class AttachParentToPupilView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AttachParentToPupilSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get('parent')
        pupil = serializer.validated_data.get('pupil')
        parent_obj = get_object_or_404(Parent.objects.all(), user_id=parent)
        pupil_obj = get_object_or_404(Pupil.objects.all(), user_id=pupil)
        if parent_obj.children.filter(user_id=pupil).exists():
            raise ValidationError({'pupil': 'Bu o\'quvchi allaqachon biriktirilgan'})
        parent_obj.children.add(pupil_obj)
        parent_obj.save()
        return Response('Success')


class AttachClassNameToPupilView(APIView):
    def post(self, request):
        serializer = AttachClassNameToPupilSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        class_name = serializer.validated_data.get('class_name')
        pupil = serializer.validated_data.get('pupil')
        class_name_obj = get_object_or_404(ClassName.objects.all(), id=class_name)
        pupil_obj: Pupil = get_object_or_404(Pupil.objects.all(), user_id=pupil)
        if pupil_obj.class_name_id == class_name_obj.id:
            raise ValidationError({'pupil': 'Bu o\'quvchi allaqachon sinfga biriktirilgan'})
        pupil_obj.class_name = class_name_obj
        pupil_obj.save()
        return Response('Success')


class CancelAttachParentView(APIView):
    def delete(self, request, parent, pupil):
        parent_obj = get_object_or_404(Parent.objects.all(), user_id=parent)
        pupil_obj = get_object_or_404(Pupil.objects.all(), user_id=pupil)
        parent_obj.children.remove(pupil_obj)
        parent_obj.save()
        return Response('Success')


class CancelAttachClassNameView(APIView):
    def delete(self, request, pk):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pk)
        pupil.class_name = None
        pupil.save()
        return Response('Success')
