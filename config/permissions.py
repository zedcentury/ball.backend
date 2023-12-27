from rest_framework.permissions import IsAuthenticated

from user.models import User


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view)
        return permission and request.user.user_type == User.UserTypeChoices.ADMIN


class IsTeacher(IsAuthenticated):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view)
        return permission and request.user.user_type == User.UserTypeChoices.TEACHER


class IsParent(IsAuthenticated):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view)
        return permission and request.user.user_type == User.UserTypeChoices.PARENT


class IsPupil(IsAuthenticated):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view)
        return permission and request.user.user_type == User.UserTypeChoices.PUPIL
