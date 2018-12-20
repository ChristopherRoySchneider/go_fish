from django.db import models
from apps.login_app.models import User
# Create your models here.

class QuoteManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['author']) <= 3:
            errors["author"] = "Author should be at least 4 characters"
        if len(postData['quote']) <= 10:
            errors["quote"] = "Quote should be at least 10 characters"
        return errors


class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    user = models.ForeignKey(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name = 'liked_quotes')
    objects = QuoteManager()
