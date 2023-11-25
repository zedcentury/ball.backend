from django.urls import path

from user.views import PupilsView, PupilCreateView, TeachersView, TeacherCreateView, ParentsView, ParentCreateView

urlpatterns = [
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('teacher/create/', TeacherCreateView.as_view(), name='teacher-create'),
    path('parents/', ParentsView.as_view(), name='parents'),
    path('parent/create/', ParentCreateView.as_view(), name='parent-create'),
    path('pupils/', PupilsView.as_view(), name='pupils'),
    path('pupil/create/', PupilCreateView.as_view(), name='pupil-create')
]
