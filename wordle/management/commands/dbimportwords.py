from django.core.management.base import BaseCommand, CommandError
from ...models import Word

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with open("words.txt") as file:
                words = []
                for line in file:
                    current_line = str(line.split()[0])
                    new_word = Word(text = current_line)
                    words.append(new_word)
                Word.objects.bulk_create(words)
        except FileNotFoundError:
            raise CommandError("File was not found.")
        except:
            raise CommandError("Something went wrong.")



