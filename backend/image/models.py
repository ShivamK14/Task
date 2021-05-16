from django.db import models

from django.db import models


# Create your models here.

class InputImage(models.Model):
    image = models.ImageField(blank=False, null=False, upload_to='post_images')
    xml = models.FileField(blank=False, null=False, upload_to='post_images')


class OutputImage(models.Model):
    image_name = models.CharField(max_length=100)

    coordinates = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

