from django.contrib.auth.models import User
from django.db import models


# extended User model with additional info
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    last_activity = models.DateTimeField(null=True, blank=True)  # filled in by middleware

    def __str__(self):
        return self.user.username
