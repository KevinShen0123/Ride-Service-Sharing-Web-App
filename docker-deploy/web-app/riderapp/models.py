from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    role = models.IntegerField() #0:common user; 1:driver
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)+' '+str(self.username)+' '+str(self.password)+' '+str(self.name)+' '+str(self.role)+' '+str(self.email)
    
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    vehicle_tid = models.IntegerField()
    license_plate_number = models.CharField(max_length=30)
    max_numbers = models.IntegerField()
    specific = models.TextField(null=True)

    def __str__(self):
        return str(self.id)+' '+str(self.user_id)+' '+str(self.vehicle_tid)+' '+str(self.license_plate_number)+' '+str(self.max_numbers)+' '+str(self.specific)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.IntegerField()
    boarding = models.CharField(max_length=100) #where to board the car
    destination = models.CharField(max_length=100)
    arrival_time = models.DateTimeField()
    psnumbers = models.IntegerField()
    vehicle_tid = models.IntegerField(null=True)
    specific = models.TextField(null=True)
    canshare = models.BooleanField()
    status = models.IntegerField() #-1 canceled; 0 open; 1 confirmed; 2 completed
    driver_id = models.IntegerField(null=True)
    request_time = models.DateTimeField(auto_now_add=True)
    comfirmed_time = models.DateTimeField(null=True)
    complete_time = models.DateTimeField(null=True)

    def __str__(self):
        return 'Boarding: '+self.boarding+'\nDestination: '+self.destination

class Shared(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.IntegerField()
    user_id = models.IntegerField()
    join_time = models.DateTimeField(auto_now_add=True)
    party_number = models.IntegerField()

    def __str__(self):
        return str(self.id)+' '+str(self.request_id)+' '+str(self.user_id)+' '+str(self.join_time)+' '+str(self.party_number)

class Vehicle_Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50) #vehicle type: small car...

    def __str__(self):
        return str(self.id)+' '+str(self.type)