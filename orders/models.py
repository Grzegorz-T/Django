from django.db import models
from members.models import Member
from stocks.models import Stocks

class Order(models.Model):
	member = models.ForeignKey(Member, null=True, on_delete= models.SET_NULL)
	stock = models.ForeignKey(Stocks, null=True, on_delete= models.SET_NULL)
	quantity = models.IntegerField()
	owned = models.IntegerField()
	purchase_price = models.FloatField()
	buy = models.BooleanField()
	date = models.DateField(auto_now_add=True)

