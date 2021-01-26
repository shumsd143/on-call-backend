from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.LoginView.as_view(),name="login-api"),
    path('register/',views.RegisterView.as_view(),name="register-api"),
    path('info/',views.UserView.as_view(),name="user-info-api")
]