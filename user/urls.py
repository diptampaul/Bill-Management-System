from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('add-member/',views.add_member, name='add_member'),
    path('add-payment/',views.add_payment, name='add_payment'),
    path('addding-payment-successful/',views.add_successful_payment, name='add_successful_payment'),
    # path('register/',views.register, name='register'),
    # path('login/',views.login, name='login'),
    # path('logout/',views.logout, name='logout'),
]