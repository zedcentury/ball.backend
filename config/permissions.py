from rest_framework.permissions import BasePermission

from user.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.userType == User.UserTypeChoices.ADMIN


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.userType == User.UserTypeChoices.TEACHER


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.userType == User.UserTypeChoices.PARENT


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.userType == User.UserTypeChoices.STUDENT
