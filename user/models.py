from django.db import models

# Create your models here.
class GroupMemberPayout(models.Model):
    mid = models.IntegerField(primary_key=True)
    upi = models.CharField(max_length=200, null=True)
    account_number = models.CharField(max_length=100, null=True)
    account_name = models.CharField(max_length=30, null=True)
    ifsc_code = models.CharField(max_length=20, null=True)
    wallet_number = models.IntegerField(null=True)
    wallet_type = models.CharField(max_length=2, null=True)  #P = Paytm, G = GooglePay
    receiving_preference = models.CharField(max_length=2)    #B = Bank, W = Wallet, U = UPI