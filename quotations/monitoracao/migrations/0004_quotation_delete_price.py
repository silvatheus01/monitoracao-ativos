# Generated by Django 4.2.6 on 2023-10-15 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoracao', '0003_rename_price_price_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('recording_date', models.DateTimeField()),
                ('trade_date', models.DateTimeField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoracao.asset')),
            ],
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
