from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home),
    path('about', views.about),
    path('search/', views.search, name="search"),
    path('admin/', admin.site.urls),
    path('excel/',views.export_devices_to_xlsx, name="export_devices_to_xlsx")
]
