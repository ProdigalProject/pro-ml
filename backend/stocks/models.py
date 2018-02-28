from django.db import models

# Create your models here.
class Stock(models.Model): 
    name = models.CharField(max_length=50) 
    ticker = models.CharField(max_length=50) 
    high = models.FloatField(blank=True, null=True) 
    low = models.FloatField(blank=True, null=True) 
    opening = models.FloatField(blank=True, null=True) 
    closing = models.FloatField(blank=True, null=True) 
    volume = models.IntegerField(blank=True, null=True) 
    date = models.DateField(blank=True, null=True) 
