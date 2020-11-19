from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
	member = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	nick = models.TextField()
	email = models.EmailField(default='non@non.non')
	money = models.FloatField(default=20000)
