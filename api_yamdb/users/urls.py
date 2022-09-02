from django.urls import path

from .views import AdmCreateUser, ConfirmRegisteredView, SignupView

app_name = 'users'


urlpatterns = [
    path('users/<slug:username>/', AdmCreateUser.as_view(), name='user'),
    path('users/', AdmCreateUser.as_view()),
    path('auth/token/', ConfirmRegisteredView.as_view()),
    path('auth/signup/', SignupView.as_view())
]
