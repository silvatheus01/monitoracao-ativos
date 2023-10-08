from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'

class Monitoring(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=0)
    monitor = models.BinaryField()
    upper_limit = models.DecimalField(decimal_places = 2, max_digits=4)
    lower_limit = models.DecimalField(decimal_places = 2, max_digits=4)

    def __str__(self):
        return f'{self.asset} f={self.frequency}min '

class Price(models.Model):
    asset = models.ForeignKey(Asset,  on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places = 2, max_digits=4)
    recording_date = models.DateTimeField()
    trade_date = models.DateTimeField()

    