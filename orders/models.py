from django.db import models
import datetime

class Order(models.Model):
	member_id = models.IntegerField()
	stock_name = models.TextField()
	quantity = models.IntegerField()
	owned = models.IntegerField()
	stock_id = models.IntegerField()
	purchase_price = models.FloatField()
	buy = models.BooleanField()
	date = models.DateField(default=datetime.date.today)
	
