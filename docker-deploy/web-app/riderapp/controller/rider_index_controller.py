import sys
sys.path.append('..')
import riderapp.models as models
import json

def rider_index(request):
    user_id = request.session.get('id')
    #get owner request
    owner_requests = models.Request.objects.filter(owner_id=user_id, status=0) | models.Request.objects.filter(owner_id=user_id, status=1)
    #get share request
    all_requests = models.Request.objects.filter(status=0) | models.Request.objects.filter(status=1)
    all_requests.exclude(owner_id=user_id)
    sharer_requests = []
    for req in all_requests:
        if models.Shared.objects.filter(request_id=req.id, user_id=user_id):
            sharer_requests.append(req)

    context = {
        'owner_requests': owner_requests,
        'sharer_requests': sharer_requests
    }
    return context

def create_new_request(request):
    response = {'status': '0'}
    info = request.POST
    boarding = info.get('boarding', '')
    destination = info.get('destination', '')
    arrival_time = info.get('arrival_time', '')
    psnumbers = info.get('psnumbers', '')
    vehicle_tid = info.get('vehicle_tid', '')
    canshare = info.get('canshare', '')
    specific = info.get('specific', '')
    owner_id = request.session.get('id')
    
    if boarding != '' and destination != '' and arrival_time != '' and psnumbers != '' and canshare != '' and owner_id != '':
        if canshare == '0':
            canshare = False
        else:
            canshare = True
        if specific == '':
            specific = None
        if vehicle_tid == '0':
            vehicle_tid = None
        else:
            vehicle_tid = int(vehicle_tid)
        new_request = models.Request(owner_id=owner_id, boarding=boarding,destination=destination,arrival_time=arrival_time,psnumbers=int(psnumbers),vehicle_tid=vehicle_tid,specific=specific,canshare=canshare,status=0)
        new_request.save()
        response['status'] = '1'
    return json.dumps(response)