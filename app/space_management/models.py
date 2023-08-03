from django.db import models

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State , on_delete=models.CASCADE)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)

class Building(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=12)
    electricity_charge =  models.DecimalField(default=0,max_digits=5,decimal_places=2)
    water_charge = models.DecimalField(default=0,max_digits=5,decimal_places=2)
    maintenance_charge = models.PositiveIntegerField(default=0)
    image_folder = models.CharField(max_length=100)
    city =  models.ForeignKey(City , on_delete=models.CASCADE)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)

class RentalSpace(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    area = models.FloatField()
    floor = models.IntegerField()
    rent_price = models.PositiveIntegerField()
    description = models.TextField(null=True,blank=True)
    image_folder = models.CharField(max_length=100)
    document_folder = models.CharField(max_length=100)
    is_available =  models.BooleanField(default=True)
    building = models.ForeignKey(Building , on_delete=models.CASCADE)
    min_period = models.IntegerField(default=0)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active =  models.BooleanField(default=True)
    security_deposit =  models.PositiveIntegerField(default=0)

   
