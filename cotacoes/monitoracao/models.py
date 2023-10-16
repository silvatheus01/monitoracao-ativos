from decimal import Decimal
import json

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .api.sheets import Spreadsheet
from django.core.validators import MinValueValidator


class Asset(models.Model):
    name = models.CharField(max_length=10, unique=True)
    row = models.IntegerField(blank=False, editable=False)

    def save(self, *args, **kwargs):
        sheet = Spreadsheet()
        try:
            self.row = sheet.find_row(self.name)
        except ValueError:
            raise ValueError("Não é possível monitorar esse ativo. Tente outro!")
        
        super(Asset, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class Monitor(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    interval = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    task = models.OneToOneField(PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL)
    upper_limit = models.DecimalField(decimal_places = 2, max_digits=4, validators=[MinValueValidator(Decimal('0'))])
    lower_limit = models.DecimalField(decimal_places = 2, max_digits=4, validators=[MinValueValidator(Decimal('0'))]) 
    active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.task.interval.delete()
        self.task.delete()
        super(Monitor, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        
        if self.task is not None:
            self.task.interval.delete()
            self.task.delete()

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.interval,
            period=IntervalSchedule.SECONDS, 
        )
            
        task = PeriodicTask.objects.create(
            interval=schedule,
            name=f"Monitor: {self.asset.name}",
            task="monitoracao.tasks.save_quote_monitoring",
            kwargs=json.dumps(
                {
                    "row": self.asset.row,
                    "name": self.asset.name
                }
            ),
        )

        task.enabled = self.active
        task.save()
        self.task = task

        super(Monitor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.asset}'


class Quotation(models.Model):
    asset = models.ForeignKey(Asset,  on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places = 2, max_digits=4)
    recording_date = models.DateTimeField()
    trade_date = models.DateTimeField()

    def __str__(self):
        return f'Ativo: {self.asset.name} | Preço: R${self.price}'

    