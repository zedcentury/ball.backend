from rest_framework import serializers

from common.models import ClassName


class ClassNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = ['id', 'name']
