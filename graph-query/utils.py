from azure.servicebus import ServiceBusService, Message, Queue
from graph import Graph
import json
import sendgrid
import os
from sendgrid.helpers.mail import *
import requests
from requests.auth import HTTPBasicAuth
import urllib
from twilio.rest import Client


def validate_user_data(user_data, graph_data):
    keys = ['city','phone','zip']
    for key in keys:
        if str(user_data[key]).lower() != str(graph_data[key]).lower():
            raise Exception("Invalid " + key + ". It does not match with your active directory data. Please try again!")
    return True


def process_request(data):
    try:
        data = json.loads(data, strict=False)
    except Exception as e:
        raise Exception("An application error has occured. Please try again later!")

    try:
        keys = ['phone', 'zip', 'city', 'portal_id']
        bot_user_data = { key: data.get(key, None) for key in keys }
        try:
            pid = int(bot_user_data.get('portal_id','0'))
        except Exception as e:
            raise Exception("Your portal Id is invalid. Please try again later.")
        graph = Graph(pid)
        graph_user_data = graph.getUserData()
        validate_user_data(bot_user_data, graph_user_data)
        pswd = graph.resetPassword()
    except Exception as e:
        raise(e)
    text = 'your password has been reset. An email will be sent to your manager'
    graph_user_data['password'] = pswd['newPassword']
    graph_user_data['portal_id'] = pid
    return graph_user_data
    
def send_to_queue(data, queue):
    
    svcbus = ServiceBusService(
        service_namespace='botista',
        shared_access_key_name='RootManageSharedAccessKey',
        shared_access_key_value='0/O8pigV09yoxSrSpEjKK+uoMWS1JYYJQEbnbzVxnpA=')

    event = Message(json.dumps(data))
    svcbus.send_queue_message(queue, event)

def send_email(data):
    default = 'tarik.setia@nttdata.com'
    api_key = 'SG.A9CCKI49Q--KebhxMTpALA.kP9YhVLI9okaQLgHplLQEboQyvnxiHh9zhH03_hoYHg'
    sg = sendgrid.SendGridAPIClient(apikey=api_key)
    to = data.get('mail', None)
    to = to if to else default
    from_email = Email("NoReply@SherlockBot.com")
    to_email = Email(to)
    subject = "Password Reset"
    content = Content("text/plain", "Password has been reset for {}. The new password is {}. Goto https://portal.azure.com to login and change the password".format(data['name'], data['password']))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def twilio_password_reset(data):
    try:
        data = json.loads(data, strict=False)
    except Exception as e:
        raise Exception("An application error has occured. Please try again later!")
    
    pid = data['portalId']
    graph = Graph(pid)
    pswd = graph.resetPassword()
    return {'password': pswd['newPassword'] , 'portal_id': pid ,'name':data['name']}


def route_call(asid, csid, url):
    twilio_url = 'https://api.twilio.com/2010-04-01/Account/{}/Calls/{}'.format(asid,csid)
    user = 'ACea7d0dd100c883a4637a0fb48b66072b'
    password = 'f885d726c710e23f2b8bd7b09bf612d1'
    auth = HTTPBasicAuth(user, password)
    payload = {
        'Method':'POST',
        'Url':url
    }
    payload = urllib.urlencode(payload)
    print(payload)
    print(twilio_url)
    resp = requests.post(twilio_url, data=payload, auth=auth)
    print(resp.text)
    return resp.status_code == 200

def twilio_route_call(asid,csid,url):

    account_sid = 'AC2330c6acc9cdac777b2f1dca56d69876'
    auth_token = 'd7cc39c73c50bdbf845907f2489598ed'
    client = Client(account_sid, auth_token)

    call = client.calls(csid) \
                .update(
                    method='POST',
                    url=url
                )