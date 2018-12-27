import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pytrends.request import TrendReq
import pytrends.exceptions
from faker import Faker

from game.models import GameSessionTask, deserialize_player, Lang, GameSession, GameType
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


def start_game(game_session, *args):
    if not args:
        faker = Faker("pl_PL" if game_session.lang == "Lang.PL" else "en_US")
        args = faker.words(nb=3, ext_word_list=None)

    for arg in args:
        GameSessionTask.objects.create(game_session=game_session, text=arg)

    game_session.started = True
    game_session.save()
    # send_question(game_session)


def check_if_last_answer(game_task):
    if game_task.game_session.game_type == "GameType.TRE":
        return game_task.game_session.players.count() == game_task.answers.count()
    else:  # TODO implement for more advanced games
        return False


def send_question(game_session):
    task = game_session.tasks.filter(done=False).first()
    if task:
        send(game_session.uri, 'new_task', task.to_json())
        task.done = True
        task.save()
        return True
    return False


def get_points(game_session):
    lang = "PL" if game_session.lang == "Lang.PL" else "US"
    pytrends = TrendReq(hl=lang, tz=0)
    task = game_session.tasks.filter(done=True).first()
    if task:
        answers_checklist = []
        players_list = []
        answers = task.answers.all()
        for answer in answers:
            answers_checklist.append(answer.text)
            players_list.append(answer.player)
        try:
            pytrends.build_payload(answers_checklist, cat=0, timeframe='today 3-m', geo=lang, gprop='')
            scrapped_df = pytrends.interest_over_time()
        except:
            send(game_session.uri, "results_graph", "{}",
                 only_screen=True)
            send(game_session.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)
            task.delete()
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
            send(game_session.uri, "results_graph", '{'+scrapped_df.to_json(orient="split")[1:-1]+'}',
                 only_screen=True)
            send(game_session.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)

            task.delete()
            return True

        else:
            send(game_session.uri, "results_graph", "{}",
                 only_screen=True)
            send(game_session.uri, "results_answers", json.dumps([answer.to_json() for answer in answers]),
                 only_screen=True)
            task.delete()
            return False

    game_session.delete()
    return False
