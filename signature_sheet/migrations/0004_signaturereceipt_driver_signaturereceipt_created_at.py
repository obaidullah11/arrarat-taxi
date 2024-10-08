# Generated by Django 4.1.7 on 2023-10-02 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("signature_sheet", "0003_signaturereceipt"),
    ]

    operations = [
        migrations.AddField(
            model_name="signaturereceipt",
            name="Driver",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Driver",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="signaturereceipt",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
