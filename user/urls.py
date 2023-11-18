from django.urls import path

from user.views import PupilsView, LoginView, UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('pupils/', PupilsView.as_view(), name='pupils')
]
