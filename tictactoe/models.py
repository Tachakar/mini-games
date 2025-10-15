from django.db import models

class Game(models.Model):
    user = models.CharField()
    won = models.BooleanField(default=False)
