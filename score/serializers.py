from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from score.models import ScoreDaily, Score, Reason, ScoreStat
from user.models import Pupil


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

    @staticmethod
    def validate_ball(value):
        if value == 0:
            raise ValidationError('Ball 0ga teng bo\'lishi mumkin emas')
        return value


class ReasonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['text', 'ball']

    def validate(self, attrs):
        return attrs


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['pupil', 'reason', 'ball']

    @staticmethod
    def validate_ball(value):
        if value == 0:
            raise ValidationError('Ball 0ga teng bo\'lishi mumkin emas')
        return value

    @transaction.atomic
    def create(self, validated_data):
        pupil = validated_data.get('pupil')
        pupil = get_object_or_404(Pupil.objects.all(), user_id=pupil.id)
        validated_data['pupil'] = pupil
        score = super().create(validated_data)
        ball = score.ball
        score_daily: ScoreDaily = ScoreDaily.objects.filter(pupil=pupil, created_at=score.created_at).first()
        if score_daily:
            score_daily.ball += ball
            score_daily.save()
        else:
            ScoreDaily.objects.create(pupil=pupil, ball=ball)
        return score


class ScoreStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreStat
        fields = ['excellent', 'good', 'bad']
