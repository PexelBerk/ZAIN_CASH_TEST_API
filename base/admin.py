from django.contrib import admin

from .models import Merchant, Transaction, Account

admin.site.register(Merchant)
admin.site.register(Transaction)
admin.site.register(Account)

