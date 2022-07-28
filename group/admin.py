from django.contrib import admin
from .models import Group_Details, Group_Members

# Register your models here.
admin.site.register(Group_Details)
admin.site.register(Group_Members)