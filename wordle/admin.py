from django.contrib import admin
from .models import Word, Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'winning_word', 'won', 'game_over', 'created_at']
    list_filter = ['game_over', 'won', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['session_key', 'winning_word', 'created_at']
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']
