import sys
sys.path.append('..')
import riderapp.models as models
from functools import cmp_to_key
import json
from datetime import datetime
from riderapp.controller import email_sender_controller

#compare [(time, username, tag)] by time in ascending order
def cmp(a, b):
    if a[0] > b[0]:
        return 1
    elif a[0] == b[0]:
        return 0
    return -1

def existField(field):
    if field != None and field != '':
        return True
    return False

#judge if user can modify the basic information of the target request
#including:
#   boarding, destination and arrival time
def check_can_modify_basic_info(target_request, user_id):
    user_id = int(user_id)
    # must open
    if target_request.status != 0:
        return "Request is not open currently"
    # must be owner
    if target_request.owner_id != user_id:
        return "Only owner can modify boarding, destination and arrival time"
    # must has no sharer
    if models.Shared.objects.filter(request_id=target_request.id):
        return "There are sharers in that request, cannot modify currently"
    return None

def request_detail(request, request_id):

    target_request = models.Request.objects.get(id=request_id)
    owner = models.User.objects.get(id=target_request.owner_id)
    history = [(target_request.request_time, owner.username,'opened')]
    sharer_ids = models.Shared.objects.filter(request_id=request_id)
    sharer_users = []
    isSharer = 0 #if user is sharer for this request
    userId = request.session.get('id')
    for sharer_id in sharer_ids:
        if sharer_id.user_id == userId:
            isSharer = 1
        sharer_user = models.User.objects.get(id=sharer_id.user_id)
        sharer_users.append(sharer_user)
        history.append((sharer_id.join_time, sharer_user.username, 'joined'))

    driver = None
    vehicle = None
    vehicleType = None
    if existField(target_request.driver_id):
        driver = models.User.objects.get(id=target_request.driver_id)
        vehicle = models.Vehicle.objects.get(user_id=driver.id)
        vehicleType = models.Vehicle_Type.objects.get(id=vehicle.vehicle_tid)
    
    if existField(target_request.comfirmed_time):
        history.append((target_request.comfirmed_time, driver.name, 'comfirmed'))
    if existField(target_request.complete_time):
        history.append((target_request.complete_time, driver.name, 'completed'))
    history.sort(key=cmp_to_key(cmp)) #order by time in ascending order
    modifyRight = hasModifyRight(request_id, request.session.get('id'))
    canModifyBasic_errmsg = check_can_modify_basic_info(target_request, userId)
    if canModifyBasic_errmsg != None:
        canModifyBasic = '0'
    else:
        canModifyBasic = '1'

    context = {
        'targetRequest': target_request,
        'owner': owner,
        'sharers': sharer_users,
        'share_ids': sharer_ids,
        'driver': driver,
        'vehicle':vehicle,
        'vehicleType':vehicleType,
        'history':history,
        'canmodify':modifyRight,
        'issharer': isSharer,
        'canModifyBasic': canModifyBasic
    }
    return context

# check whether user have the right to modify request basic info
def hasModifyRight(request_id, user_id):
    target_request = models.Request.objects.get(id=request_id)
    if target_request.status != 0:
        #not open
        return 0
    #only owner or sharer has the modification right
    if target_request.owner_id == int(user_id) or models.Shared.objects.filter(request_id=request_id, user_id=user_id):
        return 1
    return 0

def get_total_passenger_number(targetRequest):
    result = targetRequest.psnumbers
    for share in models.Shared.objects.filter(request_id=targetRequest.id):
        result += share.party_number
    return result

def vehicle_can_container(driver_id, target_request):
    vehicle = models.Vehicle.objects.get(user_id=driver_id)
    max_numbers = vehicle.max_numbers
    total_passenger_number = get_total_passenger_number(target_request)
    if max_numbers >= total_passenger_number:
        return True
    return False

# check whether user has the right to comfirm
def check_comfirm(target_request, user_id):
    user_id = int(user_id)
    # must still open
    if target_request.status != 0:
        return "Request is not open"
    user = models.User.objects.get(id=user_id)
    # user must be a driver
    if user.role != 1:
        return "You are not a driver currently, so cannot comfirm that request"
    vehicle = models.Vehicle.objects.get(user_id=user_id)
    # specific must match
    if target_request.specific != None and target_request.specific != vehicle.specific:
        return "That request has special information that you can not match"
    # vehicle type must match
    if target_request.vehicle_tid != None and target_request.vehicle_tid != vehicle.vehicle_tid:
        return "Your vehicle type dose not match the vehicle type of that request"
    # vehicle must contain all the passengers
    if not vehicle_can_container(user_id, target_request):
        return "Your vehicle could not contain all the passengers"
    return None


