from django.urls import path,re_path

from . import views
from daily.views import IndexView,AuthorView,SearchView,CompanyView

app_name = 'daily'
urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
    path('<int:daily_id>/',views.detail,name='detail'),
    path('author/<int:owner_id>/',AuthorView.as_view(),name='author'),
    path('search/',SearchView.as_view(),name='search'),
    path('company/<int:company_id>/', CompanyView.as_view(), name='company'),
    path('results/',views.results,name='results'),
]