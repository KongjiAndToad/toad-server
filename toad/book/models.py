from django.db import models
from toad.user.models import User

class Book(models.Model):
    title = models.CharField(max_length=45)
    content = models.TextField()
    audio = models.CharField(max_length=200)
    bookmark = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book')
    liked_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "Book"


