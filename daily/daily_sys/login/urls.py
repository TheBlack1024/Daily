from django.urls import path,re_path

from . import views

app_name = 'login'
urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),

]