from django.urls import path

from ball.views import BallView, ReasonsView, BallCreateView, BallStatsView, ReasonCreateView

urlpatterns = [
    path('reasons/', ReasonsView.as_view(), name='reasons'),
    path('reason/create/', ReasonCreateView.as_view(), name='reason-create'),
    path('ball/', BallView.as_view(), name='ball'),
    path('ball/stats/', BallStatsView.as_view(), name='ball-stats'),
    path('ball/create/', BallCreateView.as_view(), name='ball-create')
]
