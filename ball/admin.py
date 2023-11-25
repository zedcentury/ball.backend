from django.contrib import admin

from ball.models import Ball, Reason, BallStat

admin.site.register(Reason)
admin.site.register(Ball)
admin.site.register(BallStat)
