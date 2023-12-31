# Generated by Django 4.2.6 on 2023-10-14 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('recording_date', models.DateTimeField()),
                ('trade_date', models.DateTimeField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoracao.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField()),
                ('active', models.BinaryField()),
                ('upper_limit', models.DecimalField(decimal_places=2, max_digits=4)),
                ('lower_limit', models.DecimalField(decimal_places=2, max_digits=4)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoracao.asset')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask')),
            ],
        ),
    ]
