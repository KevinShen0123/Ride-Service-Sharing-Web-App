import sys
sys.path.append('..')
import smtplib
from email.mime.text import MIMEText
import _thread
import riderapp.models as models

def __get_all_rider_email(targetRequest):
    emails = []
    #owner
    owner = models.User.objects.get(id=targetRequest.owner_id)
    emails.append(owner.email)
    #sharer
    shareds = models.Shared.objects.filter(request_id=targetRequest.id)
    for sharer in shareds:
        emails.append(models.User.objects.get(id=sharer.user_id).email)
    return emails

def __mult_sendEmail(dests, content):
    _thread.start_new_thread(__sendEmail, (dests, content))
    #_thread.start_new_thread(test_sending, (dests, content))

def test_sending(dests, content):
    msg_from = "fjchxq@qq.com"
    password = "hhfdmpavfcwybiig"
    dest = 'fjchxq@gmail.com'

    content += '\n'
    for d in dests:
        content += 'receiver:'+d+'\n'
    client = smtplib.SMTP_SSL("smtp.qq.com", smtplib.SMTP_SSL_PORT)
    client.login(msg_from, password)
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "Riderapp Notification"
    msg["From"] = msg_from
    msg["To"] = dest    
    client.sendmail(msg_from, dest, msg.as_string())
    client.quit()

# driver stop comfirming request
def send_cancel_mail(request):
    dests = __get_all_rider_email(request)
    content = 'Request:\n'
    content += str(request) + '\n'
    content += 'Driver gave up this request.'
    __mult_sendEmail(dests, content)

# driver comfirmed request
def send_comfirmed_mail(request):
    dests = __get_all_rider_email(request)
    content = 'Request:\n'
    content += str(request) + '\n'
    content += 'Your request has been comfirmed!'
    __mult_sendEmail(dests, content)

# sharer has been deleted from request
def send_dele_mail(request, rider_id):
    content = 'Request:\n'
    content += str(request) + '\n'
    content += 'You were removed from that request'
    rider = models.User.objects.get(id=int(rider_id))
    __mult_sendEmail([rider.email], content)

# owner canceled that request
def send_owner_cancel_request(request):
    dests = __get_all_rider_email(request)
    content = 'Request:\n'
    content += str(request) + '\n'
    content += 'Your request was canceled by the request owner'
    __mult_sendEmail(dests, content)

# modifier modify fieldname to fieldvalue in request
def send_modify_mail(request, fieldname, fieldvalue, modifier_id):
    if fieldvalue == None:
        fieldvalue = 'Not specify'
    dests = __get_all_rider_email(request)
    content = 'Request:\n'
    content += str(request) + '\n'
    modifier = models.User.objects.get(id=modifier_id)
    content += 'Your request was modified by '+modifier.username+'\n'
    content += fieldname + ' was modified to ' + fieldvalue
    __mult_sendEmail(dests, content)


# send email by multithread
def __sendEmail(dests, content):
    msg_from = "fjchxq@qq.com"
    password = "hhfdmpavfcwybiig"

    client = smtplib.SMTP_SSL("smtp.qq.com", smtplib.SMTP_SSL_PORT)
    client.login(msg_from, password)
    for dest in dests:
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = "Riderapp Notification"
        msg["From"] = msg_from
        msg["To"] = dest    
        client.sendmail(msg_from, dest, msg.as_string())
    client.quit()