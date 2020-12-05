import json
import requests
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .utils import meanings, synonyms, antonyms, examples
from .token import PAGE_ACCESS_TOKEN, VERIFY_TOKEN


def callSendAPI(sender_psid, response):
    request_body = {
    "recipient": {
      "id": sender_psid
    },
    "message": response
  }
        
    #if msg is not None:                 
    endpoint = f"https://graph.facebook.com/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response_msg = json.dumps(request_body)
    status = requests.post(
        endpoint, 
        headers={"Content-Type": "application/json"},
        data=response_msg)
    return status.json()

        
class IndexView(View):
    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax
    
    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status=403)
        return HttpResponse(hub_challenge)
            

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            
            response = {}
            for message in entry['messaging']:
                sender_psid = message['sender']['id'] # sweet!
                
                #########################################
                #***Handle payload
                if 'postback' in message:
                    payload = message['postback'].get('payload')
                    if payload=='first_handshake':
                        response = {
                            "text": "Aah, good to see you! I'm `The Dictionary Bot`. Give me any word and I'll tell you its meaning. 😀"
                        }

                #######################################
                #Handle message
                elif 'message' in message:
                    if 'quick_reply' in message['message']:
                        payload = message['message']['quick_reply']['payload']
                        data = payload[:2] #get the payload from quickreply (sy / an / ex)
                        text = payload[2:] # get the actual word
                        response = handlePayload(data, text)
                    
                    elif 'attachments' in message['message']:
                        response = {'text': 'Please send a text message.'}

                    else:
                        text = message['message'].get('text')
                        response = handleMessage(text)
                
                
                        

                #Call the send api message
                callSendAPI(sender_psid, response)
                
                
        return HttpResponse("Success", status=200)


def handlePayload(payload, text):
    result = ''
    if payload=='sy':
        result = synonyms(text)

    elif payload=='an':
        result = antonyms(text)

    elif payload=='ex':
        result = examples(text)

    if not result:
        result = "Not Found. Please try something else..."

    response = {
        "text": result,
        "quick_replies":[
        {
            "content_type":"text",
            "title":"Synonyms",
            "payload":"sy"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/synonyms.png"
        },{
            "content_type":"text",
            "title":"Antonyms",
            "payload":"an"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/antonyms.png"
        },{
            "content_type":"text",
            "title":"Examples",
            "payload":"ex"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/examples.png"
        }
        ]
        
    }
    return response



def handleMessage(text=''):
    response = {}
    result = ''
    if text:
        result = meanings(text)

    if not result:
        response = {
            "text": "Sorry! I'm not sure what that is. Please make sure that it is a single word and is spelled right. 😞"
        }
    else:
        response = {
            "text": result,
            "quick_replies":[
        {
            "content_type":"text",
            "title":"Synonyms",
            "payload":"sy"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/synonyms.png"
        },{
            "content_type":"text",
            "title":"Antonyms",
            "payload":"an"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/antonyms.png"
        },{
            "content_type":"text",
            "title":"Examples",
            "payload":"ex"+text,
            "image_url":"https://messengerdictionarybot.herokuapp.com/static/img/examples.png"
        }
        ]
        }
    return response
