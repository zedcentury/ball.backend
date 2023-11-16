from django.urls import path

from user.views import PupilsView

urlpatterns = [
    path('pupils/', PupilsView.as_view(), name='pupils')
]
