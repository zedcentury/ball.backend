from rest_framework.permissions import BasePermission

from user.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypeChoices.ADMIN


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypeChoices.TEACHER


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypeChoices.PARENT


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypeChoices.STUDENT
