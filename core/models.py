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
    time = models.DateTimeField()
    type = models.CharField(max_length=100)
    volume = models.FloatField(null=True)
    symbol = models.CharField(max_length=100, null=True)
    opening_price = models.FloatField(null=True)
    volume_spent = models.FloatField(null=True)
    closing_time = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    commision = models.FloatField(null=True)
    swap = models.FloatField(null=True)
    profit = models.FloatField(null=True)
    net_profit = models.FloatField(null=True)

    def __str__(self):
        return f"{self.opening_time} | {self.symbol} | {self.type}"