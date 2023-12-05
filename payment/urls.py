from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('<str:ref>/', views.verify_payment, name='verify-payment'),
]

