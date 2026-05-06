from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from djangoProject.settings import DEBUG, MEDIA_ROOT
from userapp import views
urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('center/',views.CenterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('loadCode/',views.LoadCodeView.as_view()),
    path('checkCode/',views.CheckCodeView.as_view()),
    path('logout/',views.Logout.as_view()),
    path('address/',views.AddressView.as_view()),
    path('loadAddr/',views.LoadAddr),
    path('setDefaultAddress/', views.SetDefaultAddressView.as_view()),
    path('deleteAddress/', views.DeleteAddressView.as_view()),

]



if DEBUG:
    urlpatterns.append(
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT})
    )