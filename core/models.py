from django.db import models
import datetime
from django.db.models import DateTimeField, FloatField

class CompositeDateTimeField(DateTimeField):
    def get_prep_value(self, value):
        return value

class CompositeFloatField(FloatField):
    def get_prep_value(self, value):
        return value

class DataModel(models.Model):
    class Meta:
        ordering = ('-opening_time',)
        constraints = [
            models.UniqueConstraint(
                fields=['opening_time', 'profit'],
                name='composite_pk',
            ),
        ]

    opening_time = CompositeDateTimeField(primary_key=True)
    type = models.CharField(max_length=100)
    volume = models.FloatField(null=True)
    symbol = models.CharField(max_length=100, null=True)
    opening_price = models.FloatField(null=True)
    volumn_spent = models.FloatField(null=True)
    closing_time = CompositeDateTimeField(null=True)
    price = models.FloatField(null=True)
    profit = CompositeFloatField(null=True)

    def __str__(self):
        return f"{self.opening_time} | {self.symbol} | {self.type}"

    def save(self, *args, **kwargs):
        # Sort the data in ascending order of opening_time before saving
        if not self.pk:  # Only perform sorting if it's a new object
            DataModel.objects.filter(opening_time__gte=self.opening_time).update(opening_time=models.F('opening_time') + datetime.timedelta(microseconds=1))
        super().save(*args, **kwargs)
