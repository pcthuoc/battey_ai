def process_log_filter(request):
    filters = {}
    
    # Lọc theo mã định danh pin (identifier)
    identifier = request.GET.get('identifier')
    if identifier:
        filters['battery__identifier'] = identifier

    # Lọc theo loại quá trình (charging hoặc discharging)
    process_type = request.GET.get('process_type')
    if process_type in ['charging', 'discharging']:
        filters['process_type'] = process_type

    # Lọc theo thời gian bắt đầu
    start_time_min = request.GET.get('start_time_min')
    start_time_max = request.GET.get('start_time_max')
    if start_time_min:
        filters['start_time__gte'] = start_time_min
    if start_time_max:
        filters['start_time__lte'] = start_time_max

    # Lọc theo thời gian kết thúc
    end_time_min = request.GET.get('end_time_min')
    end_time_max = request.GET.get('end_time_max')
    if end_time_min:
        filters['end_time__gte'] = end_time_min
    if end_time_max:
        filters['end_time__lte'] = end_time_max

    return filters
