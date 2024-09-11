from django.db import models
import uuid

# Create your models here.
class Flight_schedule(models.Model):
    flight_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default=False)  #flase means not take off

    def __str__(self):
        return f"Flight {self.flight_id} to {self.location}"+"test"


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    flight_id = models.ForeignKey(Flight_schedule, on_delete=models.CASCADE) #foreign key to flight_schedule
    #date and time calculate when user subscribe
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default=False)  #False mean not send email yet

    def __str__(self):
        return "subscription id: " + str(self.subscription_id) + " email: " + self.email + " flight id: " + str(self.flight_id)


class Query(models.Model):
    query_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    query = models.TextField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    status = models.BooleanField(default=False)  #False mean not reply or ignore yet

    def __str__(self):
        return "query id: " + str(self.query_id) + " email" + self.email + " query: " + self.query
