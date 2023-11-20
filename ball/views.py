import datetime

from django.db.models import Sum, Q
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ball.models import Ball, Reason, BallStat
from ball.serializers import BallCreateSerializer, ReasonsSerializer
from config.permissions import IsStudent, IsParent, IsTeacher
from user.models import User


class ReasonsView(ListAPIView):
    """
    Holatlar ro'yxati
    """
    serializer_class = ReasonsSerializer
    queryset = Reason.objects.all()


class BallView(APIView):
    """
    Har bir o'quvchi uchun shu kuni to'plagan umumiy ball
    """

    def get(self, request):
        today = datetime.datetime.now()
        today_ball_stat = BallStat.objects.filter(user=request.user, createdAt=today.date()).first()

        if today_ball_stat is None:
            return Response({'today': 100})

        return Response({'today': today_ball_stat.score + 100})


class BallStatsView(APIView):
    """
    Oxirgi 7kun natijalari
    """

    def get(self, request):
        user = request.user
        today = datetime.datetime.now()

        start_date = today.date() - datetime.timedelta(days=7)
        end_date = today.date() - datetime.timedelta(days=1)

        if user.date_joined.date() > start_date:
            start_date = user.date_joined.date()

        last_week_ball_stats = BallStat.objects.filter(user=user, createdAt__gte=start_date, createdAt__lte=end_date)

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
