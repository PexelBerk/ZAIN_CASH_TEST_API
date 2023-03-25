from django.urls import path

from . import views

urlpatterns = [
    path("transaction/init", views.init_transaction, name="init_transaction"),
]
