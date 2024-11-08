from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.battery_process_list, name='battery_process_list'),
    path('delete-battery-process/<int:id>/', views.delete_battery_process, name="delete_battery_process"),

    path('next-process-id/<uuid:identifier>/', views.get_next_process_id, name='get_next_process_id'),
    path('update-end-time/<uuid:identifier>/', views.update_end_time, name='update_end_time'),
]
