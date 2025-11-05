from xmlrpc import client
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ClientForm
from .models import Client

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/account/')
        else:
            context = {'messageError': 'Invalid credentials'}
            print("Invalid credentials")
            return render(request, '../templates/login.html', context)
    return render(request, '../templates/login.html')

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        if user is not None:
            login(request, user)
            return redirect('/account/')
    return render(request, '../templates/login.html', {'message': 'Registration successful'})    

def account_view(request):
    formClient = ClientForm()
    context = {'formClient': formClient}
    return render(request, '../templates/cuenta.html', context)

def account_update(request):
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
                'formClient': formClient, 
                'message': message
                }
            return render(request, '../templates/cuenta.html', context)
