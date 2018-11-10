from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pytrends.request import TrendReq
from faker import Faker

from game.models import GameSessionTask, deserialize_player, Lang, GameSession, GameType
from socialgames.settings import GAME_SETTINGS


def _send(uri, data, only_screen=False, only_controllers=False):
    channel_layer = get_channel_layer()
    if not only_controllers:
        async_to_sync(channel_layer.group_send)(uri, {"type": "broadcast", "response": data})
    if not only_screen:
        async_to_sync(channel_layer.group_send)(uri + GAME_SETTINGS['controller_postfix'],
                                                {"type": "broadcast", "response": data})


def start_game(game_session, *args):
    if not args:
        faker = Faker(game_session.lang.value)
        args = faker.words(nb=3, ext_word_list=None, unique=False)

    for arg in args:
        GameSessionTask.objects.create(game_session=game_session, text=arg)

    game_session.started = True
    game_session.save()
    send_question(game_session)


def check_if_last_answer(game_task):
    if game_task.game_session.game_type == GameType.TRE:
        return game_task.game_session.players.count() == game_task.answers.count()
    else:  # TODO implement for more advanced games
        return False


def send_question(game_session):
    task = game_session.tasks.filter(done=False).first()
    if task:
        _send(game_session.uri, task.to_json())
        task.done = True
        task.save()
        return True
    return False


def get_points(game_session):
    pytrends = TrendReq(hl='PL', tz=0)
    task = game_session.tasks.filter(done=True).first()
    if task:
        answers_checklist = []
        players_list = []
        for answer in task.answers:
            answers_checklist.append(answer.text)
            players_list.append(answer.player)

        pytrends.build_payload(answers_checklist, cat=0, timeframe='today 3-m', geo='PL', gprop='')
        scrapped_df = pytrends.interest_over_time().drop(columns='isPartial')
        scores = scrapped_df.iloc[-1]
        for i in range(len(scores)):
            players_list[i].score += scores[i]
            players_list[i].save()

        _send(game_session.uri, {'graph': scrapped_df.to_json(orient='records'),
                                 'players': [deserialize_player(p) for p in players_list]}, only_screen=True)
        task.delete()
        return True
    return False
