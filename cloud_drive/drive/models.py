from django.db import models
from django.db import models
from django.contrib.auth.models import User

class UserStorage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_space = models.IntegerField(default=100 * 1024 * 1024)  # 100 MB en octets
    used_space = models.IntegerField(default=0)  # Espace utilisé en octets

    def __str__(self):
        return f"{self.user.username} - {self.used_space} / {self.total_space}"

# Create your models here.
