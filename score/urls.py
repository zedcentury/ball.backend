from django.urls import path

from score.views import ReasonListView, ReasonCreateView, ScoreTodayView, ScoreStatView, ScoreDailyListView, \
    ScoreCreateView, ReasonUpdateView, ReasonDestroyView

urlpatterns = [
    path('reason/list/', ReasonListView.as_view(), name='reason-list'),
    path('reason/create/', ReasonCreateView.as_view(), name='reason-create'),
    path('reason/update/<int:pk>/', ReasonUpdateView.as_view(), name='reason-update'),
    path('reason/destroy/<int:pk>/', ReasonDestroyView.as_view(), name='reason-destroy'),
    path('score/today/<int:user_id>/', ScoreTodayView.as_view(), name='score'),
    path('score/stat/<int:user_id>/', ScoreStatView.as_view(), name='score-stat'),
    path('score/daily/list/<int:user_id>/', ScoreDailyListView.as_view(), name='score-stats'),
    path('score/create/', ScoreCreateView.as_view(), name='score-create')
]
