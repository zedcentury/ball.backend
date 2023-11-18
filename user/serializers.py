from rest_framework import serializers

from user.models import Pupil, User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'userType']


class PupilsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Pupil
        fields = ['id', 'full_name', 'class_name']
