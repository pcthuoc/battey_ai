from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.Battery.models import Battery
from apps.BatteryProcessLog.models import BatteryProcessLog
from apps.BatteryCycleData.models import BatteryCycleData


def battery_cycle_data_view(request):
    # Lấy danh sách tất cả các pin
    batteries = Battery.objects.all()

    # Lấy danh sách các quá trình xả (discharging) cho tất cả các pin
    discharge_logs = BatteryProcessLog.objects.filter(process_type='discharging').order_by('-start_time')

    # Biến lưu trữ dữ liệu log
    cycle_data = []

    # Lấy thông tin từ request (identifier và process_id)
    identifier = request.GET.get('identifier')
    process_id = request.GET.get('process_id')

    # Nếu có mã định danh pin (identifier) và process_id
    if identifier and process_id:
        selected_battery = get_object_or_404(Battery, identifier=identifier)
        selected_process = get_object_or_404(BatteryProcessLog, battery=selected_battery, process_id=process_id, process_type='discharging')

        # Lấy dữ liệu log từ BatteryCycleData
        cycle_data = BatteryCycleData.objects.filter(process=selected_process).order_by('timestamp')

    context = {
        'batteries': batteries,
        'discharge_logs': discharge_logs,
        'cycle_data': cycle_data,
    }

    return render(request, 'apps/battery_cycle_data.html', context)


def get_log_content(request, process_id):
    try:
        # Lấy log dựa trên process_id
        process_log = get_object_or_404(BatteryProcessLog, process_id=process_id)

        # Lấy tất cả các bản ghi BatteryCycleData liên quan
        cycle_data = BatteryCycleData.objects.filter(process=process_log).order_by('cycle_number')

        # Chuẩn bị dữ liệu để trả về JSON
        logs = [
            {
                'cycle_number': data.cycle_number,
                'voltage': data.voltage,
                'current': data.current,
                'temperature': data.temperature,
                'timestamp': data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for data in cycle_data
        ]

        return JsonResponse({'logs': logs})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)