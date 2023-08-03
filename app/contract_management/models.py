from django.db import models
from app.user_authentication.models import *
from app.space_management.models import *
from app.invoice_management.models import *
# Create your models here.


class SpaceRequest(models.Model):

    Choice = ((1, 'Pending'), (2, 'Accepted'),(3, 'Rejected'), (4, 'Cancelled'), (5, 'Security Deposit Initiated'), (6, 'Security Deposit Collected'), (7, 'Approved'))

    id = models.AutoField(primary_key=True)
    space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    period = models.IntegerField(default=0)
    valid_from = models.DateField()
    valid_to = models.DateField()
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Choice)
    purpose = models.TextField(null=True,blank=True)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=False)
    security_payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)

class Contract(models.Model):

    Choice = ((1, 'active'), (2, 'expired'))

    id = models.AutoField(primary_key=True)
    space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    valid_from = models.DateField()
    valid_to = models.DateField()
    period = models.IntegerField(default=0)
    status = models.IntegerField(choices=Choice,default=1)
    documentfolder = models.CharField(max_length=50,null=True, blank=True)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=False)



class ContractDetails(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    site_address = models.CharField(max_length=100)
    space_id = models.CharField(max_length=10)
    customer = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.PositiveIntegerField()
    electricity = models.DecimalField(max_digits=5, decimal_places=2)
    water = models.DecimalField(max_digits=5, decimal_places=2)
    clause = models.TextField(blank=True)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=False)
