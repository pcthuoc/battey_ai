def battery_filter(request):
    filters = {}

    if 'name' in request.GET and request.GET['name']:
        filters['name__icontains'] = request.GET['name']
    if 'nominal_capacity' in request.GET and request.GET['nominal_capacity']:
        try:
            filters['nominal_capacity'] = float(request.GET['nominal_capacity'])
        except ValueError:
            pass 
    if 'voltage_min' in request.GET and request.GET['voltage_min']:
        try:
            filters['voltage_min__gte'] = float(request.GET['voltage_min'])
        except ValueError:
            pass

    if 'voltage_max' in request.GET and request.GET['voltage_max']:
        try:
            filters['voltage_max__lte'] = float(request.GET['voltage_max'])
        except ValueError:
            pass

    return filters