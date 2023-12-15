from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from icecream import ic

from orders.models import Order, OrderItem
from orders.views import user_orders
from store.models import Product, ProductReview

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'account/user/dashboard.html', {'orders': orders})
    # return render(request, 'account/user/dashboard.html', {'section': 'profile', 'orders': orders})

@login_required
def submit_review(request):
    
    if request.method == "POST":
        product_id = request.POST.get('product_id') 
        user = request.user
        topic = request.POST.get('topic')
        review_content = request.POST.get('review')
        rating = int(request.POST.get('rating'))
        order_id = request.POST.get('order')
        
        product = Product.objects.get(pk=product_id)
        
        review = ProductReview.objects.get_or_create(
            product=product,
            user=user,
            topic=topic,
            review=review_content,
            rating=rating
        )
        
        ic(product)
        ic(order_id)
        
        order = Order.objects.get(id=order_id)
        
        order_item = get_object_or_404(OrderItem, order=order, product=product)
        print(order_item.reviewed)
        order_item.reviewed = True
        order_item.save()
        
        print(order_item.reviewed)
        print(request.path)
        
        return redirect('account:dashboard')
        
    return HttpResponse("<h1>Hello World</h1>")

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        print(user_form.errors)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()
            
            print(user.pk)
            
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            
            print(user.email)  # Debug print statement
            print(message)
            return HttpResponse('<h1>Registration Successful!</h1> <h1>Check your email for activation link</h1>')
    else:
        register_form = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': register_form})




def account_activate(request, uidb64, token):
    try:
        
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = UserBase.objects.get(pk=uid)
        print(user)
        
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist) as e:  # Use ObjectDoesNotExist here
        user = None
    finally:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/registration/activation_invalid.html')


