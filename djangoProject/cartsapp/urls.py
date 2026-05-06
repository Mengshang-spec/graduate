from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from cartsapp import views
from djangoProject.settings import DEBUG, MEDIA_ROOT

urlpatterns = [
    path('', views.CartView.as_view()),
    path('queryAll/', views.queryAll),
]