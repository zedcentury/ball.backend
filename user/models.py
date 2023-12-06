from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import ClassName


class User(AbstractUser):
    class UserTypeChoices(models.IntegerChoices):
        ADMIN = 0
        TEACHER = 1
        PARENT = 2
        PUPIL = 3

    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    userType = models.PositiveSmallIntegerField(choices=UserTypeChoices.choices, default=UserTypeChoices.ADMIN)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pupil_to_user', limit_choices_to={
        'userType': User.UserTypeChoices.PUPIL
    })
    class_name = models.ForeignKey(ClassName, on_delete=models.RESTRICT, related_name='pupil_to_class_name')

    def __str__(self):
        return f'{self.user.full_name}, {self.class_name}'


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_to_user', limit_choices_to={
        'userType': User.UserTypeChoices.PARENT
    })
    children = models.ManyToManyField(Pupil, related_name='parent_to_pupil')

    def __str__(self):
        return self.user.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_to_user', limit_choices_to={
        'userType': User.UserTypeChoices.TEACHER
    })
    pupils = models.ManyToManyField(Pupil)

    def __str__(self):
        return self.user.full_name
