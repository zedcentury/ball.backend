from django_filters.rest_framework import filters, FilterSet

from user.models import Pupil, Parent, User


class UserFilter(FilterSet):
    user_type = filters.CharFilter(method='user_type_filter')
    parent = filters.NumberFilter(method='parent_filter')
    no_attach_parent = filters.NumberFilter(method='no_attach_parent_filter')
    class_name = filters.NumberFilter(method='class_name_filter')
    no_attach_class_name = filters.NumberFilter(method='no_attach_class_name_filter')

    class Meta:
        model = User
        fields = ['user_type', 'parent', 'no_attach_parent', 'class_name', 'no_attach_class_name']

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
