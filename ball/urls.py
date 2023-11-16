from django.urls import path

from ball.views import BallView, ReasonsView, BallCreateView

urlpatterns = [
    path('reasons/', ReasonsView.as_view(), name='reasons'),
    path('ball/', BallView.as_view(), name='ball'),
    path('ball/create/', BallCreateView.as_view(), name='ball-create')
]
