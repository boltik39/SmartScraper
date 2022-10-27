from django.urls import path, re_path
from django.contrib import admin
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.LoginUser.as_view(), name="login"),
    path('about', views.about),
    path('search/', views.search, name="search"),
    path('scraper/', views.scraper, name="scraper"),
    path('admin/', admin.site.urls),
    path('excel/', views.export_devices_to_xlsx, name="export_devices_to_xlsx"),
    path('search/delete', views.delete, name="delete"),
]
