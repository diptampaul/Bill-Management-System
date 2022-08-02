from django.contrib import admin
from .models import Group_Details, Group_Members, AdminBillClear

# Register your models here.
admin.site.register(Group_Details)
admin.site.register(Group_Members)
admin.site.register(AdminBillClear)