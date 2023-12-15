import datetime

from django.db import models
from django.db.models import Q, Case, When, Sum
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.mixins import PaginationMixin
from config.permissions import IsAdmin, IsTeacher
from score.serializers import ScoreCreateSerializer, ReasonListSerializer, ReasonCreateSerializer, ScoreStatSerializer, \
    ReasonUpdateSerializer
from score.models import ScoreDaily, Reason, ScoreStat
from user.models import Pupil


class ReasonListView(PaginationMixin, ListAPIView):
    """
    Holatlar ro'yxati
    """
    permission_classes = [IsAdmin | IsTeacher]
    filter_backends = [SearchFilter]
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


class ScoreTodayView(APIView):
    """
    O'quvchining shu kuni to'plagan umumiy balli
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pk)
        today_date = datetime.datetime.now().date()
        today_score_daily = ScoreDaily.objects.filter(pupil=pupil, created_at=today_date).first()
        if today_score_daily is None:
            return Response({'today': 100})
        return Response({'today': today_score_daily.ball + 100})


class ScoreStatView(APIView):
    """
    Foydalanuvchining to'plagan ballari bo'yicha umumiy statistika
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pupil: Pupil = get_object_or_404(Pupil.objects.all(), user_id=pk)
        date_today = datetime.datetime.now().date()

        excellent_condition = Case(
            When(ball__gt=80 - 100, then=1),
            default=0,
            output_field=models.IntegerField(),
        )
        good_condition = Case(
            When(Q(ball__gt=60 - 100, ball__lte=80 - 100), then=1),
            default=0,
            output_field=models.IntegerField(),
        )
        bad_condition = Case(
            When(Q(ball__lte=60 - 100), then=1),
            default=0,
            output_field=models.IntegerField(),
        )

        result: dict = ScoreDaily.objects.filter(pupil=pupil).exclude(created_at=date_today).aggregate(
            excellent=Sum(excellent_condition),
            good=Sum(good_condition),
            bad=Sum(bad_condition),
        )

        result_count = sum(result.values())
        difference_days = (date_today - pupil.user.date_joined.date()).days

        result['excellent'] += difference_days - result_count

        if not ScoreStat.objects.filter(pupil=pupil).exists():
            score_stat = ScoreStat.objects.create(**{'pupil': pupil, **result})
        else:
            score_stat = ScoreStat.objects.filter(pupil=pupil, updated_at=date_today).first()
            if not score_stat:
                score_stat.excellent = result['excellent']
                score_stat.good = result['good']
                score_stat.bad = result['bad']
                score_stat.save()
        return Response(ScoreStatSerializer(score_stat).data)


class ScoreDailyListView(APIView):
    """
    Oxirgi 7 kun natijalari
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pk)
        user = pupil.user
        today_date = datetime.datetime.now().date()
        start_date = today_date - datetime.timedelta(days=7)
        end_date = today_date - datetime.timedelta(days=1)
        user_date_joined = user.date_joined.date()
        if user_date_joined > start_date:
            start_date = user_date_joined
        last_week_score_daily_list = ScoreDaily.objects.filter(pupil=pupil,
                                                               created_at__gte=start_date,
                                                               created_at__lte=end_date).order_by('-id')

        score_daily_list = []
        difference = (end_date - start_date).days + 1
        for _ in range(difference):
            for stat in last_week_score_daily_list:
                if stat.created_at == end_date:
                    score_daily_list.append(stat.ball + 100)
                    break
            else:
                score_daily_list.append(100)
            end_date -= datetime.timedelta(days=1)
        return Response({'scores': score_daily_list})


class ScoreCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    permission_classes = [IsTeacher]
    serializer_class = ScoreCreateSerializer
