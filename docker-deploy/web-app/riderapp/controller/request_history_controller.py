import sys
sys.path.append('..')
import riderapp.models as models

def request_history(request, user_id, histype):
    context = {}
    history = []
    if histype == 'r':
        owner_history = getRiderHistory(user_id)
        for his in owner_history:
            history.append(his)
        share_history = getSharerHistory(user_id)
        for his in share_history:
            history.append(his)
    elif histype == 'd':
        history = getDriverHistory(user_id)
    context['history'] = history
    return context

def getRiderHistory(user_id):
    requests = models.Request.objects.filter(owner_id=int(user_id), status=2)
    return requests

def getSharerHistory(user_id):
    sql_statement = "select riderapp_request.* from riderapp_request, riderapp_shared where riderapp_request.id = riderapp_shared.request_id"
    sql_statement += " and status=2 and riderapp_shared.user_id="+str(user_id)
    requests = models.Request.objects.raw(sql_statement)
    return requests

def getDriverHistory(user_id):
    requests = models.Request.objects.filter(driver_id=int(user_id), status=2)
    return requests
