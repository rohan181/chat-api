from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    reply = models.TextField( null=True)
    api = models.TextField( null=True)
