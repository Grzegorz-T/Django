from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
	member = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.TextField()
	email = models.EmailField(default='non@non.non')
	money = models.FloatField(default=20000)
	capital = models.FloatField(default=20000)
	profit = models.FloatField(default=0)
	def __str__(self):
		return self.name
