import sys
sys.path.append('..')
import riderapp.models as models
from riderapp.controller.request_detail_controller import driver_cancel_comfirmed
from django.core.exceptions import ObjectDoesNotExist
import json
import hashlib

def personal_info(request, user_id):
    user = models.User.objects.get(id=user_id)
    #hide user password
    user.password = '******'
    vehicle = None
    vehicleType = None
    if user.role == 1:
        vehicle = models.Vehicle.objects.get(user_id=user_id)  
        vehicleType = models.Vehicle_Type.objects.get(id=vehicle.vehicle_tid)      
    context = {
        'user': user,
        'vehicle': vehicle,
        'vehicleType': vehicleType
    }
    return context

def handle_personal_info_modification(request):
    response = {'status':'0'}
    info = request.POST
    fieldName = info.get('fieldName','')
    fieldVal = info.get('fieldVal','')
    userId = info.get('userId','')
    if fieldName != '' and userId != '' and (fieldName=='specific' or fieldVal != ''):
        result = personal_info_modify(userId, fieldName, fieldVal)
        if result == True:
            response['status'] = '1'

    return json.dumps(response)

# Modify user information by user_id
# @return success:True; fail:False
def personal_info_modify(user_id, fieldName, fieldVal):
    user = models.User.objects.get(id=user_id)
    # user basic information
    if fieldName == 'username':
        user.username = fieldVal
        user.save()
    elif fieldName == 'name':
        user.name = fieldVal
        user.save()
    elif fieldName == 'email':
        user.email = fieldVal
        user.save()
    elif fieldName == 'password':
        user.password = fieldVal
        user.save()
    else:
        # vehicle information
        # can not modify vehicle information when have uncompleted requests
        if models.Request.objects.filter(driver_id=user_id, status=1):
            return False
        try:
            vehicle = models.Vehicle.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return False
        if fieldName == 'vehicle_tid':
            vehicle.vehicle_tid = int(fieldVal)
            vehicle.save()
        elif fieldName == 'license_plate_number':
            vehicle.license_plate_number = fieldVal
            vehicle.save()
        elif fieldName == 'max_numbers':
            vehicle.max_numbers = int(fieldVal)
            vehicle.save()
        elif fieldName == 'specific':
            vehicle.specific = fieldVal
            vehicle.save()
        else:
            return False
    return True

# encrypt password by sha256
def encrypt_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def modify_password(request):
    response = {'status':'0'}
    info = request.POST
    userId = info.get('userId','')
    oldpwd = info.get('oldpwd','')
    newpwd = info.get('newpwd','')
    if userId != '' and oldpwd != '' and newpwd != '':
        user = models.User.objects.get(id=userId)
        if encrypt_password(oldpwd) != user.password:
            return json.dumps(response)
        user.password = encrypt_password(newpwd)
        user.save()
        response['status'] = '1'
    return json.dumps(response)

def register_driver(request):
    response = {'status':'0'}
    info = request.POST
    name = info.get('name', '')
    license_plate_number = info.get('license_plate_number', '')
    vehicle_tid = info.get('vehicle_tid', '')
    max_numbers = info.get('max_numbers', '')
    specific = info.get('specific', '')
    user_id = info.get('user_id', '')
    if name != '' and license_plate_number != '' and vehicle_tid != '' and max_numbers != '' and user_id != '':
        user = models.User.objects.get(id=int(user_id))
        if user.role != 0:
            return json.dumps(response)
        user.name = name
        user.role = 1
        if specific == '':
            specific = None
        vehicle = models.Vehicle(user_id=user.id, vehicle_tid=int(vehicle_tid), license_plate_number=license_plate_number, max_numbers=int(max_numbers),specific=specific)
        user.save()
        vehicle.save()
        response['status'] = '1'
    return json.dumps(response)

def stop_driver(request):
    response = {'status':'0'}
    driver_user_id = int(request.session.get('id'))
    driver = models.User.objects.get(id=driver_user_id)
    vehicle = models.Vehicle.objects.get(user_id=driver_user_id)

    #cancel all the comfirmation of this driver's unfinished request
    driver_requests = models.Request.objects.filter(driver_id=driver_user_id, status=1)
    for req in driver_requests:
        ret = driver_cancel_comfirmed(driver, req)
        if ret == False:
            return json.dumps(response)
    
    #delete driver information
    driver.role = 0
    vehicle.delete()
    driver.save()
    request.session['role'] = 0
    request.session['loginType'] = 'r'
    response = {'status':'1'}
    
    return json.dumps(response)