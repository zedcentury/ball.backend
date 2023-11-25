from django.urls import path

from common.views import ClassNamesView, StatView, ClassNameCreateView

urlpatterns = [
    path('class-names/', ClassNamesView.as_view(), name='class-names'),
    path('class-name/create/', ClassNameCreateView.as_view(), name='class-name-create'),
    path('stat/', StatView.as_view(), name='stat')
]
