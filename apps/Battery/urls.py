from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('list/', views.battery_list, name='battery_list'),
    path('delete-battery/<int:id>/', views.delete_battery, name="delete_battery"),
    path('download-discharge-data-zip/', views.download_discharge_data_zip, name='download_discharge_data_zip')
]
