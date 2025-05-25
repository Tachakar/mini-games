from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.db import connection
from ...models import Word

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE wordle_word_id_seq RESTART WITH 1;")
            Word.objects.all().delete()
        except:
            raise CommandError("Something went wrong.")


