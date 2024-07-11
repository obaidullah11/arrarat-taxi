from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, contact, password=None, password2=None, image=None):
        """
        Creates and saves a User with the given email, name, contact, password, and image.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact=contact,
        )

        if password:
            user.set_password(password)

        if image:
            # Generate a unique file name for the image
            file_name = f"{uuid.uuid4().hex}.{image.name.split('.')[-1]}"
            # Save the image to the default storage location
            default_storage.save(file_name, ContentFile(image.read()))
            user.image = file_name

        user.save(using=self._db)
        return user



























    def create_superuser(self, email, name,contact, password=None,password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            contact=contact,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),

        ('Driver', 'Driver'),


    )
    is_registered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    username=None
    role = models.CharField(max_length=150, choices=ROLE_CHOICES, default='Driver')
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField("Driver Name",max_length=200)
    contact = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact','name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        # Add any other meta options if needed
        verbose_name = "Driver"
        verbose_name_plural = "Driver"