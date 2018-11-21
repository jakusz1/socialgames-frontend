from django.contrib.auth import get_user_model

from socialgames.settings import GAME_SETTINGS
from .models import GameSession, GameSessionPlayer, deserialize_player, GameSessionTask, \
    GameSessionAnswer, GameSessionChoice, GameType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

import game.services as services


class GameStartView(APIView):
    def patch(self, request, *args, **kwargs):
        User = get_user_model()

        uri = kwargs['uri']
        username = request.data['username']
        user = User.objects.get(username=username)
        game_session = GameSession.objects.get(uri=uri)
        player = game_session.players.filter(user=user, game_session=game_session)
        if game_session.started or not player.exists():
            return Response({
                'status': 'ERROR',
                'message': 'Game was already started'
            })
        else:
            services.start_game(game_session)
        services.send(uri, 'start_game', game_session.to_json())
        return Response({
            'status': 'SUCCESS',
            'message': '%s started game' % user.username,
            'game': game_session.to_json()
        })


class GameSessionView(APIView):
    """Manage Game sessions."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """create a new Game session."""
        user = request.user
        game_type = request.data['game_type']

        if game_type == 'tre':
            game_session = GameSession.objects.create(owner=user, game_type=GameType.TRE)
            GameSessionPlayer.objects.create(user=user, game_session=game_session)

            return Response({
                'status': 'SUCCESS', 'uri': game_session.uri,
                'message': 'New game session created'
            })

        return Response({
            'status': 'ERROR',
            'message': 'Game_type is not recognized'
        })

    def patch(self, request, *args, **kwargs):
        """Add a player to a game session."""
        User = get_user_model()

        uri = kwargs['uri']
        username = request.data['username']
        user = User.objects.get(username=username)
        game_session = GameSession.objects.get(uri=uri)
        player = game_session.players.filter(user=user, game_session=game_session)
        if game_session.started and not player.exists():
            return Response({
                'status': 'ERROR',
                'message': 'Game was already started'
            })
        else:
            game_session.players.get_or_create(user=user, game_session=game_session)
        services.send(uri, 'new_player_joined', game_session.to_json(), only_screen=True)
        return Response({
            'status': 'SUCCESS',
            'message': '%s joined game' % user.username,
            'game': game_session.to_json()
        })


class GameSessionTaskView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game_session = GameSession.objects.get(uri=kwargs['uri'])
        tasks = [game_session_task.to_json()
                 for game_session_task in game_session.tasks.all()]

        return Response({'uri': game_session.uri, 'tasks': tasks})

    def post(self, request, *args, **kwargs):
        text = request.data['text']
        user = request.user
        game_session = GameSession.objects.get(uri=kwargs['uri'])
        player = GameSessionPlayer.objects.filter(user=user, game_session=game_session).first()

        GameSessionTask.objects.create(player=player, game_session=game_session, text=text)

        return Response({'status': 'SUCCESS'})


class GameSessionFirstTaskView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game_session = GameSession.objects.get(uri=kwargs['uri'])
        game_session_task = game_session.tasks.filter(done=False).first()
        if game_session_task:
            services.send(kwargs['uri'], 'new_trends_word', {'id': game_session_task.id, 'word': game_session_task.text}, only_controllers=True)
            game_session_task.done = True
            game_session_task.save()
            return Response(game_session_task.to_json())

        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        game_session = GameSession.objects.get(uri=kwargs['uri'])
        services.get_points(game_session)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GameSessionAnswerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game_session_task = GameSessionTask.objects.get(id=kwargs['task_id'])
        answers = [game_session_answer.to_json()
                   for game_session_answer in game_session_task.answers.all()]

        return Response({'id': game_session_task.id, 'answers': answers})

    def post(self, request, *args, **kwargs):
        text = request.data['text']
        answer_type = request.data['type']
        user = request.user
        game_session_task = GameSessionTask.objects.get(id=kwargs['task_id'])
        player = GameSessionPlayer.objects.filter(user=user, game_session=game_session_task.game_session).first()
        print("post")
        GameSessionAnswer.objects.create(player=player, game_task=game_session_task, text=text, type=answer_type)
        if services.check_if_last_answer(game_session_task):
            services.send(game_session_task.game_session.uri, "all_answers", {}, only_screen=True)
        return Response({'status': 'SUCCESS'})


class GameSessionChoiceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game_session_task = GameSessionTask.objects.get(id=kwargs['task_id'])
        choices = [game_session_choice.to_json()
                   for game_session_choice in game_session_task.choices.all()]

        return Response({'id': game_session_task.id, 'choices': choices})

    def post(self, request, *args, **kwargs):
        answer_id = request.data['answer_id']
        user = request.user
        game_session_task = GameSessionTask.objects.get(id=kwargs['task_id'])
        game_session_answer = GameSessionAnswer.objects.get(id=answer_id)
        player = GameSessionPlayer.objects.filter(user=user, game_session=game_session_task.game_session).first()

        GameSessionChoice.objects.create(player=player, game_task=game_session_task, choice=game_session_answer)

        return Response({'status': 'SUCCESS'})
