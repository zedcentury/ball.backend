from django.urls import path, include

from score.views import ReasonListView, ReasonCreateView, ScoreCreateView, ReasonUpdateView, ReasonDestroyView, \
    ScoreListView, ScoreMonthView

urlpatterns = [
    path('reason/', include([
        path('list/', ReasonListView.as_view(), name='reason-list'),
        path('create/', ReasonCreateView.as_view(), name='reason-create'),
        path('update/<int:pk>/', ReasonUpdateView.as_view(), name='reason-update'),
        path('destroy/<int:pk>/', ReasonDestroyView.as_view(), name='reason-destroy'),
    ])),
    path('score/', include([
        path('create/', ScoreCreateView.as_view(), name='score-create'),
        path('list/', ScoreListView.as_view(), name='score-list'),
        path('month/<int:pk>/', ScoreMonthView.as_view(), name='score-month')
    ]))
]
