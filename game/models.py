from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    US = "en_US"
    PL = "pl_PL"


class Step(ChoiceEnum):
    PRE = "not_started"
    IDL = "started_not_answering"
    ANS = "started_answering"


# User = get_user_model()


# def deserialize_player(player):
#     """Deserialize user instance to JSON"""
#     if player:
#         return {"id": player.user.id, "username": player.user.username, "score": player.score}
#     return {}


def _generate_unique_uri():
    """Generates a unique uri for the game session"""
    all_chars = string.ascii_lowercase
    return "".join(random.choice(all_chars) for _ in range(GAME_SETTINGS["code_length"]))


class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    uri = models.CharField(max_length=GAME_SETTINGS["code_length"],
                           default=_generate_unique_uri)
    lang = models.CharField(max_length=2,
                            choices=Lang.choices(),
                            default=Lang.PL.name)
    step = models.CharField(max_length=3,
                            choices=Step.choices(),
                            default=Step.PRE.name)

    def to_json(self):
        return {"id": self.id,
                "lang": self.lang,
                "step": self.step,
                "players": [player.to_json()
                            for player in self.players.all()],
                "rounds": self.rounds.count()}


class GamePlayer(models.Model):
    game = models.ForeignKey(
        Game, related_name="players", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def to_json(self):
        return {"id": self.id,
                "username": self.user.username,
                "email": self.user.email,
                "score": self.score,
                "total_score": self.user.userstats.total_score,
                "total_won": self.user.userstats.total_won}


class Round(models.Model):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    text = models.TextField(max_length=50)
    done = models.BooleanField(default=False)

    def to_json(self):
        return {"id": self.id, "text": self.text, "done": self.done}


class Answer(models.Model):
    player = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
    game_round = models.ForeignKey(Round, related_name="answers", on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    score = models.IntegerField(default=0)

    def to_json(self):
        return {"username": self.player.user.username,
                "id": self.id,
                "text": self.text,
                "score": self.score}


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_won = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    instance.userstats.save()
