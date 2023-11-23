from django.urls import path

from common.views import ClassNamesView

urlpatterns = [
    path('class-names/', ClassNamesView.as_view(), name='class-names')
]
