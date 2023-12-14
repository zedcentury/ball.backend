from rest_framework.permissions import BasePermission

from user.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user) and
                request.user.is_authenticated and
                request.user.user_type == User.UserTypeChoices.ADMIN)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user) and request.user.is_authenticated and
                request.user.user_type == User.UserTypeChoices.TEACHER)


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user) and request.user.is_authenticated and
                request.user.user_type == User.UserTypeChoices.PARENT)


class IsPupil(BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user) and request.user.is_authenticated and
                request.user.user_type == User.UserTypeChoices.PUPIL)
