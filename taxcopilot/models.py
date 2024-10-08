from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    public_id = models.CharField(max_length=255, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)
