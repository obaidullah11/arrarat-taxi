# Generated by Django 4.1.7 on 2023-07-07 16:38

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', users.models.MyUserManager()),
            ],
        ),
    ]
