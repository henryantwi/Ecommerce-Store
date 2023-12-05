from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('contact_admin/', views.contact_admin, name='contact-admin'),
    path('orderplaced/', views.order_placed, name='order-placed'),
    path('', views.initiate_payment, name='initiate-payment'),
]
