from django.db import models
from user.models import User

# Create your models here.
class Book(models.Model):
    book_num = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=45)
    content = models.TextField()
    audio = models.CharField(max_length=200)
    bookmark = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book')
    liked_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Book"
