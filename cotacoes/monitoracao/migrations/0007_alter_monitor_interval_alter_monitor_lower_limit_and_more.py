# Generated by Django 4.2.6 on 2023-10-16 22:19

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoracao', '0006_alter_monitor_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='interval',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='lower_limit',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='upper_limit',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]