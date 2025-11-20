from decimal import Decimal
from xmlrpc import client
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from app_products.models import Product
from .forms import ClientForm
from .models import Client, Order, OrderDetail
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

def login_user(request):
    landing_page = request.GET.get('next', None)
    context = {
        'destination': landing_page
    }
    if request.method == 'POST':
        data_username = request.POST.get('username')
        data_password = request.POST.get('password')
        data_destination = request.POST.get('destination')
        userAuth = authenticate(request, username=data_username, password=data_password)
        if userAuth is not None:
            login(request, userAuth)

            if data_destination != 'None':
                print(data_destination)
                return redirect(data_destination)

            return redirect('/account/')
        else:
            context = {'messageError': 'Datos Incorrectos'}
            print("Datos Incorrectos")
            
    return render(request, '../templates/login.html', context)

def logout_user(request):
    logout(request)
    return render(request, '../templates/login.html')

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        # new_user.save()
        if new_user is not None:
            login(request, new_user)
            return redirect('/account/')
        
    return render(request, '../templates/login.html')    

def account_user(request):
    try:
        client_edit = Client.objects.get(user=request.user)
        dataClient = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'dni': client_edit.dni,
        'address': client_edit.address,
        'phone': client_edit.phone,
        'gender': client_edit.gender,
        'birth_date': client_edit.birth_date
    }
    except:
        dataClient = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    
    formClient = ClientForm(dataClient)
    context = {'formClient': formClient}
    return render(request, '../templates/cuenta.html', context)

def account_update(request):
    message = ''
    if request.method == 'POST':
        formClient = ClientForm(request.POST)
        if formClient.is_valid():
            dataClient = formClient.cleaned_data
            # update user info
            update_user = User.objects.get(id=request.user.id)
            update_user.first_name = dataClient['first_name']
            update_user.last_name = dataClient['last_name']
            update_user.email = dataClient['email']
            update_user.save()
            # register client info
            newClient = Client()
            newClient.user = update_user
            newClient.dni = dataClient['dni']
            newClient.address = dataClient['address']
            newClient.phone = dataClient['phone']
            newClient.gender = dataClient['gender']
            newClient.birth_date = dataClient['birth_date']
            newClient.save()

            message = 'Datos actualizados correctamente'
    context = {
              'message': message,
              'formClient': formClient
            }
    return render(request, '../templates/cuenta.html', context)

"""Views for  process of buying products"""

@login_required(login_url='/login/')
def register_order(request):
    try:
        client_edit = Client.objects.get(user=request.user)
        dataClient = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'dni': client_edit.dni,
        'address': client_edit.address,
        'phone': client_edit.phone,
        'gender': client_edit.gender,
        'birth_date': client_edit.birth_date
    }
    except:
        dataClient = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    
    formClient = ClientForm(dataClient)
    context = {'formClient': formClient}
    return render(request, '../templates/pedido.html', context)


@login_required(login_url='/login/')
def confirm_order(request):
    context = {}
    if request.method == 'POST':
        # update user info
        update_user = User.objects.get(id=request.user.id)
        update_user.first_name = request.POST['first_name']
        update_user.last_name = request.POST['last_name']
        update_user.email = request.POST['email']
        update_user.save()
        # register or update client info
        try:
            client_order = Client.objects.get(user=request.user)
            client_order.phone = request.POST['phone']
            client_order.address = request.POST['address']
            client_order.save()
        except:
            client_order = Client()
            client_order.user = update_user
            client_order.address = request.POST['address']
            client_order.phone = request.POST['phone']
            client_order.save()

        # register new order
        number_order = ''
        total_amount = (Decimal(request.session.get('total_amount', '0.00'))).quantize(Decimal('0.01'))
        new_order = Order()
        new_order.client = client_order
        new_order.save()

        # register order details
        cart_order = request.session.get('cart', {})
        for key, value in cart_order.items():
            product_order = Product.objects.get(id=value['product_id'])
            order_detail = OrderDetail()
            order_detail.order = new_order
            order_detail.product = product_order
            order_detail.price = float(Decimal(value['price']).quantize(Decimal('0.01')))
            order_detail.quantity = int(value['quantity'])
            order_detail.subtotal = float(value['subtotal'])
            order_detail.save()

        # update order
        number_order = f"ORD{new_order.registration_date.strftime('%Y%m%d')}{str(new_order.id).zfill(5)}"
        new_order.number_order = number_order
        new_order.amount_total = total_amount
        new_order.save()

        # create button for paypal payment
        paypal_dict = {
        "business": "sb-caoi4747409839@business.example.com",
        "amount": total_amount,
        "item_name": "PEDIDO CODIGO" + number_order,
        "invoice": number_order,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/thanks_order/'),
        "cancel_return": request.build_absolute_uri('/'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }

        # Create the instance.
        formPayPal = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            'order': new_order,
            'formPayPal': formPayPal
        }

        # clean the shopping cart
        del request.session['cart']
        request.session['total_amount'] = "0.00"

    return render(request, '../templates/compra.html', context)

def thanks_order(request):
    return render(request, '../templates/gracias.html')

# Test paypal integration
def view_that_asks_for_money(request):
    # What you want the button to do.
    paypal_dict = {
        "business": "sb-caoi4747409839@business.example.com",
        "amount": "100.00",
        "item_name": "producto de prueba de paypal",
        "invoice": "100-ED100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('home'),
        "cancel_return": request.build_absolute_uri('Logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)