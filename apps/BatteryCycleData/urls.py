from django.urls import path
from . import views

urlpatterns = [
    path('data-view/', views.battery_cycle_data_view, name='battery_cycle_data_view'),
    path('get-log/<str:process_id>/', views.get_log_content, name='get_log_content'),
]


