from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from apps.Battery.models import Battery
from .models import BatteryProcessLog
from .utils import process_log_filter

@csrf_exempt
@require_POST
def get_next_process_id(request, identifier):
    battery = get_object_or_404(Battery, identifier=identifier)
    process_type = request.POST.get('process_type')

    if process_type not in ['charging', 'discharging']:
        return JsonResponse({'error': 'Invalid process_type. Use "charging" or "discharging".'}, status=400)

    last_process = BatteryProcessLog.objects.filter(battery=battery).order_by('-id').first()
    next_process_id = str(int(last_process.process_id) + 1) if last_process else '0'

    new_process = BatteryProcessLog.objects.create(
        battery=battery,
        process_id=next_process_id,
        process_type=process_type,
        start_time=timezone.now(),
        end_time=None
    )

    return JsonResponse({
        'next_process_id': next_process_id,
        'message': 'New process log created successfully',
        'start_time': new_process.start_time.isoformat(),
        'process_type': process_type
    })

@csrf_exempt
@require_POST
def update_end_time(request, identifier):
    battery = get_object_or_404(Battery, identifier=identifier)
    process_id = request.POST.get('process_id')

    if not process_id:
        return JsonResponse({'error': 'Missing process_id.'}, status=400)
    process_log = get_object_or_404(BatteryProcessLog, battery=battery, process_id=process_id)
    process_log.end_time = timezone.now()
    process_log.save()

    return JsonResponse({
        'message': 'End time updated successfully',
        'process_id': process_id,
        'end_time': process_log.end_time.isoformat()
    })

def battery_process_list(request):
    filters = process_log_filter(request)
    process_logs = BatteryProcessLog.objects.filter(**filters).order_by('-start_time')

    context = {
        'process_logs': process_logs,
    }
    return render(request, 'apps/battery_process.html', context)



def delete_battery_process(request, id):
    process_log = get_object_or_404(BatteryProcessLog, id=id)
    process_log.delete() 
    return redirect(request.META.get('HTTP_REFERER', '/'))