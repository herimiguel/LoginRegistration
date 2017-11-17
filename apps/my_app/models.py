from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_name = models.CharField(max_length=100, unique =True)
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

