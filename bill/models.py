from django.db import models

# Create your models here.
class Bill(models.Model):
    photo = models.FileField(upload_to='bills/')
    bid = models.IntegerField(primary_key=True)
    billed_for = models.CharField(max_length=400)
    amount = models.FloatField()
    status = models.CharField(max_length=2)  #p or a or c (pending or approve or completed)
    upvote =  models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    gid = models.IntegerField()
    mid = models.IntegerField(default=0)   #mid of user
    
    def __str__(self):
        return(str(self.bid) + ' ' + str(self.billed_for))