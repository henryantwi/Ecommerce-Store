from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from icecream import ic

from basket.basket import Basket
from payment.models import Payment

from .models import Order, OrderItem


def contact_admin(request):
    if request.method == 'POST':
        user_issue = request.POST.get('user_issue', '')

        # Email details
        admin_email = 'henryantwi191@gmail.com'
        subject = 'User Issue Submitted'
        message = f"The user has submitted the following issue:\n\n{user_issue}"

        # Send email to admin
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Your sender email
            [admin_email],
            fail_silently=False,
        )

        # Optionally, you can provide a success message or redirect the user
        return HttpResponse('<b>Issue submitted successfully!</b>')

    return render(request, 'orders/contact_admin.html')


@login_required
def order_placed(request):
    basket = Basket(request)
    basket.clear()

    # Retrieve the user's payment with the latest date_created (assumed to be the most recent order)
    user_payment = Payment.objects.filter(user=request.user).order_by('-date_created').first()

    # Check if a payment exists for the user and examine its billing_status
    if user_payment:
        billing_status = user_payment.billing_status
        payment_id = user_payment.ref
        if billing_status:
            # Order is successful, send email to the user
            user_email = request.user.email
            subject = 'Your Order Details'
            email_template = 'orders/emails/order_confirmation.html'  # Replace with your email template

            order_items = OrderItem.objects.filter(order__payments=user_payment)

            total_amount = user_payment.amount
            # Add more order-related data as per your requirement

            # Prepare context for the email
            context = {
                'user': request.user,
                'order_items': order_items,
                'total_amount': total_amount,
                'payment_id': payment_id,
                # Add more context variables related to the order if needed
            }

            # Prepare and send the successful order placement email
            html_message = render_to_string(email_template, context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user_email],
                html_message=html_message,
            )

        else:
            # Order is unsuccessful, send email to the user to contact the admin
            user_email = request.user.email
            subject = 'Order Unsuccessful'
            admin_email = 'henryantwi191@gmail.com'

            admin_contact_link = request.build_absolute_uri(reverse('orders:contact-admin'))
            admin_message = (
                f"Dear {request.user},\n\n"
                f"Unfortunately, your order was unsuccessful. Please contact the admin at {admin_email} "
                f"with the following details:\n\n"
                f"Username: {request.user}\n"
                f"Email: {user_email}\n"
                f"Order ID: {user_payment.id}\n\n"
                f"You can use this link to easily contact the admin: {admin_contact_link}\n\n"
                f"Thank you."
            )

            # Send email to the user prompting them to contact the admin
            send_mail(
                subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [user_email],
            )

    return render(request, 'orders/orderplaced.html', {'billing_status': billing_status})


@login_required
def initiate_payment(request):
    basket = Basket(request)

    if request.method == 'POST':

        user_id: int = request.user.id
        user = get_object_or_404(get_user_model(), id=user_id)
        cust_name = request.POST.get('custName')
        email = request.POST.get('email')
        phone = request.POST.get('custPhone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        city = request.POST.get('city')
        total = str(basket.get_total_price())
        total = total.replace('.', '')
        total = int(total)
        basket_total = total

        order = Order.objects.create(
            user=user,
            total_price=basket_total,
            full_name=cust_name,
            address1=address1,
            address2=address2,
            phone=phone,
            state=state,
            city=city,
        )
        order.save()
        order_id = order.pk

        for item in basket:
            OrderItem.objects.create(
                order_id=order_id,
                product=item['product'],
                price=item['price'],
                quantity=item['qty']
            )
            

        payment = Payment.objects.create(
            order=order,
            amount=total,
            email=email,
            user=user
        )
        payment.save()

        context = {
            'amount': basket.get_total_price(),
            'payment': payment,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        }
        return render(request, 'orders/make_payment.html', context)

    return render(request, 'orders/home.html')


def user_orders(request):
    user_id = request.user.id
    # Fetch orders associated with the user using the Payment model's order field
    orders = Order.objects.filter(payments__user_id=user_id, payments__billing_status=True).order_by('-date_ordered')
    
    # print(orders.get_status)

    return orders
