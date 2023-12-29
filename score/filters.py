from django_filters.rest_framework import filters, FilterSet

from score.models import Reason


class ReasonFilter(FilterSet):
    user_type = filters.CharFilter(method='user_type_filter')

    class Meta:
        model = Reason
        fields = ['user_type']

    @staticmethod
    def user_type_filter(queryset, name, value):
        user_types = ['admin', 'teacher', 'parent', 'pupil']

        if value not in user_types:
            return queryset

        user_type = user_types.index(value)
        return queryset.filter(user_type=user_type)
