from django.db import transaction
from rest_framework import serializers
from user.models import Pupil, User, Parent, Teacher


class UserListSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField()
    latest_ball = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'class_name', 'latest_ball']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'user_type']
        extra_kwargs = {
            'user_type': {
                'write_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)

        user_type = validated_data.get('user_type')
        if user_type == User.UserTypeChoices.TEACHER:
            Teacher.objects.create(user=user)
        elif user_type == User.UserTypeChoices.PARENT:
            Parent.objects.create(user=user)
        elif user_type == User.UserTypeChoices.PUPIL:
            Pupil.objects.create(user=user)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name']


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name']


class AttachPupilToParentSerializer(serializers.Serializer):
    parent = serializers.IntegerField()
    pupil = serializers.IntegerField()


class AttachPupilToClassNameSerializer(serializers.Serializer):
    class_name = serializers.IntegerField()
    pupil = serializers.IntegerField()
