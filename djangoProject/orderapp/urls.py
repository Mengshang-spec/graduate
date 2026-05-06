from django.urls import path, include
from orderapp import views
urlpatterns = [
    path('', views.order_View),
    path('toOrder/', views.toOrder),
]