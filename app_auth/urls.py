from django.urls import path
from . import views

app_name = 'app_auth'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('create_user/', views.create_user, name='create_user'),
    path('account/', views.account_view, name='account_view'),
    path('account/update/', views.account_update, name='account_update'),
]
