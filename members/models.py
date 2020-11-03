from django.db import models

class Member(models.Model):
	nick = models.TextField()
	email = models.EmailField()
	date = models.DateField()
	money = models.FloatField(default=20000)
