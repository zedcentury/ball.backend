from rest_framework import serializers

from user.models import Pupil


class PupilsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Pupil
        fields = ['id', 'full_name', 'class_name']
