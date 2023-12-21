from django.urls import path

from score.views import ReasonListView, ReasonCreateView, ScoreCreateView, ReasonUpdateView, ReasonDestroyView, \
    ScoreListView, ScoreMonthView

urlpatterns = [
    path('reason/list/', ReasonListView.as_view(), name='reason-list'),
    path('reason/create/', ReasonCreateView.as_view(), name='reason-create'),
    path('reason/update/<int:pk>/', ReasonUpdateView.as_view(), name='reason-update'),
    path('reason/destroy/<int:pk>/', ReasonDestroyView.as_view(), name='reason-destroy'),
    path('score/create/', ScoreCreateView.as_view(), name='score-create'),
    path('score/list/', ScoreListView.as_view(), name='score-list'),
    path('score/month/<int:pk>/', ScoreMonthView.as_view(), name='score-monthly')
]
