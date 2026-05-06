from django.urls import path
from goodsapp import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category/<int:cid>/', views.IndexView.as_view()),
    path('category/<int:cid>/page/<int:num>/', views.IndexView.as_view()),
    path('goodsdetails/<int:goodsid>/', views.DetailView.as_view()),
]