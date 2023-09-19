from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user',
                                on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.id} - {self.from_user.name}({self.from_user.id})"
                f" send request to {self.to_user.name}({self.to_user.id})")
