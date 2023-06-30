#This is the controller for driver_index.html
import sys
sys.path.append('..')
import riderapp.models as models

def driver_index(request):
    cr = models.Request.objects.filter(driver_id=request.session.get('id'), status=1)
    context = {
        'comfirmedRequests':cr
    }
    return context