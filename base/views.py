from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


from .models import Merchant, Transaction, Account

import json
import jwt

# Create your views here.

@api_view(['POST'])
@csrf_exempt
def init_transaction(request):
    if request.method == 'POST':
        token = request.data['token']
        merchantId = request.data['merchantId']
        lang = request.data['lang']

        merchant = Merchant.objects.get(merchantId=merchantId)


        data = jwt.decode(token, merchant.secret, algorithms=['HS256'])

        transaction = Transaction.objects.create(
            merchant=merchant,
            amount=data.get('amount'),
            serviceType=data.get("serviceType"),
            msisdn=data.get("msisdn"),
            orderId=data.get("orderId"),
            redirectUrl=data.get("redirectUrl"),
            iat=data.get("iat"),
            exp=data.get("exp"),
            lang=data.get("lang"),
        )

        transaction.generate_operation_id()
        transaction.save()
        
        data = {
            "id":transaction.operation_id
        }

        return HttpResponse(json.dumps(data))
        
         
        
    else:
        data = {
            "err":{
                "msg":"most be post request"
            }
        }
        return HttpResponseBadRequest(json.dumps(data))

