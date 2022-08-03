from django.db import models

# Create your models here.
class PaymentInitialized(models.Model):
    order_id = models.CharField(max_length=200, primary_key=True)
    mid = models.IntegerField()
    amount = models.FloatField()
    actual_amount = models.FloatField()
    gid = models.CharField(max_length=200)
    g_password = models.CharField(max_length=50)
    
class PaymentHistory(models.Model):
    order_id = models.CharField(max_length=200, primary_key=True)
    payment_id = models.CharField(max_length=200)
    mid = models.IntegerField()
    amount = models.FloatField()
    