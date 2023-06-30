from django.shortcuts import render, HttpResponse
from riderapp.controller import driver_index_controller, search_result_controller, request_detail_controller, personal_info_controller, request_history_controller
from riderapp.controller import register_controller, rider_index_controller

def driver_login_guard(func):
    def guard(*args, **kwargs):
        request = args[0]
        if request.session.get('id') == None or request.session.get('role') != 1 or request.session.get('loginType') != 'd':
            return render(request, 'riderapp/login.html')
        else:
            return func(*args, **kwargs)
    return guard

def rider_login_guard(func):
    def guard(*args, **kwargs):
        request = args[0]
        if request.session.get('id') == None or request.session.get('loginType') != 'r':
            return render(request, 'riderapp/login.html')
        else:
            return func(*args, **kwargs)
    return guard

def common_login_guard(func):
    def guard(*args, **kwargs):
        request = args[0]
        if request.session.get('id') == None:
            return render(request, 'riderapp/login.html')
        else:
            return func(*args, **kwargs)
    return guard

# Display driver_index.html for users
@driver_login_guard
def driver_index(request):
    driver_login_guard(request)
    context = driver_index_controller.driver_index(request)
    return render(request, 'riderapp/driver_index.html', context)

# Display search result page for users
@common_login_guard
def search_result(request):
    context = search_result_controller.search_result(request)
    return render(request, 'riderapp/search_result.html', context)

# Display request detail page for users
# @param request_id id of request in database
@common_login_guard
def request_detail(request, request_id):
    context = request_detail_controller.request_detail(request, request_id)
    return render(request, 'riderapp/request_detail.html', context)

# Driver comfirm open request
@driver_login_guard
def comfirm_request(request):
    response = request_detail_controller.comfirm_request(request)
    return HttpResponse(response)

# Driver complete request
@driver_login_guard
def complete_request(request):
    response = request_detail_controller.complete_request(request)
    return HttpResponse(response)

# Owner cancel request
@rider_login_guard
def cancel_request(request):
    response = request_detail_controller.cancel_request(request)
    return HttpResponse(response)

# Driver stop comfirming
@driver_login_guard
def driver_stop_comfirmed(request):
    response = request_detail_controller.driver_stop_comfirmed(request)
    return HttpResponse(response)

# Sharer join request
@rider_login_guard
def join_request(request):
    response = request_detail_controller.join_request(request)
    return HttpResponse(response)

# Modify request basic info
@rider_login_guard
def modify_request(request):
    response = request_detail_controller.modify_request(request)
    return HttpResponse(response)

# Delete user from request
@rider_login_guard
def delete_rider_in_request(request):
    response = request_detail_controller.delete_rider_in_request(request)
    return HttpResponse(response)

# Display personal info page for users
@common_login_guard
def personal_info(request, user_id):
    if int(user_id) != request.session.get('id'):
        return render(request, 'riderapp/login.html')
    context = personal_info_controller.personal_info(request, user_id)
    return render(request, 'riderapp/personal_info.html', context)

# Modify personal info except password
@common_login_guard
def modify_personal_info(request):
    response = personal_info_controller.handle_personal_info_modification(request)
    return HttpResponse(response)

# Modify password
@common_login_guard
def modify_password(request):
    response = personal_info_controller.modify_password(request)
    return HttpResponse(response)

# Register to be a driver in personal info page
@common_login_guard
def personal_register_driver(request):
    response = personal_info_controller.register_driver(request)
    return HttpResponse(response)

# Display request history for users
@common_login_guard
def request_history(request, user_id, histype):
    context = request_history_controller.request_history(request, user_id, histype)
    return render(request, 'riderapp/request_history.html', context)

# Stop being a driver
@common_login_guard
def stop_driver(request):
    response = personal_info_controller.stop_driver(request)
    return HttpResponse(response)

# Login page for users
def login(request):
    return render(request, 'riderapp/login.html')

@common_login_guard
def log_out(request):
    response = register_controller.log_out(request)
    return HttpResponse(response)

# Receive register information and register
def register(request):
    response = register_controller.register(request)
    return HttpResponse(response)

# Receive login information and try login
def try_login(request):
    response = register_controller.try_login(request)
    return HttpResponse(response)

# Display rider index for users
@rider_login_guard
def rider_index(request):
    context = rider_index_controller.rider_index(request)
    return render(request, 'riderapp/rider_index.html', context)

# Create new request
@rider_login_guard
def create_new_request(request):
    response = rider_index_controller.create_new_request(request)
    return HttpResponse(response)