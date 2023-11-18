from django.db import models

from user.models import User


class Reason(models.Model):
    """
    Turli xil holatlar uchun turli xil ballar
    text - holat matni (kitob o'qidi, darsga sababsiz kelmadi)
    score - holat yuzasidan beriladigan ballar (30, -10)
    """
    text = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        if self.score > 0:
            return f'{self.text} (+{self.score})'
        else:
            return f'{self.text} ({self.score})'


class Ball(models.Model):
    """
    Har bir o'quvchiga berilgan ballar ro'yxati
    user - o'quvchi
    reason - holat (sabab)
    score - berilgan ball (20, -12)
    createdAt - ball berilgan vaqt
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ball_to_user', limit_choices_to={
        'userType': User.UserTypeChoices.PUPIL
    })
    reason = models.CharField(max_length=100, default=None, null=True, blank=True)
    score = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.score > 0:
            return f'{self.user.full_name} (+{self.score})'
        else:
            return f'{self.user.full_name} ({self.score})'
