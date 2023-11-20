from django.db.models import signals
from django.dispatch import receiver

from ball.models import Ball, BallStat


@receiver(signals.post_save, sender=Ball)
def on_create_ball(sender, instance: Ball, created, **kwargs):
    user = instance.user
    score = instance.score
    if created:
        ball_stat: BallStat = BallStat.objects.filter(user=user, createdAt=instance.createdAt).first()
        if ball_stat:
            ball_stat.score += score
            ball_stat.save()
        else:
            BallStat.objects.create(user=user, score=score)
