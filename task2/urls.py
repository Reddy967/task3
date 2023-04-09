
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.login_attempt, name="login"),
    path('register/', views.register, name="register"),
    path('otp/', views.otp, name="otp"),
    path('login_otp/', views.login_otp, name="login_otp"),
    path('dashboard/', views.dashboard)

]