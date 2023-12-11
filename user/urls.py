from django.urls import path, include

from user.views import UserListView, UserCreateView, UserUpdateView, \
    UserDestroyView, AttachParentToPupilView, AttachClassNameToPupilView, CancelAttachClassNameView, \
    CancelAttachParentView, ChildrenView, UserRetrieveView

urlpatterns = [
    path('user/', include([
        path('list/', UserListView.as_view(), name='user-list'),
        path('create/', UserCreateView.as_view(), name='user-create'),
        path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
        path('destroy/<int:pk>/', UserDestroyView.as_view(), name='user-destroy'),
        path('retrieve/<int:pk>/', UserRetrieveView.as_view(), name='user-retrieve'),
    ])),
    path('children/', ChildrenView.as_view(), name='children'),
    path('attach/parent-to-pupil/', AttachParentToPupilView.as_view(), name='attach-parent-to-pupil'),
    path('attach/class-name-to-pupil/', AttachClassNameToPupilView.as_view(), name='attach-class-name-to-pupil'),
    path('cancel-attach/class-name/<int:pk>/', CancelAttachClassNameView.as_view(), name='cancel-attach-class-name'),
    path('cancel-attach/parent/<int:parent>/<int:pupil>/', CancelAttachParentView.as_view(),
         name='cancel-attach-parent')
]
