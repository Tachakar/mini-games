from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    text = models.CharField(max_length = 5, unique=True)

    def __str__(self):
        return f"{self.text}"

class Game(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    winning_word = models.CharField(max_length = 5)
    guesses = models.JSONField(default=list)
    statuses = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game_over = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

    def __str__(self):
        return f"Game {self.id} - {self.winning_word} ({'Finished' if self.game_over else 'Active'})"
    class Meta:
        ordering = ['-created_at']
    @property
    def guess_count(self):
        return len([g for g in self.guesses if g != '     '])
