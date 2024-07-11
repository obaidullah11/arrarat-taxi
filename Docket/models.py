from django.db import models
from users.models import User
from runsheets.models import Passenger
from django.utils import timezone


class dockets(models.Model):
    Driver = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Driver")
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    account_name = models.CharField(max_length=255,null=True)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    trip_explanation = models.CharField(max_length=255,null=True)
    start_point = models.CharField(max_length=255)
    drop_point = models.CharField(max_length=255)
    taxi_no = models.CharField(max_length=255)
    dc_no = models.CharField(max_length=255)
    passenger_name = models.CharField(max_length=255)
    fare_meter = models.DecimalField(max_digits=10, decimal_places=2)
    extras = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Image field is now optional
    # repairing_id = models.CharField("Repairing ID", max_length=9, unique=True)
    docket_id = models.CharField("Docket ID", max_length=6, unique=True)

    def save(self, *args, **kwargs):
        if not self.docket_id:
            last_receipt = dockets.objects.order_by('-id').first()
            if last_receipt:
                last_id = int(last_receipt.docket_id)  # Extract the numeric part
                new_id = str(last_id + 1).zfill(6)  # Increment and format as 6 digits
            else:
                new_id = "100001"  # Initial ID
            self.docket_id = new_id
        super().save(*args, **kwargs)
    def __str__(self):
        return f'Taxi Receipt for {self.passenger_name} on {self.date}'
