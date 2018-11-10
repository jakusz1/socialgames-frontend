from django.contrib import admin
from .models import GameSessionPlayer, GameSessionAnswer, GameSessionChoice, \
    GameSessionTask, GameSession

# Register your models here.
admin.site.register(GameSession)
admin.site.register(GameSessionPlayer)
admin.site.register(GameSessionAnswer)
admin.site.register(GameSessionChoice)
admin.site.register(GameSessionTask)
