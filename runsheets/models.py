from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from users.models import User
# from django.contrib.auth.models import User
ROLE_CHOICES = (
        ('normal', 'Normal'),
       
        ('special', 'Special'),


    )
class Passenger(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Passenger Name",max_length=255)
    adress= models.CharField(max_length=255,blank=True, null=True)
    Passenger_type=models.CharField(max_length=150, choices=ROLE_CHOICES, default='Normal')
    organization_name= models.CharField(max_length=255,blank=True, null=True)
    invoice_number = models.CharField(max_length=255,blank=True, null=True)
    driver_invoice_number= models.CharField(max_length=255,blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name
class ShiftTime(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
    


# class Runsheet1(models.Model):
#     passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
#     # shift_name = models.CharField(max_length=255)
#     Morning_price = models.DecimalField(max_digits=8, decimal_places=2)
#     Evening_price = models.DecimalField(max_digits=8, decimal_places=2)
#     driver = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Runsheet1: {self.passenger_name} - {self.date_created}"
    



# from django.db import models
# from django.contrib.auth.models import User

class Runsheet1(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Runsheet1: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet1"
        verbose_name_plural = "Runsheet1"



class Runsheet2(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet2: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet2"
        verbose_name_plural = "Runsheet2"
class Runsheet3(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet3: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet3"
        verbose_name_plural = "Runsheet3"
class Runsheet4(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet4: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet4"
        verbose_name_plural = "Runsheet4"

class Runsheet5(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet5: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet5"
        verbose_name_plural = "Runsheet5"




class Runsheet6(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet6: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet6"
        verbose_name_plural = "Runsheet6"

class Runsheet7(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet7: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet7"
        verbose_name_plural = "Runsheet7"
class Runsheet8(models.Model):
    passenger_name = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # shift_name = models.CharField(max_length=255)
    Morning_price = models.DecimalField(max_digits=8,blank=True, null=True, decimal_places=2)
    Evening_price = models.DecimalField(max_digits=8, blank=True, null=True,decimal_places=2)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Runsheet8: {self.passenger_name} - {self.date_created}"

    class Meta:
        # Add any other meta options if needed
        verbose_name = "Runsheet8"
        verbose_name_plural = "Runsheet8"
# class Runsheet1Proxy(Runsheet1):
#     class Meta:
#         proxy = True
#         verbose_name = "Assign Passengers runsheet 1"
#         verbose_name_plural = "Assign Passengers runsheet 1"

#     def custom_method(self):
#         # Add any custom methods or overrides here
#         pass





##########################################

class AssignPassengerToRunsheet1(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 1"
        verbose_name_plural = "Assign Passengers to Runsheet 1"


class AssignPassengerToRunsheet2(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 2"
        verbose_name_plural = "Assign Passengers to Runsheet 2"

class AssignPassengerToRunsheet3(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 3"
        verbose_name_plural = "Assign Passengers to Runsheet 3"



class AssignPassengerToRunsheet4(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 4"
        verbose_name_plural = "Assign Passengers to Runsheet 4"


class AssignPassengerToRunsheet5(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 5"
        verbose_name_plural = "Assign Passengers to Runsheet 5"

class AssignPassengerToRunsheet6(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 6"
        verbose_name_plural = "Assign Passengers to Runsheet 6"
class AssignPassengerToRunsheet7(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 7"
        verbose_name_plural = "Assign Passengers to Runsheet 7"


class AssignPassengerToRunsheet8(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Driver")
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.passenger.name}"

    class Meta:
        verbose_name = "Assign Passenger to Runsheet 8"
        verbose_name_plural = "Assign Passengers to Runsheet 8"

















































































class HelpAndDispute(models.Model):
    complaint = models.TextField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"HelpAndDispute - Driver: {self.driver} - Complaint ID: {self.pk}"