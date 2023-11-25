from rest_framework import serializers

from common.models import ClassName


class ClassNamesSerializer(serializers.ModelSerializer):
    pupils_count = serializers.IntegerField()

    class Meta:
        model = ClassName
        fields = ['id', 'name', 'pupils_count']


class ClassNameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = ['name']