def comfirm_request(request):
    info = request.POST
    request_id = info.get('request_id', '')
    driver_id = request.session.get('id')
    response = {'status':'0'}
    if request_id != '' and driver_id != '':
        target_request = models.Request.objects.get(id=request_id)
        errmsg = check_comfirm(target_request, driver_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        target_request.driver_id = driver_id
        target_request.comfirmed_time = datetime.now()
        target_request.status = 1
        target_request.save()
        response['status'] = '1'
        email_sender_controller.send_comfirmed_mail(target_request)
    return json.dumps(response)

# check whether user can complete the request
def check_complete(target_request, user_id):
    user_id = int(user_id)
    # must in comfirmed status
    if target_request.status != 1:
        return "That request has been comfirmed"
    # user must be the driver of that request
    if target_request.driver_id != user_id:
        return "You are not the driver of that request"
    return None

def complete_request(request):
    info = request.POST
    request_id = info.get('request_id', '')
    driver_id = info.get('driver_id', '')
    response = {'status':'0'}
    if request_id != '' and driver_id != '':
        target_request = models.Request.objects.get(id=request_id)
        errmsg = check_complete(target_request, driver_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        target_request.status = 2
        target_request.complete_time = datetime.now()
        target_request.save()
        response['status'] = '1'
    return json.dumps(response)

# check if rider can cancel that request
def check_cancel(target_request, user_id):
    user_id = int(user_id)
    #only owner can cancel that request
    if target_request.owner_id != user_id:
        return "You are not the owner of that request"
    #status must be open
    if target_request.status != 0:
        return "That request is not open currently"
    return None

def cancel_request(request):
    response = {'status': '0'}
    info = request.POST
    request_id = info.get('request_id', '')
    owner_id = info.get('owner_id', '')
    if request_id != '' and owner_id != '':
        target_request = models.Request.objects.get(id=request_id)
        errmsg = check_cancel(target_request, owner_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        target_request.status = -1
        target_request.save()
        response['status'] = '1'
        email_sender_controller.send_owner_cancel_request(target_request)
    return json.dumps(response)

# check if sharer can join that request
def check_join(target_request, user_id):
    user_id = int(user_id)
    # status must be open
    if target_request.status != 0:
        return "Request is not open currently"
    # must can share
    if target_request.canshare != True:
        return "Request is not sharing currently"
    # user must not be owner of that request
    if target_request.owner_id == user_id:
        return "You are the owner of that request, cannot join again"
    # user must not be sharer of that request
    if models.Shared.objects.filter(request_id=target_request.id, user_id=user_id):
        return "You have joint that request, do not need to join again"
    return None

def join_request(request):
    response = {'status': '0'}
    info = request.POST
    request_id = info.get('request_id', '')
    sharer_id = info.get('sharer_id', '')
    party_number = info.get('party_number', '')
    if request_id != '' and sharer_id != '' and party_number != '':
        target_request = models.Request.objects.get(id=request_id)
        errmsg = check_join(target_request, sharer_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        share_insert = models.Shared(request_id=request_id, user_id=int(sharer_id),join_time=datetime.now(), party_number=int(party_number))
        share_insert.save()
        response['status'] = '1'

    return json.dumps(response)

# check if user_id can delete del_id from target request
def check_delete_rider(target_request, user_id, del_id):
    user_id = int(user_id)
    del_id = int(del_id)
    # status must be open
    if target_request.status != 0:
        return "Request is not open currently"
    # user must be the owner or del self
    if user_id != del_id and user_id != target_request.owner_id:
        return "You have no right to remove that rider out of that request"
    # user must be the sharer of that request
    if not models.Shared.objects.filter(request_id=target_request.id, user_id=del_id):
        return "That rider is not in that request currently"
    return None

def delete_rider_in_request(request):
    response = {'status': '0'}
    info = request.POST
    user_id = request.session.get('id')
    del_id = info.get('del_id', '')
    request_id = info.get('request_id', '')
    if request_id != '' and del_id != '' and user_id != '':
        target_request = models.Request.objects.get(id=request_id)
        errmsg = check_delete_rider(target_request, user_id, del_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        target_sharer = models.Shared.objects.get(request_id=int(request_id), user_id=int(del_id))
        target_sharer.delete()
        response['status'] = '1'
        email_sender_controller.send_dele_mail(target_request, del_id)
    return json.dumps(response)

# check if user can modify target request
def check_modify(target_request, user_id):
    user_id = int(user_id)
    # must be open
    if target_request.status != 0:
        return "Request is not open currently"
    #only owner or sharer has the modification right
    if target_request.owner_id != user_id and not models.Shared.objects.filter(request_id=target_request.id, user_id=user_id):
        return "You have no right to modify that request currently"
    return None
    
        
def modify_request(request):
    response = {'status': '0'}
    info = request.POST
    request_id = info.get('request_id', '')
    fieldName = info.get('fieldName', '')
    fieldVal = info.get('fieldVal', '')
    myId = info.get('myId', '')
    if request_id != '' and fieldName != '' and (fieldVal != '' or fieldName == 'specific') and myId != '':
        target_request = models.Request.objects.get(id=request_id)
        #basic information
        if fieldName == 'boarding' or fieldName == 'destination' or fieldName == 'arrival_time':
            errmsg = check_can_modify_basic_info(target_request, myId)
        else:
            errmsg = check_modify(target_request, myId)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        if fieldName == 'destination':
            email_sender_controller.send_modify_mail(target_request, 'Destination', fieldVal, myId)
            target_request.destination = fieldVal
        elif fieldName == 'boarding':
            email_sender_controller.send_modify_mail(target_request, 'Boarding', fieldVal, myId)
            target_request.boarding = fieldVal
        elif fieldName == 'arrival_time':
            email_sender_controller.send_modify_mail(target_request, 'Arrival Time', fieldVal, myId)
            target_request.arrival_time = fieldVal
        elif fieldName == 'psnumbers':
            target_request.psnumbers = fieldVal
        elif fieldName == 'specific':
            if fieldVal == '':
                fieldVal = None
            email_sender_controller.send_modify_mail(target_request, 'Special Requests', fieldVal, myId)
            target_request.specific = fieldVal
        elif fieldName == 'vehicle_tid':
            if fieldVal == '0':
                fieldVal = None
            if fieldVal != None:
                email_sender_controller.send_modify_mail(target_request, 'Vehicle Type', models.Vehicle_Type.objects.get(id=int(fieldVal)).type, myId)
            else:
                email_sender_controller.send_modify_mail(target_request, 'Vehicle Type', None, myId)
            target_request.vehicle_tid = fieldVal
        elif fieldName == 'canshare':
            if fieldVal == '0':
                email_sender_controller.send_modify_mail(target_request, 'Can share', 'no', myId)
                target_request.canshare = False
            elif fieldVal == '1':
                email_sender_controller.send_modify_mail(target_request, 'Can share', 'yes', myId)
                target_request.canshare = True
            else:
                return json.dumps(response)
        elif fieldName == 'party_number':
            if target_request.owner_id == int(myId):
                target_request.psnumbers = int(fieldVal)
            else:
                sharer = models.Shared.objects.get(user_id=int(myId), request_id=int(request_id))
                sharer.party_number = int(fieldVal)
                sharer.save()
        else:
            return json.dumps(response)
        target_request.save()
        response['status'] = '1'
    return json.dumps(response)

def driver_cancel_comfirmed(driver, request):
    if driver.id != request.driver_id:
        return False
    request.status = 0
    request.driver_id = None
    request.comfirmed_time = None
    request.save()
    email_sender_controller.send_cancel_mail(request)
    return True

# check if driver can stop cofirmed
def check_driver_stop_comfirmed(target_request, user_id):
    user_id = int(user_id)
    #status must be comfirmed
    if target_request.status != 1:
        return "Request is not comfirmed currently"
    # must be the driver of that request
    if target_request.driver_id != user_id:
        return "You are not the driver of that request"
    return None

def driver_stop_comfirmed(request):
    response = {'status': '0'}
    info = request.POST
    request_id = info.get('request_id', '')
    driver_id = request.session.get('id')
    if request_id != '' and driver_id != None:
        targetRequest = models.Request.objects.get(id=int(request_id))
        errmsg = check_driver_stop_comfirmed(targetRequest, driver_id)
        if errmsg != None:
            response['errmsg'] = errmsg
            return json.dumps(response)
        driver = models.User.objects.get(id=driver_id)
        ret = driver_cancel_comfirmed(driver, targetRequest)
        if ret == True:
            response['status'] = '1'
    return json.dumps(response)