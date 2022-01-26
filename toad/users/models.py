from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length = 45, unique = False)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=100)
    class Meta:
        db_table = "users"