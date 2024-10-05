import datetime

from django.db.models import Q
from django_filters.rest_framework import filters, FilterSet

from user.models import User


class UserFilter(FilterSet):
    user_type = filters.CharFilter(method='user_type_filter')
    parent = filters.NumberFilter(method='parent_filter')
    no_attach_parent = filters.NumberFilter(method='no_attach_parent_filter')
    class_name = filters.NumberFilter(method='class_name_filter')
    no_attach_class_name = filters.NumberFilter(method='no_attach_class_name_filter')
    ball_type = filters.NumberFilter(method='ball_type_filter')

    class Meta:
        model = User
        fields = ['user_type', 'parent', 'no_attach_parent', 'class_name', 'no_attach_class_name', 'ball_type']

    @staticmethod
    def ball_type_filter(queryset, name, value):
        today = datetime.date.today()

        if value == 0:
            return queryset.filter(score_month_to_user__ball__gt=100 - 100,
                                   score_month_to_user__created_at__month=today.month,
                                   score_month_to_user__created_at__year=today.year)

        if value == 1:
            return queryset.filter(Q(score_month_to_user__ball__gte=72 - 100,
                                     score_month_to_user__ball__lte=100 - 100,
                                     score_month_to_user__created_at__month=today.month,
                                     score_month_to_user__created_at__year=today.year) |
                                   Q(score_month_to_user__isnull=True))

        if value == 2:
            return queryset.filter(score_month_to_user__ball__gte=55 - 100,
                                   score_month_to_user__ball__lt=72 - 100,
                                   score_month_to_user__created_at__month=today.month,
                                   score_month_to_user__created_at__year=today.year)

        if value == 3:
            return queryset.filter(score_month_to_user__ball__lt=55 - 100,
                                   score_month_to_user__created_at__month=today.month,
                                   score_month_to_user__created_at__year=today.year)

        return queryset

    @staticmethod
    def user_type_filter(queryset, name, value):
        user_types = ['admin', 'teacher', 'parent', 'pupil']

        if value not in user_types:
            return queryset

        user_type = user_types.index(value)
        return queryset.filter(user_type=user_type)

    @staticmethod
    def parent_filter(queryset, name, value):
        """
        Pupils of parent
        """
        return queryset.filter(pupil_to_user__parent_to_pupil__user_id=value)

    @staticmethod
    def no_attach_parent_filter(queryset, name, value):
        """
        Joriy foydalanuvchi ota-onasi bo'lgan foydalanuvchilar olib tashlanadi
        Ya'ni biror ota-ona uchun unga bog'lanmagan foydalanuvchilar ro'yxati chiqariladi
        """
        return queryset.exclude(pupil_to_user__parent_to_pupil__user_id=value)

    @staticmethod
    def class_name_filter(queryset, name, value):
        """
        Joriy sinfga biriktirilgan o'quvchilar ro'yxati
        """
        return queryset.filter(pupil_to_user__class_name_id=value)

    @staticmethod
    def no_attach_class_name_filter(queryset, name, value):
        """
        Birorta ham sinfga biriktirilmagan o'quvchilar ro'yxati
        """
        return queryset.filter(pupil_to_user__class_name__isnull=True)
