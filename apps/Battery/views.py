import io
from django.http import JsonResponse, HttpResponse
from zipfile import ZipFile
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from io import StringIO, BytesIO
import csv
import zipfile

from .models import Battery
from .forms import BatteryForm
from .utils import battery_filter

from apps.Battery.models import Battery
from apps.BatteryProcessLog.models import BatteryProcessLog
from apps.BatteryCycleData.models import BatteryCycleData

def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))


def battery_list(request):
    filters = battery_filter(request)
    batterys = Battery.objects.filter(**filters)
    form = BatteryForm()
    if request.method == 'POST':
        form = BatteryForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)
    context = {
        'batterys': batterys,
        'form': form,
    }
    return render(request, 'apps/batterys.html', context)

def delete_battery(request, id):
    battery = Battery.objects.get(id=id)
    battery.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def delete_battery(request, id):
 
    battery = get_object_or_404(Battery, id=id)
    BatteryCycleData.objects.filter(battery=battery).delete()
    BatteryProcessLog.objects.filter(battery=battery).delete()
    battery.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))



def download_discharge_data_zip(request):
    try:
        battery_ids = request.GET.get('battery_ids', '')
        if not battery_ids:
            return JsonResponse({'error': 'Không có pin nào được chọn.'}, status=400)

        battery_ids = battery_ids.split(',')
        batteries = Battery.objects.filter(id__in=battery_ids)

        if not batteries.exists():
            return JsonResponse({'error': 'Không tìm thấy pin đã chọn.'}, status=404)

        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for battery in batteries:
                process_logs = BatteryProcessLog.objects.filter(battery=battery, process_type='discharging', end_time__isnull=False)
                if not process_logs.exists():
                    continue

                for log in process_logs:
                    filename = f"{battery.name}/discharge_session_{log.process_id}.csv"
                    data = BatteryCycleData.objects.filter(process=log).order_by('cycle_number')
                    csv_content = "cycle_number,voltage,current,temperature,timestamp\n"
                    csv_content += "\n".join([
                        f"{d.cycle_number},{d.voltage},{d.current},{d.temperature},{d.timestamp}"
                        for d in data
                    ])
                    zip_file.writestr(filename, csv_content)

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="discharge_data.zip"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)