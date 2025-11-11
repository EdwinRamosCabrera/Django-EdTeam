from django.urls import path
from . import views

app_name = 'app_auth'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('create_user/', views.create_user, name='create_user'),
    path('account/', views.account_user, name='account_user'),
    path('account/update/', views.account_update, name='account_update'),
    path('logout/', views.logout_user, name='logout_user'), 
    path('register_order/', views.register_order, name='register_order'),
]
