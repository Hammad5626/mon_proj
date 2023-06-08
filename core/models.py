from django.db import models
from datetime import timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserModel(models.Model):
    name = models.CharField(max_length=128)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class DataModel(models.Model):
    class Meta:
        ordering = ('-opening_time',)
        
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    opening_time = models.DateTimeField()
    type = models.CharField(max_length=100)
    volume = models.FloatField(null=True)
    symbol = models.CharField(max_length=100, null=True)
    opening_price = models.FloatField(null=True)
    volumn_spent = models.FloatField(null=True)
    closing_time = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    profit = models.FloatField(null=True)

    def __str__(self):
        return f"{self.opening_time} | {self.symbol} | {self.type}"

@receiver(pre_save, sender=DataModel)
def create_new_entry(sender, instance, **kwargs):
    existing_entry = DataModel.objects.filter(
        user=instance.user,
        opening_time=instance.opening_time,
        profit=instance.profit
    ).exists()

    if existing_entry:
        # If an entry already exists, create a new instance with an incremented opening_time
        instance.opening_time += timedelta(microseconds=1)
        instance.pk = None  # Clear the primary key to force