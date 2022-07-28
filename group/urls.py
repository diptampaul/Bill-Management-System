from django.urls import path
from . import views


urlpatterns = [
    path('',views.group, name='group'),
    path('upvote/',views.bill_upvote, name='bill_upvote'),
    path('adding-new-bill/',views.add_bill_home, name='add_bill_home'),
    path('bill-added/',views.bill_added, name='bill_added'),
    path('bills-download/<str:filename>',views.bills_download, name='bills_download'),
]