from rest_framework import serializers

from ball.models import Ball, Reason


class ReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['id', 'text', 'score']


class BallCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ball
        fields = ['user', 'reason', 'score']
