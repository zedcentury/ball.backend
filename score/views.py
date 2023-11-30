import datetime

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from score.serializers import ScoreCreateSerializer, ReasonListSerializer, ReasonCreateSerializer
from score.models import ScoreStat, Reason
from user.models import Pupil
from user.views import BaseCreateView


class ReasonListView(ListAPIView):
    """
    Holatlar ro'yxati
    """
    serializer_class = ReasonListSerializer
    queryset = Reason.objects.all()
    pagination_class = None


class ReasonCreateView(BaseCreateView):
    create_serializer_class = ReasonCreateSerializer
    retrieve_serializer_class = ReasonListSerializer


class ScoreView(APIView):
    """
    Har bir o'quvchi uchun shu kuni to'plagan umumiy ball
    """

    def get(self, request):
        pupil = Pupil.objects.filter(user=request.user).first()
        today = datetime.datetime.now()
        today_ball_stat = ScoreStat.objects.filter(pupil=pupil, created_at=today.date()).first()
        if today_ball_stat is None:
            return Response({'today': 100})
        return Response({'today': today_ball_stat.ball + 100})


class GoalsView(APIView):
    def get(self, request):
        user = request.user
        date_joined = user.date_joined.date()
        date_today = datetime.datetime.now().date()
        difference_days = (date_today - date_joined).days
        score_stats = ScoreStat.objects.filter(pupil__user=user)
        goals = {
            'excellent': 0,
            'good': 0,
            'bad': 0
        }
        index = 0
        initial_date = date_joined
        for _ in range(difference_days):
            try:
                if score_stats[index].createdAt == initial_date:
                    if score_stats[index].ball + 100 > 80:
                        goals['excellent'] += 1
                    elif score_stats[index].ball + 100 > 60:
                        goals['good'] += 1
                    else:
                        goals['bad'] += 1
                    index += 1
                else:
                    goals['excellent'] += 1
            except IndexError as e:
                goals['excellent'] += 1
            initial_date += datetime.timedelta(days=1)
        return Response({'goals': goals})


class ScoreStatsView(APIView):
    """
    Oxirgi 7kun natijalari
    """

    def get(self, request):
        user = request.user
        pupil = Pupil.objects.filter(user=request.user).first()
        today = datetime.datetime.now()

        start_date = today.date() - datetime.timedelta(days=7)
        end_date = today.date() - datetime.timedelta(days=1)

        if user.date_joined.date() > start_date:
            start_date = user.date_joined.date()

        last_week_score_stats = ScoreStat.objects.filter(pupil=pupil, createdAt__gte=start_date,
                                                         created_at__lte=end_date)

        scores = []
        difference = (end_date - start_date).days + 1

        for _ in range(difference):
            for stat in last_week_score_stats:
                if stat.created_at == end_date:
                    scores.append(stat.ball)
                    break
            else:
                scores.append(0)

            end_date -= datetime.timedelta(days=1)

        scores = list(map(lambda x: x + 100, scores))

        return Response({'scores': scores})


class ScoreCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    serializer_class = ScoreCreateSerializer
