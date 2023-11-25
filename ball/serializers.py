from rest_framework import serializers

from ball.models import Ball, Reason


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
