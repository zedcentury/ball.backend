from django.urls import path

from common.views import ClassNamesView, StatView

urlpatterns = [
    path('class-names/', ClassNamesView.as_view(), name='class-names'),
    path('stat/', StatView.as_view(), name='stat')
]
