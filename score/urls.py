from django.urls import path

from score.views import ReasonListView, ReasonCreateView, ScoreView, GoalsView, ScoreStatsView, ScoreCreateView

urlpatterns = [
    path('reason/list/', ReasonListView.as_view(), name='reason-list'),
    path('reason/create/', ReasonCreateView.as_view(), name='reason-create'),
    path('score/', ScoreView.as_view(), name='score'),
    path('goals/', GoalsView.as_view(), name='goals'),
    path('score/stats/', ScoreStatsView.as_view(), name='score-stats'),
    path('score/create/', ScoreCreateView.as_view(), name='score-create')
]
