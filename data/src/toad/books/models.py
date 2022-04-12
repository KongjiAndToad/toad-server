from django.db import models
from users.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=45)
    content = models.TextField()
    audio = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book', null=True, blank=True)
    liked_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', null=True, blank=True)

    class Meta:
        db_table = "books"

