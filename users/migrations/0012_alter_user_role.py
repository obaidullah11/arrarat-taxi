# Generated by Django 4.1.7 on 2023-07-13 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('Importer', 'Importer'), ('Dealer_admin', 'Dealer admin'), ('Dealer_sales', 'Dealer sales'), ('Dealer_work_reciever', 'Dealer work reciever'), ('Dealer_mechanic', 'Dealer mechanic'), ('Vehicle_owner', 'Vehicle owner')], default='Vehicle_owner', max_length=150),
        ),
    ]
