from django.db import transaction
from rest_framework import serializers

from user.models import Pupil, User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'userType']


class PupilsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Pupil
        fields = ['id', 'full_name', 'class_name']


class PupilCreateSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'class_name']

    @transaction.atomic
    def create(self, validated_data):
        class_name = validated_data.pop('class_name')

        validated_data['userType'] = User.UserTypeChoices.PUPIL

        user = User.objects.create_user(**validated_data)

        Pupil.objects.create(user=user, class_name=class_name)

        return user
