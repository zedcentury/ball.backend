from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from common.models import ClassName
from user.models import Pupil, User


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']


class TeacherCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'first_name', 'last_name', 'username']
        extra_kwargs = {
            'first_name': {
                'write_only': True
            },
            'last_name': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        validated_data['userType'] = User.UserTypeChoices.TEACHER
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)
        return user


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']


class ParentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

    def create(self, validated_data):
        validated_data['userType'] = User.UserTypeChoices.PARENT
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)
        return user


class PupilsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    username = serializers.CharField(source='user.username')
    class_name = serializers.CharField(source='class_name.name')

    class Meta:
        model = Pupil
        fields = ['id', 'full_name', 'username', 'class_name']


class PupilCreateSerializer(serializers.ModelSerializer):
    class_name = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'class_name']

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        class_name = validated_data.pop('class_name')

        validated_data['userType'] = User.UserTypeChoices.PUPIL
        validated_data['password'] = '1'

        user = User.objects.create_user(**validated_data)

        class_name_obj = get_object_or_404(ClassName.objects.all(), id=class_name)
        Pupil.objects.create(user=user, class_name=class_name_obj)

        return user
