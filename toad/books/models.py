from django.db import models
from users.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=45)
    content = models.TextField()
    audio = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book')
    liked_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        db_table = "books"