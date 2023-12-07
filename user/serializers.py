from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import Pupil, User, Parent, Teacher


class TeachersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'full_name']


class TeacherCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, write_only=True)
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'username']

    def validate(self, attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError({'username': 'Username is already exist'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data['userType'] = User.UserTypeChoices.TEACHER
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)
        teacher = Teacher.objects.create(user=user)
        return teacher


class ParentsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Parent
        fields = ['id', 'username', 'full_name']


class ParentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, write_only=True)
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'first_name', 'last_name', 'username']

    def validate(self, attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError({'username': 'Username is already exist'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data['userType'] = User.UserTypeChoices.PARENT
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)
        parent = Parent.objects.create(user=user)
        return parent


class PupilsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    username = serializers.CharField(source='user.username')
    class_name = serializers.CharField(source='class_name.name')
    today_ball = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pupil
        fields = ['id', 'user_id', 'full_name', 'username', 'class_name', 'today_ball']


class PupilCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, write_only=True)
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Pupil
        fields = ['username', 'first_name', 'last_name', 'class_name']

    def validate(self, attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError({'username': 'Username is already exist'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        class_name = validated_data.pop('class_name')
        validated_data['userType'] = User.UserTypeChoices.PUPIL
        validated_data['password'] = '1'
        user = User.objects.create_user(**validated_data)
        pupil = Pupil.objects.create(user=user, class_name=class_name)
        return pupil
