from django.urls import path
from app_users.views import UserRegisterView, UserLoginView, UserLogoutView, PersonalAreaView

urlpatterns = [
    path(
        'register/',
        UserRegisterView.as_view(),
        name='register',
    ),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout',
    ),
    path(
        'personal_area/<int:pk>/',
        PersonalAreaView.as_view(),
        name='personal_area',
    ),
]
