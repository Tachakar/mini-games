from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.db import connection
from ...models import Word

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='wordle_word';")
            Word.objects.all().delete()
        except:
            raise CommandError("Something went wrong.")


