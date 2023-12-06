from django.urls import path

from account.views import LoginView, UserView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('change/password/', ChangePasswordView.as_view(), name='change-password')
]
