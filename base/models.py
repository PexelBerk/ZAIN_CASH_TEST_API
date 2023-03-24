from django.db import models

# Create your models here.



class Transaction(models.Model):
    amount = models.IntegerField()
    serviceType = models.TextField()
    orderid = models.TextField()
    redirectUrl = models.TextField()
    iat = models.IntegerField()
    exp = models.IntegerField()
    lang = models.TextField()


class Merchant(models.Model):
    merchantId = models.TextField()
    secret = models.TextField()
    msisdn = models.TextField()
    name = models.TextField()
    number = models.TextField()





