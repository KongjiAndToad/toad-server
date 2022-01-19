from django.db import models
from toad.user.models import User
from toad.book.models import Book

class Like(models.Model):
    book_num = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_num = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Like"
