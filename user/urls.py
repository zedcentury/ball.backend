from django.urls import path, include

from user.views import UserListView, UserCreateView, UserUpdateView, \
    UserDestroyView

urlpatterns = [
    path('user/', include([
        path('list/', UserListView.as_view(), name='user-list'),
        path('create/', UserCreateView.as_view(), name='user-create'),
        path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
        path('destroy/<int:pk>/', UserDestroyView.as_view(), name='user-destroy'),
    ])),
]
