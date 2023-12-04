from django_filters.rest_framework import filters, FilterSet

from user.models import Pupil, Parent


class PupilFilter(FilterSet):
    parent = filters.NumberFilter(method='parent_filter')

    class Meta:
        model = Pupil
        fields = ['class_name_id', 'parent']

    @staticmethod
    def parent_filter(queryset, name, value):
        return queryset.filter(parent_to_pupil__user_id=value)
