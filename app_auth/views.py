from xmlrpc import client
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ClientForm
from .models import Client
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