from django.contrib import admin
from .models import GamePlayer, Answer, Round, Game

# Register your models here.
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(Answer)
admin.site.register(Round)
