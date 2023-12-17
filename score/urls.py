from django.urls import path

from score.views import ReasonListView, ReasonCreateView, ScoreTodayView, ScoreStatView, ScoreDailyListView, \
    ScoreCreateView, ReasonUpdateView, ReasonDestroyView, ScoreListView

urlpatterns = [
    path('reason/list/', ReasonListView.as_view(), name='reason-list'),
    path('reason/create/', ReasonCreateView.as_view(), name='reason-create'),
    path('reason/update/<int:pk>/', ReasonUpdateView.as_view(), name='reason-update'),
    path('reason/destroy/<int:pk>/', ReasonDestroyView.as_view(), name='reason-destroy'),
    path('score/today/<int:pk>/', ScoreTodayView.as_view(), name='score'),
    path('score/stat/<int:pk>/', ScoreStatView.as_view(), name='score-stat'),
    path('score/daily/list/<int:pk>/', ScoreDailyListView.as_view(), name='score-stats'),
    path('score/create/', ScoreCreateView.as_view(), name='score-create'),
    path('score/list/', ScoreListView.as_view(), name='score-list')
]
