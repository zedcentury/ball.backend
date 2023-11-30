import datetime

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ball.models import Reason, BallStat
from ball.serializers import BallCreateSerializer, ReasonsSerializer, ReasonCreateSerializer
from user.models import Pupil
from user.views import BaseCreateView


class ReasonsView(ListAPIView):
    """
    Holatlar ro'yxati
    """
    serializer_class = ReasonsSerializer
    queryset = Reason.objects.all()
    pagination_class = None


class ReasonCreateView(BaseCreateView):
    create_serializer_class = ReasonCreateSerializer
    retrieve_serializer_class = ReasonsSerializer


class BallView(APIView):
    """
    Har bir o'quvchi uchun shu kuni to'plagan umumiy ball
    """

    def get(self, request):
        pupil = Pupil.objects.filter(user=request.user).first()
        today = datetime.datetime.now()
        today_ball_stat = BallStat.objects.filter(pupil=pupil, createdAt=today.date()).first()
        if today_ball_stat is None:
            return Response({'today': 100})
        return Response({'today': today_ball_stat.score + 100})


class GoalsView(APIView):
    def get(self, request):
        user = request.user
        date_joined = user.date_joined.date()
        date_today = datetime.datetime.now().date()
        difference_days = (date_today - date_joined).days
        ball_stats = BallStat.objects.filter(pupil__user=user)
        goals = {
            'excellent': 0,
            'good': 0,
            'bad': 0
        }
        index = 0
        initial_date = date_joined
        for _ in range(difference_days):
            try:
                if ball_stats[index].createdAt == initial_date:
                    if ball_stats[index].score + 100 > 80:
                        goals['excellent'] += 1
                    elif ball_stats[index].score + 100 > 60:
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


class BallStatsView(APIView):
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

        last_week_ball_stats = BallStat.objects.filter(pupil=pupil, createdAt__gte=start_date, createdAt__lte=end_date)

        scores = []
        difference = (end_date - start_date).days + 1

        for _ in range(difference):
            for stat in last_week_ball_stats:
                if stat.createdAt == end_date:
                    scores.append(stat.score)
                    break
            else:
                scores.append(0)

            end_date -= datetime.timedelta(days=1)

        scores = list(map(lambda x: x + 100, scores))

        return Response({'scores': scores})


class BallCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    # permission_classes = [IsTeacher]
    serializer_class = BallCreateSerializer
