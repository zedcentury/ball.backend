from django.db import transaction
from rest_framework import serializers

from ball.models import Ball, Reason, BallStat


class ReasonsSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = Reason
        fields = ['id', 'text', 'score']

    @staticmethod
    def get_score(obj):
        if obj.score > 0:
            return f'+{obj.score}'
        return str(obj.score)


class ReasonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['text', 'score']


class BallCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ball
        fields = ['pupil', 'reason', 'score']

    @transaction.atomic
    def create(self, validated_data):
        ball = super().create(validated_data)
        pupil = ball.pupil
        score = ball.score
        ball_stat: BallStat = BallStat.objects.filter(pupil=pupil, createdAt=ball.createdAt).first()
        if ball_stat:
            ball_stat.score += score
            ball_stat.save()
        else:
            BallStat.objects.create(pupil=pupil, score=score)
        return ball
