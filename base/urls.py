from django.urls import path

from . import views

urlpatterns = [
    path("transaction/init", views.init_transaction, name="init_transaction"),
    path("transaction/pay", views.pay_transaction, name="pay_transaction"),
    path("transaction/otp", views.otp_confirmation, name="otp_confirmation"),
    path("transaction/otp/check", views.check_otp, name="check_otp"),
]
