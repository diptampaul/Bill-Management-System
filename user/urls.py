from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('add-member/',views.add_member, name='add_member'),
    # path('register/',views.register, name='register'),
    # path('login/',views.login, name='login'),
    # path('logout/',views.logout, name='logout'),
]