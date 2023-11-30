from django.db import models

from user.models import Pupil


class Reason(models.Model):
    """
    Turli xil holatlar uchun turli xil ballar
    text - holat matni (kitob o'qidi, darsga sababsiz kelmadi)
    score - holat yuzasidan beriladigan ballar (30, -10)
    """
    text = models.CharField(max_length=50, unique=True)
    ball = models.IntegerField()

    def __str__(self):
        if self.ball > 0:
            return f'{self.text} (+{self.ball})'
        return f'{self.text} ({self.ball})'


class Score(models.Model):
    """
    Har bir o'quvchiga berilgan ballar ro'yxati
    user - o'quvchi
    reason - holat (sabab)
    score - berilgan ball (20, -12)
    created_at - ball berilgan vaqt
    """
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='ball_to_pupil')
    reason = models.CharField(max_length=100, default=None, null=True, blank=True)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.score > 0:
            return f'{self.pupil.user.full_name} (+{self.score})'
        return f'{self.pupil.user.full_name} ({self.score})'


class ScoreStat(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='score_stat_to_pupil')
    ball = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.pupil.user.full_name} ({self.ball}, {self.created_at})'
