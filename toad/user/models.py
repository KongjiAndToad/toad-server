from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length = 45, unique = False)
    user_id = models.CharField(max_length=45, unique=True)
    class Meta:
        db_table = "User"