from django.db import models

from user.models import Pupil


class Reason(models.Model):
    """
    Turli xil holatlar uchun turli xil ballar
    text - holat matni (kitob o'qidi, darsga sababsiz kelmadi)
    ball - holat yuzasidan beriladigan ballar (30, -10)
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
    pupil - o'quvchi
    reason - holat (sabab)
    ball - berilgan ball (20, -12)
    created_at - ball berilgan vaqt
    """
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='ball_to_pupil')
    reason = models.CharField(max_length=100, default=None, null=True, blank=True)
    ball = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.ball > 0:
            return f'{self.pupil.user.full_name} (+{self.ball})'
        return f'{self.pupil.user.full_name} ({self.ball})'


class ScoreDaily(models.Model):
    """
    Har bir foydalanuvchining har kungi umumiy ballari
    pupil - o'quvchi
    ball - joriy kunda to'plagan umumiy balli
    """
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='score_daily_to_pupil')
    ball = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['pupil', 'created_at']

    def __str__(self):
        return f'{self.pupil.user.full_name} ({self.ball}, {self.created_at})'


class ScoreStat(models.Model):
    """
    Har bir foydalanuvchining to'plagan ballari bo'yicha statistika
    excellent (81-100 ball)
    good (61-80 ball)
    bad (0-60)
    """
    pupil = models.OneToOneField(Pupil, on_delete=models.CASCADE, related_name='score_stat_to_pupil')
    excellent = models.PositiveIntegerField(default=0)
    good = models.PositiveIntegerField(default=0)
    bad = models.PositiveIntegerField(default=0)
    updated_at = models.DateField(auto_now=True)
