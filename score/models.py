from django.db import models
from django.db.models import Q

from user.models import Pupil, User


class Reason(models.Model):
    """
    Turli xil holatlar uchun turli xil ballar
    user_type - holat o'qituvchi yoki o'quvchiga tegishli ekanligini bildiradi
    text - holat matni (kitob o'qidi, darsga sababsiz kelmadi)
    ball - holat yuzasidan beriladigan ballar (30, -10)
    """
    user_type = models.PositiveSmallIntegerField(choices=User.UserTypeChoices.choices)
    text = models.CharField(max_length=50)
    ball = models.IntegerField()

    class Meta:
        ordering = ['user_type']

    def __str__(self):
        if self.ball > 0:
            return f'{self.text} (+{self.ball})'
        return f'{self.text} ({self.ball})'


class Score(models.Model):
    """
    Har bir o'quvchiga berilgan ballar ro'yxati
    author - ball kim tomonidan qo'yilgani
    user - o'qituvchi yoki o'quvchi
    reason - holat (sabab)
    ball - berilgan ball (20, -12)
    created_at - ball berilgan vaqt
    """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='score_to_author',
                               limit_choices_to=
                               Q(user_type=User.UserTypeChoices.ADMIN) | Q(user_type=User.UserTypeChoices.TEACHER))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_to_user',
                             limit_choices_to=
                             Q(user_type=User.UserTypeChoices.TEACHER) | Q(user_type=User.UserTypeChoices.PUPIL))
    reason = models.CharField(max_length=100)
    ball = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.ball > 0:
            return f'{self.user.full_name} (+{self.ball})'
        return f'{self.user.full_name} ({self.ball})'


class ScoreMonth(models.Model):
    """
    O'quvchi yoki o'qituvchining oylik to'plagan balli
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_month_to_user', limit_choices_to={
        'user_type': User.UserTypeChoices.TEACHER or User.UserTypeChoices.PUPIL
    })
    ball = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
