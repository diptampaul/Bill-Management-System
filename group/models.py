from statistics import mode
from django.db import models

# Create your models here.
class Group_Details(models.Model):
    gid = models.IntegerField(primary_key=True)
    g_name = models.CharField(max_length=200)
    g_password = models.CharField(max_length=50)
    g_members = models.IntegerField(default=0)
    
    
class Group_Members(models.Model):
    mid = models.IntegerField(primary_key=True)   #Groupid + Member Number    #And also check if mid can never be greater than gid
    gid = models.IntegerField(default=0)
    m_name = models.CharField(max_length=200)
    wallet_balance = models.FloatField(default=0)
    
