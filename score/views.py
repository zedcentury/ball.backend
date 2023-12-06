import datetime

from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.mixins import PaginationMixin
from score.serializers import ScoreCreateSerializer, ReasonListSerializer, ReasonCreateSerializer, ScoreStatSerializer
from score.models import ScoreDaily, Reason, ScoreStat
from user.models import Pupil, User
from user.views import BaseCreateView


class ReasonListView(PaginationMixin, ListAPIView):
    """
    Holatlar ro'yxati
    """
    serializer_class = ReasonListSerializer
    queryset = Reason.objects.all()


class ReasonCreateView(BaseCreateView):
    """
    Holat qo'shish
    """
    create_serializer_class = ReasonCreateSerializer
    retrieve_serializer_class = ReasonListSerializer


class ScoreTodayView(APIView):
    """
    O'quvchining shu kuni to'plagan umumiy balli
    """

    def get(self, request, user_id):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=user_id)
        today = datetime.datetime.now()
        today_score_daily = ScoreDaily.objects.filter(pupil=pupil, created_at=today.date()).first()
        if today_score_daily is None:
            return Response({'today': 100})
        return Response({'today': today_score_daily.ball + 100})


class ScoreStatView(APIView):
    """
    Foydalanuvchining to'plagan ballari bo'yicha umumiy statistika
    """

    def get(self, request, user_id):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=user_id)
        date_today = datetime.datetime.now().date()

        # Agar bugun o'quvchining statiktikasi ScoreStat modelida yangilangan bo'lsa,
        # ma'lumotlar modeldan olinadi
        score_stat: ScoreStat = ScoreStat.objects.filter(pupil=pupil, updated_at=date_today).first()
        if score_stat:
            return Response(ScoreStatSerializer(score_stat).data)

        date_joined = pupil.user.date_joined.date()
        difference_days = (date_today - date_joined).days
        score_stats = ScoreDaily.objects.filter(pupil=pupil)
        stats = {
            'excellent': 0,
            'good': 0,
            'bad': 0
        }
        index = 0
        initial_date = date_joined
        for _ in range(difference_days):
            try:
                if score_stats[index].created_at == initial_date:
                    if score_stats[index].ball + 100 > 80:
                        stats['excellent'] += 1
                    elif score_stats[index].ball + 100 > 60:
                        stats['good'] += 1
                    else:
                        stats['bad'] += 1
                    index += 1
                else:
                    stats['excellent'] += 1
            except IndexError as e:
                stats['excellent'] += 1
            initial_date += datetime.timedelta(days=1)

        # Foydalanuvchi ScoreStat modelida mavjud bo'lsa, ma'lumotlar yangilanadi
        score_stat = ScoreStat.objects.filter(pupil=pupil).first()
        if score_stat:
            score_stat.excellent = stats['excellent']
            score_stat.good = stats['excellent']
            score_stat.bad = stats['bad']
            score_stat.save()
            return Response(ScoreStatSerializer(score_stat).data)

        # Agar foydalanuvchi ScoreStat modelida mavjud bo'lmasa,
        score_stat = ScoreStat.objects.create(**{'pupil': pupil, **stats})
        return Response(ScoreStatSerializer(score_stat).data)


class ScoreDailyListView(APIView):
    """
    Oxirgi 7 kun natijalari
    """

    def get(self, request, user_id):
        pupil = get_object_or_404(Pupil.objects.all(), user_id=user_id)
        user = pupil.user
        today_date = datetime.datetime.now().date()
        start_date = today_date - datetime.timedelta(days=7)
        end_date = today_date - datetime.timedelta(days=1)
        if user.date_joined.date() > start_date:
            start_date = user.date_joined.date()
        last_week_score_daily_list = ScoreDaily.objects.filter(pupil=pupil,
                                                               created_at__gte=start_date,
                                                               created_at__lte=end_date)
        score_daily_list = []
        difference = (end_date - start_date).days + 1
        for _ in range(difference):
            for stat in last_week_score_daily_list:
                if stat.created_at == end_date:
                    score_daily_list.append(stat.ball)
                    break
            else:
                score_daily_list.append(0)
            end_date -= datetime.timedelta(days=1)
        score_daily_list = list(map(lambda x: x + 100, score_daily_list))
        return Response({'scores': score_daily_list})


class ScoreCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    serializer_class = ScoreCreateSerializer
