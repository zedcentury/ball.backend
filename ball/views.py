import datetime

from django.db.models import Sum, Q
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ball.models import Ball, Reason
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

    # permission_classes = [(IsParent | IsStudent) & IsAuthenticated]

    def get(self, request):
        # user = request.user
        user = User.objects.get(id=2)
        today = datetime.datetime.now()
        last_week = [today - datetime.timedelta(days=i) for i in range(1, 8)]
        aggregate_dict = {
            f'{day.day}/{day.month}/{day.year}': Sum('score', filter=Q(createdAt__day=day.day), default=0) for day in
            last_week
        }

        score = Ball.objects.filter(user=user).aggregate(
            **{'today': Sum('score', filter=Q(createdAt__day=today.day), default=0), **aggregate_dict})

        score = dict(list(score.items())[:(today.date() - user.date_joined.date()).days + 1])

        score = dict(map(lambda item: (item[0], item[1] + 100), score.items()))

        return Response(score)


class BallCreateView(CreateAPIView):
    """
    O'qituvchi tomonidan ball berish
    """
    # permission_classes = [IsTeacher]
    serializer_class = BallCreateSerializer
