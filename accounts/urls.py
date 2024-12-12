from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('phone_verify/', views.PhoneVerifyLoginView.as_view(), name='phone_verify'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('UserUserLoginWithPassword/', views.UserLoginWithPasswordView.as_view(), name='user_login_with_password'),

]
