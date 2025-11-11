from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.PositiveIntegerField(null=False)
    pro_image = models.ImageField(upload_to='photos/accounts', null=True, blank=True)

    def __str__(self):
        return self.user_name