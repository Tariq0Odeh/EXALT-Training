from django.db import models
from django.contrib.auth.models import AbstractUser, User
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    phone = PhoneField(blank=True, help_text='Contact phone number')
    address = models.CharField(max_length=300)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
