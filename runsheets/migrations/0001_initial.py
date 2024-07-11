# Generated by Django 4.1.7 on 2023-07-20 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('adress', models.CharField(blank=True, max_length=255, null=True)),
                ('Passenger_type', models.CharField(choices=[('normal', 'Normal'), ('special', 'Special')], default='Normal', max_length=150)),
                ('organization_name', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('driver_invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Runsheet1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Morning_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('Evening_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('passenger_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runsheets.passenger')),
            ],
        ),
    ]
