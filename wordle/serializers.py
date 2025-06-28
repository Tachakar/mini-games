from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'winning_word', 'guesses', 'game_over', 'won', 'guess_count']
        read_only_fields = ['winning_word']
