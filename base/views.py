from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db import transaction as trans

from .models import Merchant, Transaction, Account

import json
import jwt
import time

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
            orderId=data.get("orderId"),
            redirectUrl=data.get("redirectUrl"),
            iat=data.get("iat"),
            exp=data.get("exp"),
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





def pay_transaction(request):

    try:
        id = request.GET.get("id")
    except:
        return HttpResponse("no operation id provided")
    
    try:
        transaction = Transaction.objects.get(operation_id=id)
    except:
        return HttpResponse("no transaction with this operation id")


    context = {
        "merchant":transaction.merchant,
        "amount":transaction.amount,
        "operation_id":transaction.operation_id,
    }


    return render(request, "payment.html", context)

@api_view(['POST'])
@csrf_exempt
def otp_confirmation(request):
    if request.method == "POST":
        phone = request.data['phone']
        pin   = request.data['pin']
        operation_id = request.data['operation_id']

        
        try:
            transaction = Transaction.objects.get(operation_id=operation_id)
        except:
            return HttpResponse("no transaction with this id")

        

        try:
            account = Account.objects.get(phone=phone)
        except:
            _time = int(time.time())
            data = {
                "status":"failed",
                "msg":"wrong credentionals",
                "orderid":transaction.orderId,
                'iat': _time,
                'exp': _time + 60 * 60 * 4
            }
            token = jwt.encode(data, transaction.merchant.secret, algorithm='HS256')
            return redirect(transaction.redirectUrl+ f"?token={token}")

        if account.pin != pin:
            _time = int(time.time())
            data = {
                "status":"failed",
                "msg":"wrong credentionals",
                "orderid":transaction.orderId,
                'iat': _time,
                'exp': _time + 60 * 60 * 4
            }
            token = jwt.encode(data, transaction.merchant.secret, algorithm='HS256')
            return redirect(transaction.redirectUrl+ f"?token={token}")
        
        if account.balance < transaction.amount:
            _time = int(time.time())
            data = {
                "status":"failed",
                "msg":"not enough balance",
                "orderid":transaction.orderId,
                'iat': _time,
                'exp': _time + 60 * 60 * 4
            }
            token = jwt.encode(data, transaction.merchant.secret, algorithm='HS256')
            return redirect(transaction.redirectUrl+ f"?token={token}")

        transaction.account = account
        transaction.save()
        context = {
            "operation_id":operation_id,
            'amount':transaction.amount,
            'balance':account.balance
        }
        return render(request, "otp.html", context)
    
    else:
        return HttpResponse("most be post request")



@api_view(['POST'])
@csrf_exempt
def check_otp(request):
    if request.method == "POST":
        operation_id = request.data['operation_id']
        otp = request.data['otp']
        
        
        try:
            transaction = Transaction.objects.get(operation_id=operation_id)
        except:
            return HttpResponse("no transaction with this id")

        if transaction.account.otp != otp:
            _time = int(time.time())
            data = {
                "status":"failed",
                "msg":"wrong creds",
                "orderid":transaction.orderId,
                'iat': _time,
                'exp': _time + 60 * 60 * 4
            }
            token = jwt.encode(data, transaction.merchant.secret, algorithm='HS256')
            return redirect(transaction.redirectUrl+ f"?token={token}")
        

        with trans.atomic():
            transaction.account.balance -= transaction.amount
            transaction.merchant.balance += transaction.amount
            transaction.account.save()
            transaction.merchant.save()

        
        _time = int(time.time())
        data = {
            "status":"success",
            "msg":"success",
            "orderid":transaction.orderId,
            'iat': _time,
            'exp': _time + 60 * 60 * 4
        }
        token = jwt.encode(data, transaction.merchant.secret, algorithm='HS256')
        return redirect(transaction.redirectUrl+ f"?token={token}")


    else:
        return HttpResponse("most be post request")



