from django.db import models


class Word(models.Model):
    text = models.CharField(max_length = 5)

    def __str__(self):
        return f"{self.text}"

class Game(models.Model):
    session_key = models.CharField(max_length = 40)
    status = models.CharField(max_length = 20)
    winning_word = models.CharField(max_length = 5)
    guesses = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game_over = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    def get_guess_count(self):
        return len([g for g in self.guesses if g != '     '])
    def is_won(self):
        return True if self.won else False

    def __str__(self):
        return f"Game {self.id} - {self.winning_word} ({'Finished' if self.game_over else 'Active'})"
    class Meta:
        ordering = ['-created_at']
        unique_together = ['session_key']
