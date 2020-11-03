from django.db import models

class Stocks(models.Model):
    name = models.TextField()
    price = models.FloatField()
    change = models.FloatField()
    perc = models.FloatField()
    opening = models.FloatField()
    max = models.FloatField()
    min = models.FloatField()

    