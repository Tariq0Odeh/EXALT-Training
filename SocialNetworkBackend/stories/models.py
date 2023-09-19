from datetime import timedelta, datetime
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL




class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(default=datetime.now() +
                                           timedelta(hours=24))

    def __str__(self):
        return f"{self.user.name} Story ({self.id})"
