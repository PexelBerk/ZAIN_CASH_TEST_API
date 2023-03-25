from django.urls import path

from . import views

urlpatterns = [
    path("transaction/init", views.init_transaction, name="init_transaction"),
    path("transaction/pay", views.pay_transaction, name="pay_transaction"),
]
