from django.db import models
from app.space_management.models import *
from app.user_authentication.models import *

# Create your models here.

class UtilityReading(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    year = models.IntegerField()
    electricity_reading = models.IntegerField()
    electricityreading_image=models.CharField(max_length=500)
    water_reading = models.IntegerField()
    waterreading_image=models.CharField(max_length=500)
    space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False,null=True)
    approved_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)

    # class Meta:
    #     unique_together = ('month','space','year')
    
    
class Grievances(models.Model):

    ISSUE_STATUS_CHOICE=((1,'open'),(2,'assigned'),(3,'in Process'),(4,'closed'),(5,'declined')) 
    ISSUE_TYPE_CHOICE = ((1,'discontinuation'),(2,'rent'),(3,'electricity'),(4,'water'),(5,'common area maintenance'))

    id=models.AutoField(primary_key=True)
    issue_type=models.PositiveIntegerField(choices=ISSUE_TYPE_CHOICE)
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='customer_grievances')
    assignee=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='assigned_grievances',null=True,blank=True)   
    space=models.ForeignKey(RentalSpace,on_delete=models.CASCADE)       
    issue_status=models.PositiveIntegerField(choices=ISSUE_STATUS_CHOICE,default=1)   
    subject=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField()
    issue_image_folder=models.CharField(max_length=500)
    is_created=models.DateTimeField(auto_now=False,auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)


class Invoice(models.Model):

    Choice = ((1, 'Pending'), (2, 'Completed'))

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    payment_status = models.IntegerField(choices=Choice)
    rent_amount = models.IntegerField()
    water_charge = models.IntegerField()
    electricity_charge = models.IntegerField()
    maintenance_charge = models.IntegerField()
    total_amount = models.IntegerField()
    due_date = models.DateField()
    late_fee =  models.IntegerField(null=True, blank=True)
    month = models.IntegerField()
    year = models.IntegerField()
    payment_type = models.IntegerField(null=True, blank=True)
    invoice_number = models.CharField(max_length=100)
    kiosk_number = models.CharField(max_length=10, null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    is_created=models.DateTimeField(auto_now=False,auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)


class Payment(models.Model):
    payment_id = models.CharField(max_length=500)
    order_id = models.CharField(max_length=500)
    currency = models.CharField(max_length=10)
    amount = models.FloatField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    error_code = models.TextField(null=True, blank=True)
    is_created=models.DateTimeField(auto_now=False,auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)


class Notification_Content(models.Model):
    id = models.AutoField(primary_key=True)
    notification_type = models.CharField(max_length=500)
    content = models.TextField()