from decimal import Decimal
import json

from django.db import models
from django.forms import ValidationError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .api.sheets import Spreadsheet
from django.core.validators import MinValueValidator

class Asset(models.Model):
    name = models.CharField(max_length=10, unique=True,  verbose_name = "Ativo")
    row = models.IntegerField(blank=False, editable=False)

    def clean(self):
        sheet = Spreadsheet()
        try:
            self.row = sheet.find_row(self.name)
        except ValueError:
            raise ValidationError("Não é possível monitorar esse ativo. Tente outro!") 
    
    class Meta:
        verbose_name = "Ativo"

    def __str__(self):
        return f'{self.name}'

class Monitor(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, verbose_name = "Ativo")
    interval = models.IntegerField(blank=False, validators=[MinValueValidator(1)], verbose_name="Intervalo")
    task = models.OneToOneField(PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL)
    upper_limit = models.DecimalField(decimal_places = 2, max_digits=4, validators=[MinValueValidator(Decimal('0'))], verbose_name = "Limite superior")
    lower_limit = models.DecimalField(decimal_places = 2, max_digits=4, validators=[MinValueValidator(Decimal('0'))], verbose_name = "Limite inferior") 
    active = models.BooleanField(default=True, verbose_name = "Ativo")

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitores"

    def clean(self):
        upper_limit = self.upper_limit
        lower_limit = self.lower_limit

        if(upper_limit and lower_limit):
            if upper_limit < lower_limit:
                raise ValidationError("O limite superior deve ser maior do que o limite inferior.") 

    def delete(self, *args, **kwargs):
        delete_task(self)
        super(Monitor, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.task is not None:
            delete_task(self)

        task = create_task(self)
        self.task = task
        super(Monitor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.asset}'

class Quotation(models.Model):
    asset = models.ForeignKey(Asset,  on_delete=models.CASCADE, verbose_name = "Ativo")
    price = models.DecimalField(decimal_places = 2, max_digits=4, verbose_name = "Preço")
    recording_date = models.DateTimeField(verbose_name = "Momento do registro")
    trade_date = models.DateTimeField(verbose_name = "Horário da negociação")

    class Meta:
        verbose_name = "Cotação"
        verbose_name_plural = "Cotações"

    def __str__(self):
        return f'Ativo: {self.asset.name} | Preço: R${self.price}'
    
def delete_task(self):
    self.task.interval.delete()
    self.task.delete()

def create_task(self):
    schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.interval,
            period=IntervalSchedule.MINUTES, 
        )
            
    task = PeriodicTask.objects.create(
        interval=schedule,
        name=f"Monitor: {self.asset.name}",
        task="monitoracao.tasks.save_quote_monitoring",
        kwargs=json.dumps(
            {
                "row": self.asset.row,
                "asset_name": self.asset.name
            }
        ),
    )

    task.enabled = self.active
    task.save()
    return task
    