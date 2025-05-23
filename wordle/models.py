from django.db import models


class Word(models.Model):
    text = models.CharField(max_length = 5)

    def __str__(self):
        return f"{self.text}"
