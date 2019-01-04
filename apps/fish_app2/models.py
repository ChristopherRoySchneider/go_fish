from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.login_app.models import User

class Game(models.Model):
    game_over = models.BooleanField()
    deck = models.TextField(null=True)
    player_index = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(3)])
    books = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Player(models.Model):
    position = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(3)])
    game = models.ForeignKey(Game, related_name = 'players')
    user = models.ForeignKey(User)
    hand = models.TextField(default = "'[]'")
    books = models.TextField(default = "'[]'")



