from django.urls import path, include

from common.views import ClassNameListView, StatView, ClassNameCreateView, ClassNameUpdateView, ClassNameDestroyView

urlpatterns = [
    path('class-name/', include([
        path('list/', ClassNameListView.as_view(), name='class-name-list'),
        path('create/', ClassNameCreateView.as_view(), name='class-name-create'),
        path('update/<int:pk>/', ClassNameUpdateView.as_view(), name='class-name-update'),
        path('destroy/<int:pk>/', ClassNameDestroyView.as_view(), name='class-name-destroy'),
    ])),
    path('stat/', StatView.as_view(), name='stat')
]
