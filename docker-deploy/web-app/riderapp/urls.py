from django.urls import path

from . import views

urlpatterns = [
    # urls for driver/index
    path('driver/index', views.driver_index, name="driver_index"),

    # urls for rider/index
    path('rider/index', views.rider_index, name="rider_index"),
    path('rider/new_request', views.create_new_request, name="new_request"),

    # urls for search
    path('search', views.search_result, name="search_result"),

    # urls for reqdetail
    path('reqdetail/<int:request_id>', views.request_detail, name="request_detail"),
    path('reqdetail/comfirm', views.comfirm_request, name='comfirm_request'),
    path('reqdetail/complete', views.complete_request, name='complete_request'),
    path('reqdetail/cancel', views.cancel_request, name='cancel_request'),
    path('reqdetail/join', views.join_request, name='join_request'),
    path('reqdetail/modify', views.modify_request, name='modify_request'),
    path('reqdetail/delete', views.delete_rider_in_request, name='delete_rider_request'),
    path('reqdetail/stop_comfirmed', views.driver_stop_comfirmed, name='stop_comfirmed'),

    # urls for personal info
    path('personal/<int:user_id>', views.personal_info, name='personal_info'),
    path('personal/modify', views.modify_personal_info, name='modify_personal_info'),
    path('personal/password', views.modify_password, name="modify_password"),
    path('personal/register', views.personal_register_driver, name="register_driver"),
    path('personal/stopdriver', views.stop_driver, name='stop_driver'),

    # urls for request history
    path('reqhistory/<int:user_id>/<str:histype>', views.request_history, name="request_history"),

    # urls for register page
    path('register', views.register, name='register'),
    # urls for login page
    path('login', views.login, name="login"),
    path('try_login', views.try_login, name='try_login'),
    path('log_out', views.log_out, name="log_out"),

]