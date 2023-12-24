import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from score.models import Score, Reason, ScoreMonth
from user.models import Pupil, User


class ReasonListSerializer(serializers.ModelSerializer):
    ball = serializers.SerializerMethodField()

    class Meta:
        model = Reason
        fields = ['id', 'text', 'ball', 'user_type']

    @staticmethod
    def get_ball(obj):
        if obj.ball > 0:
            return f'+{obj.ball}'
        return str(obj.ball)


class ReasonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['text', 'ball', 'user_type']

    def validate(self, attrs):
        text = attrs.get('text')
        user_type = attrs.get('user_type')
        if Reason.objects.filter(user_type=user_type, text=text).exists():
            raise ValidationError({'text': 'Bu holat allaqachon mavjud'})
        return attrs

    @staticmethod
    def validate_ball(value):
        if value == 0:
            raise ValidationError('Ball 0ga teng bo\'lishi mumkin emas')
        return value


class ReasonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['text', 'ball', 'user_type']

    def validate(self, attrs):
        text = attrs.get('text')
        user_type = attrs.get('user_type')
        if Reason.objects.filter(user_type=user_type, text=text).exclude(id=self.instance.id).exists():
            raise ValidationError({'text': 'Bu holat allaqachon mavjud'})
        return attrs

    @staticmethod
    def validate_ball(value):
        if value == 0:
            raise ValidationError('Ball 0ga teng bo\'lishi mumkin emas')
        return value


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['user', 'reason', 'ball']

    @staticmethod
    def validate_ball(value):
        if value == 0:
            raise ValidationError('Ball 0ga teng bo\'lishi mumkin emas')
        return value

    def validate(self, attrs):
        # O'qituvchiga faqat admin ball bera olishi kerakligini tekshirish
        user = attrs.get('user')
        if user.user_type == User.UserTypeChoices.TEACHER:
            request_user = self.context.get('request').user
            if request_user.user_type != User.UserTypeChoices.ADMIN:
                raise ValidationError('Bu foydalanuvchiga siz ball bera olmaysiz')
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.get('user')
        validated_data['author'] = self.context.get('request').user
        score = super().create(validated_data)
        today = datetime.datetime.now()
        score_month = ScoreMonth.objects.filter(user=user,
                                                created_at__month=today.month,
                                                created_at__year=today.year).first()
        if bool(score_month):
            ball = validated_data.get('ball')
            score_month.ball += ball
            score_month.save()
        else:
            user = validated_data.get('user')
            ball = validated_data.get('ball')
            ScoreMonth.objects.create(user=user, ball=ball)
        return score


class ScoreListSerializer(serializers.ModelSerializer):
    ball = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = ['id', 'reason', 'ball', 'created_at']

    @staticmethod
    def get_ball(obj):
        if obj.ball > 0:
            return f'+{obj.ball}'
        return str(obj.ball)

    @staticmethod
    def get_created_at(obj: Score):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
