import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'myenv/Lib/site-packages')))

import requests,json
import azure.servicebus
from utils import process_request, send_to_queue, send_email, twilio_password_reset, twilio_route_call
from graph import Graph
import time,twilio

data = open(os.environ['data']).read()
print(data + "\n")
jdata = json.loads(data, strict=False)
cData = {
        'routeToMainMenu':True,
        'hangUp': False
}
try:
    if jdata['channel'] == 'twilio':
        print("Channel = Twilio")
        result = twilio_password_reset(data)
        print("sleeping for 20 seconds")
        time.sleep(20)
        print("sending email")
        send_email(result)
        asid = jdata['asid']
        csid = jdata['csid']
        url = jdata['redirect_url_success']
        print("routing call")
        twilio_route_call(asid, csid, url)

    else:
        result = process_request(data)
        print(result)
        scData = dict(cData)
        scData['hangUp'] = True
        bot_data = {
            'text': 'Your password has been reset and an email will be sent to your manager containingg the new password.',
            'channelData':{
                'hangUp' : True
            },
            'address':jdata['address']
        }

        send_to_queue(bot_data, 'send-to-bot')
        send_email(result)
    
except Exception as e:
    print(str(e))
    if jdata['channel'] == 'twilio':
        pass
    else:
        bot_data = {
            'text': str(e),
            'channelData':{
                'routeToMainMenu':True
            },
            'address':jdata['address']
        }

        send_to_queue(bot_data, 'send-to-bot')

