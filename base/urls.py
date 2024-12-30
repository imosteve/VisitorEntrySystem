from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('registration-complete/', views.registration_complete, name="registration-complete"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]