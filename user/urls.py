from django.urls import path, include

from user.views import UserListView, UserCreateView, UserUpdateView, UserDestroyView, UserRetrieveView, \
    AttachPupilToParentView, AttachPupilToClassNameView, DetachPupilFromParentView, DetachPupilFromClassNameView

urlpatterns = [
    path('user/', include([
        path('list/', UserListView.as_view(), name='user-list'),
        path('create/', UserCreateView.as_view(), name='user-create'),
        path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
        path('destroy/<int:pk>/', UserDestroyView.as_view(), name='user-destroy'),
        path('retrieve/<int:pk>/', UserRetrieveView.as_view(), name='user-retrieve'),
    ])),
    path('attach/', include([
        path('pupil-to-parent/', AttachPupilToParentView.as_view(), name='attach-pupil-to-parent'),
        path('pupil-to-class-name/', AttachPupilToClassNameView.as_view(), name='attach-pupil-to-class-name'),
    ])),
    path('detach/', include([
        path('pupil-from-parent/<int:parent>/<int:pupil>/', DetachPupilFromParentView.as_view(),
             name='cancel-attach-class-name'),
        path('pupil-from-class-name/<int:pk>/', DetachPupilFromClassNameView.as_view(),
             name='cancel-attach-parent')
    ]))
]
