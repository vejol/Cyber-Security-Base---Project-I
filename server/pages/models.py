from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.IntegerField()

class Event(models.Model):
	sender = models.TextField()
	receiver = models.TextField()
	amount = models.IntegerField()
	message = models.TextField()