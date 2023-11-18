from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserTypeChoices(models.IntegerChoices):
        ADMIN = 0
        TEACHER = 1
        PARENT = 2
        PUPIL = 3

    userType = models.PositiveSmallIntegerField(choices=UserTypeChoices.choices, default=UserTypeChoices.ADMIN)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={
        'userType': User.UserTypeChoices.PUPIL
    })
    class_name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.full_name}, {self.class_name}'
