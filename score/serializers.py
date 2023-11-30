from django.db import transaction
from rest_framework import serializers

from score.models import ScoreStat, Score, Reason


class ReasonListSerializer(serializers.ModelSerializer):
    ball = serializers.SerializerMethodField()

    class Meta:
        model = Reason
        fields = ['id', 'text', 'ball']

    @staticmethod
    def get_ball(obj):
        if obj.ball > 0:
            return f'+{obj.ball}'
        return str(obj.ball)


class ReasonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['text', 'ball']


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['pupil', 'reason', 'ball']

    @transaction.atomic
    def create(self, validated_data):
        score = super().create(validated_data)
        pupil = score.pupil
        ball = score.ball
        score_stat: ScoreStat = ScoreStat.objects.filter(pupil=pupil, created_at=score.created_at).first()
        if score_stat:
            score_stat.ball += ball
            score_stat.save()
        else:
            ScoreStat.objects.create(pupil=pupil, ball=ball)
        return score
