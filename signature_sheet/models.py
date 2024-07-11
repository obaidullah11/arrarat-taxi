from django.db import models
from users.models import User
from runsheets.models import Passenger
from django.utils import timezone

class signature_sheet1(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    signature = models.ImageField(upload_to='signature_sheet_images/')  # Add the image field

    def __str__(self):
        return f"signature_sheet1: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "signature_sheet1"
        verbose_name_plural = "signature_sheet1"



class AssignPassengerTosignature_sheet1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to signature_sheet1"
        verbose_name_plural = "Assign Passengers to signature_sheet1"
from django.db import models

class SignatureReceipt(models.Model):
    Driver = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Driver")
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    account_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    trip_explanation = models.CharField(max_length=255)
    start_point = models.CharField(max_length=255)
    drop_point = models.CharField(max_length=255)
    taxi_no = models.CharField(max_length=255)
    dc_no = models.CharField(max_length=255)
    passenger_name = models.CharField(max_length=255)
    fare_meter = models.DecimalField(max_digits=10, decimal_places=2)
    extras = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Image field is now optional

    def __str__(self):
        return f'Taxi Receipt for {self.passenger_name} on {self.date}'
