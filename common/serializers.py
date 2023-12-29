from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.models import ClassName


class ClassNameListSerializer(serializers.ModelSerializer):
    pupils_count = serializers.IntegerField(default=0)

    class Meta:
        model = ClassName
        fields = ['id', 'name', 'pupils_count']


class ClassNameCreateSerializer(serializers.ModelSerializer):
    pupils_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = ClassName
        fields = ['id', 'name', 'pupils_count']


class ClassNameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = ['name']
