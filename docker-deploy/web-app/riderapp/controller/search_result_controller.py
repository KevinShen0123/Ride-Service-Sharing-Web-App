import sys
sys.path.append('..')
import riderapp.models as models

# search requests by provided options. [POST ONLY]
# ASSUME data formats are all valid
# Accept name fields: 
#   boarding
#   destination
#   startTime
#   endTime
#   psnumbers
#   canshare: if 'canshare' in data: True; else: False
def search_result(request):
    loginType = request.session.get('loginType')
    if loginType == 'r':
        return rider_search(request)
    elif loginType == 'd':
        return driver_search(request)
    else:
        return None

def exclude_request_with_inshare(requests, user_id):
    filtered = []
    for req in requests:
        if not models.Shared.objects.filter(request_id=req.id, user_id=user_id):
            filtered.append(req)
    return filtered

def exclude_request_with_passenger_numbers(requests, driver_id):
    filtered = []
    for req in requests:
        if vehicle_can_contain(driver_id, req):
            filtered.append(req)
    return filtered

def get_total_passenger_number(targetRequest):
    result = targetRequest.psnumbers
    for share in models.Shared.objects.filter(request_id=targetRequest.id):
        result += share.party_number
    return result

def vehicle_can_contain(driver_id, target_request):
    vehicle = models.Vehicle.objects.get(user_id=driver_id)
    max_numbers = vehicle.max_numbers
    total_passenger_number = get_total_passenger_number(target_request)
    if max_numbers >= total_passenger_number:
        return True
    return False

def exclude_request_with_specific_passenger_number(requests, target_number):
    filtered = []
    for req in requests:
        passnumber = get_total_passenger_number(req)
        if passnumber <= target_number:
            filtered.append(req)
    return filtered

def driver_search(request):
    search_info = request.POST
    boarding = search_info.get('boarding', '')
    destination = search_info.get('destination', '')
    print(boarding)
    print(destination)
    startTime = search_info.get('startTime', '')
    endTime = search_info.get('endTime', '')
    psnumbers = search_info.get('psnumbers', '')
    canshare = search_info.get('canshare', False)
    user_id = request.session.get('id')
    vehicle = models.Vehicle.objects.get(user_id=user_id)
    if canshare != False:
        canshare = True

    result = models.Request.objects.filter(canshare=canshare, status=0).exclude(owner_id=user_id)
    # filter by vehicle type
    result = result.filter(vehicle_tid=vehicle.vehicle_tid) | result.filter(vehicle_tid=None)
    # filter by specific
    result = result.filter(specific=vehicle.specific) | result.filter(specific=None)
    # filter by passenger number
    result = result.filter(psnumbers__lte=vehicle.max_numbers)
    if boarding != '':
        result = result.filter(boarding=boarding)
    if destination != '':
        result = result.filter(destination=destination)
    if startTime != '':
        result = result.filter(arrival_time__gte=startTime)
    if endTime != '':
        result = result.filter(arrival_time__lte=endTime)
    if psnumbers != '':
        result = exclude_request_with_specific_passenger_number(result, int(psnumbers))
    result = exclude_request_with_inshare(result, user_id)
    result = exclude_request_with_passenger_numbers(result, user_id)
    context = {
        'searchResult':result
    }
    return context

def rider_search(request):
    id = request.session.get('id')
    search_info = request.POST
    boarding = search_info.get('boarding', '')
    destination = search_info.get('destination', '')
    startTime = search_info.get('startTime', '')
    endTime = search_info.get('endTime', '')
    psnumbers = search_info.get('psnumbers', '')

    result = models.Request.objects.filter(canshare=True, status=0).exclude(owner_id=id)

    if boarding != '':
        result = result.filter(boarding=boarding)
    if destination != '':
        result = result.filter(destination=destination)
    if startTime != '':
        result = result.filter(arrival_time__gte=startTime)
    if endTime != '':
        result = result.filter(arrival_time__lte=endTime)
    result = exclude_request_with_inshare(result, id)
    if psnumbers != '':
        #total number must <= psnumbers
        result = exclude_request_with_specific_passenger_number(result, int(psnumbers))
    context = {
        'searchResult':result
    }
    return context