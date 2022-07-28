from django.urls import path
from . import views


urlpatterns = [
    path('',views.group, name='group'),
    path('upvote/',views.bill_upvote, name='bill_upvote'),
    path('bills-download/<str:filename>',views.bills_download, name='bills_download'),
]