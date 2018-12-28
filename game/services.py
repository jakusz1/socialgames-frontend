import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pytrends.request import TrendReq
import pytrends.exceptions
from faker import Faker

from game.models import Round, Lang, Game, Step
from socialgames.settings import GAME_SETTINGS


def send(uri, command, data, only_screen=False, only_controllers=False):
    channel_layer = get_channel_layer()
    if not only_controllers:
        async_to_sync(channel_layer.group_send)(uri, {"type": "broadcast",
                                                      "response": {
                                                          "command": command,
                                                          "data": data
                                                      }})
    if not only_screen:
        async_to_sync(channel_layer.group_send)(uri + GAME_SETTINGS['controller_postfix'],
                                                {"type": "broadcast",
                                                 "response": {
                                                     "command": command,
                                                     "data": data
                                                 }})


def start_game(game, *args):
    if not args:
        print(Lang[game.lang].value)
        faker = Faker('en_US')
        args = faker.words(nb=3, ext_word_list=None)

    for arg in args:
        print(arg)
        Round.objects.create(game=game, text=arg)

    game.step = Step.IDL.name
    game.save()


def check_if_last_answer(game_round):
    return game_round.game.players.count() == game_round.answers.count()


def send_question(game):
    game_round = game.rounds.filter(done=False).first()
    if game_round:
        send(game.uri, 'new_round', game_round.to_json())
        game_round.done = True
        game_round.game.step = Step.ANS.name
        game_round.save()
        return True
    return False


def get_points(game):
    game_round = game.rounds.filter(done=True).first()
    if game_round:
        game.step = Step.IDL.name
        game.save()
        pytrends = TrendReq(hl=game.lang, tz=0)
        answers_checklist = []
        players_list = []
        answers = game_round.answers.all()
        for answer in answers:
            answers_checklist.append(answer.text)
            players_list.append(answer.player)
        try:
            pytrends.build_payload(answers_checklist, cat=0, timeframe='today 3-m', geo=game.lang, gprop='')
            scrapped_df = pytrends.interest_over_time()
        except:
            send(game.uri, "results_graph", "{}",
                 only_screen=True)
            send(game.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)
            game_round.delete()
            return False

        if scrapped_df.size != 0:
            scrapped_df = scrapped_df.drop(columns='isPartial')

            scores = scrapped_df.iloc[-1]
            for i in range(len(scores)):
                players_list[i].score += scores[i]
                players_list[i].save()
                answer = answers[i]
                answer.score = int(scores[i])
                answer.save()

            print(json.dumps([answer.to_json() for answer in answers]))
            send(game.uri, "results_graph", '{' + scrapped_df.to_json(orient="split")[1:-1] + '}',
                 only_screen=True)
            send(game.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)

            game_round.delete()
            return True

        else:
            send(game.uri, "results_graph", "{}",
                 only_screen=True)
            send(game.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)
            game_round.delete()
            return False

    game.delete()
    return False
