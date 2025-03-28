from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Accommodation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    type_accommodation=models.CharField(max_length=100)
    arrival_time=models.DateTimeField()
    stay_length = models.IntegerField()
    additional_information=models.CharField(max_length=500)
    def __str__(self):
        return self.user.username

class Food(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    type_food=models.CharField(max_length=100)
    pickup_time=models.DateTimeField()
    require_delivery = models.CharField(max_length=100)
    additional1_information=models.CharField(max_length=500)
    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=200)
    def __str__(self):
        return self.name