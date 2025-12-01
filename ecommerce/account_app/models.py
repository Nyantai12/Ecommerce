from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(null=False)
    pro_image = models.ImageField(upload_to='photos/accounts', blank=True)

    def __str__(self):
        return self.user.email
    