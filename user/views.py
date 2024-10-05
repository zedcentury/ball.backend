import datetime

from django.db import transaction
from django.db.models import F, Subquery, OuterRef, Case, When, Value, CharField, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView, get_object_or_404, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ClassName
from config.mixins import PaginationMixin
from config.permissions import IsAdmin, IsTeacher, IsParent
from score.models import ScoreMonth
from user.filters import UserFilter
from user.models import Pupil, Parent, Teacher, User
from user.serializers import UserListSerializer, UserCreateSerializer, UserUpdateSerializer, \
    AttachPupilToParentSerializer, AttachPupilToClassNameSerializer, UserRetrieveSerializer


class UserListView(PaginationMixin, ListAPIView):
    permission_classes = [IsAdmin | IsTeacher | IsParent]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
    search_fields = ['full_name', 'username']
    serializer_class = UserListSerializer

    def get_queryset(self):
        today = datetime.datetime.now()

        return (
            User.objects.order_by('full_name').
            prefetch_related('pupil_to_user__class_name', 'score_month_to_user').
            annotate(class_name=Case(
                When(
                    pupil_to_user__class_name__name__isnull=False,
                    then=F('pupil_to_user__class_name__name')
                ),
                default=Value("-", output_field=CharField())
            )).
            annotate(latest_ball=Coalesce(Subquery(
                ScoreMonth.objects.filter(user_id=OuterRef('pk'),
                                          created_at__month=today.month,
                                          created_at__year=today.year).
                order_by('-created_at').values('ball')[:1]), 0)).
            annotate(latest_ball=F('latest_ball') + 100))


class UserCreateView(CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserDestroyView(DestroyAPIView):
    permission_classes = [IsAdmin]
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


class AttachPupilToParentView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AttachPupilToParentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent_user = serializer.validated_data.get('parent')
        pupil_user = serializer.validated_data.get('pupil')

        parent = get_object_or_404(Parent.objects.all(), user_id=parent_user)
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pupil_user)

        if parent.children.filter(user_id=pupil_user).exists():
            raise ValidationError({'pupil': 'Bu o\'quvchi allaqachon biriktirilgan'})

        parent.children.add(pupil)
        parent.save()
        return Response('Success')


class AttachPupilToClassNameView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AttachPupilToClassNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = serializer.validated_data.get('class_name')
        pupil_user = serializer.validated_data.get('pupil')

        class_name = get_object_or_404(ClassName.objects.all(), id=class_name)
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pupil_user)

        if pupil.class_name is not None:
            raise ValidationError({'pupil': 'Bu o\'quvchi allaqachon sinfga biriktirilgan'})

        pupil.class_name = class_name
        pupil.save()
        return Response('Success')


class DetachPupilFromParentView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, parent, pupil):
        parent_obj = get_object_or_404(Parent.objects.all(), user_id=parent)
        pupil_obj = get_object_or_404(Pupil.objects.all(), user_id=pupil)

        parent_obj.children.remove(pupil_obj)
        parent_obj.save()
        return Response('Success')


class DetachPupilFromClassNameView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, pk):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pk)
        pupil.class_name = None
        pupil.save()
        return Response('Success')


class PupilStatsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        today = datetime.date.today()

        return Response({
            "perfect": User.objects.filter(
                user_type=User.UserTypeChoices.PUPIL,
                score_month_to_user__ball__gt=100 - 100,
                score_month_to_user__created_at__month=today.month,
                score_month_to_user__created_at__year=today.year
            ).count(),
            "best": User.objects.filter(
                Q(score_month_to_user__ball__gte=72 - 100,
                  score_month_to_user__ball__lte=100 - 100,
                  score_month_to_user__created_at__month=today.month,
                  score_month_to_user__created_at__year=today.year,
                  user_type=User.UserTypeChoices.PUPIL) |
                Q(score_month_to_user__isnull=True,
                  user_type=User.UserTypeChoices.PUPIL)
            ).count(),
            "good": User.objects.filter(
                score_month_to_user__ball__gte=55 - 100,
                score_month_to_user__ball__lt=72 - 100,
                score_month_to_user__created_at__month=today.month,
                score_month_to_user__created_at__year=today.year,
                user_type=User.UserTypeChoices.PUPIL,
            ).count(),
            "bad": User.objects.filter(
                score_month_to_user__ball__lt=55 - 100,
                score_month_to_user__created_at__month=today.month,
                score_month_to_user__created_at__year=today.year,
                user_type=User.UserTypeChoices.PUPIL,
            ).count()
        })
