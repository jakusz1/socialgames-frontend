from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pytrends.request import TrendReq

from socialgames.settings import GAME_SETTINGS

import string
import random

from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class Lang(ChoiceEnum):
    EN = "en_US"
    PL = "pl_PL"


class GameType(ChoiceEnum):
    TRE = "Trends"


User = get_user_model()


def deserialize_player(player):
    """Deserialize user instance to JSON"""
    if player:
        return {"id": player.user.id, "username": player.user.username, "score": player.score}
    return {}


def _generate_unique_uri():
    """Generates a unique uri for the game session"""
    all_chars = string.ascii_lowercase
    return "".join(random.choice(all_chars) for _ in range(settings.GAME_SETTINGS["code_length"]))


class GameSession(models.Model):
    """A Game Session. The uri"s length is defined in GAME_SETTINGS"""

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.TextField(default=_generate_unique_uri)
    game_type = models.CharField(max_length=3, choices=GameType.choices(), default=GameType.TRE)
    lang = models.CharField(max_length=2, choices=Lang.choices(), default=Lang.EN)
    started = models.BooleanField(default=False)

    def to_json(self):
        return {"id": self.id,
                "game_type": self.game_type,
                "lang": self.lang,
                "started": self.started,
                "players": [deserialize_player(player) for player in self.players.all()],
                "rounds": self.tasks.count()}


class GameSessionPlayer(models.Model):
    """Store all users in a game session."""

    game_session = models.ForeignKey(
        GameSession, related_name="players", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.IntegerField(default=0, null=False)

    def to_json(self):
        return {"id": self.id, "username": self.user.username, "score": self.score}


class GameSessionTask(models.Model):
    player = models.ForeignKey(GameSessionPlayer, on_delete=models.CASCADE, null=True)
    game_session = models.ForeignKey(GameSession, related_name="tasks", on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    done = models.BooleanField(default=False)

    def to_json(self):
        return {"id": self.id, "player": deserialize_player(self.player), "text": self.text, "done": self.done}


class GameSessionAnswer(models.Model):
    player = models.ForeignKey(GameSessionPlayer, on_delete=models.CASCADE)
    game_task = models.ForeignKey(GameSessionTask, related_name="answers", on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    type = models.TextField(max_length=10, default="text")

    def to_json(self):
        return {"username": self.player.user.username, "id": self.id, "type": self.type, "text": self.text}


class GameSessionChoice(models.Model):
    player = models.ForeignKey(GameSessionPlayer, on_delete=models.CASCADE)
    game_task = models.ForeignKey(
        GameSessionTask, related_name="choices", on_delete=models.CASCADE
    )
    choice = models.ForeignKey(GameSessionAnswer, on_delete=models.CASCADE)

    def to_json(self):
        return {"player": deserialize_player(self.player), "choice": self.game_task.to_json()}
