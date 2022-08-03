from django.urls import path
from . import views


urlpatterns = [
    path('top-up/',views.top_up_wallet, name='top_up_wallet'),
    #path('confirm/',views.top_up_confirm, name='top_up_confirm'),
    path('top-up/status/',views.paymenthandler, name='paymenthandler'),
]