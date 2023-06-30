import sys
sys.path.append('..')
import riderapp.models as models
import json
import hashlib

# encrypt password by sha256
def encrypt_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# initialize vehicle type table
def initialize_vehicle_type_table():
    #it is the first time login
    if not models.Vehicle_Type.objects.filter(type="SUV"):
        vehicle_1 = models.Vehicle_Type(id=1, type="SUV")
        vehicle_1.save()
        vehicle_2 = models.Vehicle_Type(id=2, type="Hatchback")
        vehicle_2.save()
        vehicle_3 = models.Vehicle_Type(id=3, type="Crossover")
        vehicle_3.save()
        vehicle_4 = models.Vehicle_Type(id=4, type="Convertible")
        vehicle_4.save()
        vehicle_5 = models.Vehicle_Type(id=5, type="Sedan")
        vehicle_5.save()
        vehicle_6 = models.Vehicle_Type(id=6, type="Sports Car")
        vehicle_6.save()
        vehicle_7 = models.Vehicle_Type(id=7, type="Coupe")
        vehicle_7.save()
        vehicle_8 = models.Vehicle_Type(id=8, type="Minivan")
        vehicle_8.save()
        vehicle_9 = models.Vehicle_Type(id=9, type="Station Wagon")
        vehicle_9.save()
        vehicle_10 = models.Vehicle_Type(id=10, type="Pickup Truck")
        vehicle_10.save()

# set session for login user
def set_session(request, user, loginType):
    request.session['role'] = user.role
    request.session['username'] = user.username
    request.session['id'] = user.id
    if loginType == '0':
        loginType = 'r'
    else:
        loginType = 'd'
    request.session['loginType'] = loginType

def try_login(request):
    initialize_vehicle_type_table()
    response = {'status':'0'}
    info = request.POST
    username = info.get('username', '')
    password = info.get('password', '')
    loginType = info.get('loginType', '')
    if username == '' or password == '' or loginType == '':
        return json.dumps(response)
    user = models.User.objects.filter(username=username, password=encrypt_password(password))
    if user:
       response['status'] = '1'
       response['role'] = user.first().role
       if not (user.first().role == 0 and loginType == '1'):
          set_session(request, user.first(), loginType)     
       
    return json.dumps(response)

def register(request):
    response = {'status':'0'}
    info = request.POST
    role = info.get('role', '')
    if role != '0' and role != '1':
        return json.dumps(response)
    username = info.get('username', '')
    email = info.get('email', '')
    password = info.get('password', '')
    if username == '' or email == '' or password == '':
        return json.dumps(response)
    #username already exist
    if models.User.objects.filter(username=username):
        response['username'] = '1'
        return json.dumps(response)
    if role == '0':
        #rider
        newUser = models.User(username=username, password=encrypt_password(password), role=0, email=email)
        newUser.save()
    else:
        #driver
        #driver info
        name = info.get('name', '')
        license_plate_number = info.get('license_plate_number', '')
        max_numbers = info.get('max_numbers', '')
        specific = info.get('specific', '')
        vehicle_tid = info.get('vehicle_tid', '')
        if name == '' or license_plate_number == '' or max_numbers == '' or vehicle_tid == '':
            return json.dumps(response)
        #insert user table
        newUser = models.User(username=username, password=encrypt_password(password),name=name,role=1,email=email)
        newUser.save()
        user_id = newUser.id
        #insert vehicle table
        vehicle = models.Vehicle(user_id=user_id, vehicle_tid=int(vehicle_tid), license_plate_number=license_plate_number, max_numbers=int(max_numbers),specific=specific)
        vehicle.save()
    response['status'] = '1'
    return json.dumps(response)

def log_out(request):
    request.session.flush()
    response = {'status':'1'}
    return json.dumps(response)