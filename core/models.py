from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=128)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class DataModel(models.Model):
    class Meta:
        ordering = ('time',)
        
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    time = models.DateTimeField(primary_key=True)
    type = models.CharField(max_length=100)
    volume = models.FloatField(null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    opening_price = models.FloatField(null=True, blank=True)
    volume_spent = models.FloatField(null=True, blank=True)
    closing_time = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    commision = models.FloatField(null=True, blank=True)
    swap = models.FloatField(null=True, blank=True)
    profit = models.FloatField(null=True, blank=True)
    net_profit = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.time} | {self.symbol} | {self.type}"