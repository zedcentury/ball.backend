import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.mixins import PaginationMixin
from config.permissions import IsAdmin, IsTeacher
from score.serializers import ScoreCreateSerializer, ReasonListSerializer, ReasonCreateSerializer, \
    ReasonUpdateSerializer, ScoreListSerializer
from score.models import Reason, Score, ScoreMonth
from user.models import User


class ReasonListView(PaginationMixin, ListAPIView):
    """
    Holatlar ro'yxati
    """
    permission_classes = [IsAdmin | IsTeacher]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_type']
    search_fields = ['text']
    serializer_class = ReasonListSerializer
    queryset = Reason.objects.all()


class ReasonCreateView(APIView):
    """
    Holat qo'shish
    """
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = ReasonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.save()
        return Response(ReasonListSerializer(reason).data)


class ReasonUpdateView(UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReasonUpdateSerializer
    queryset = Reason.objects.all()


class ReasonDestroyView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Reason.objects.all()


class ScoreCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    permission_classes = [IsAdmin | IsTeacher]
    serializer_class = ScoreCreateSerializer


class ScoreListView(PaginationMixin, ListAPIView):
    serializer_class = ScoreListSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return Score.objects.filter(pupil__user_id=user_id, created_at__gte=today_date)


class ScoreMonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User.objects.all(), id=pk)
        today = datetime.datetime.now()
        score_month = ScoreMonth.objects.filter(user=user, created_at__month=today.month,
                                                created_at__year=today.year).first()
        if bool(score_month):
            return Response({'result': score_month.ball})
        return Response({'result': 100})
