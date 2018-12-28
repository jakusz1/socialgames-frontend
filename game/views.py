from django.contrib.auth import get_user_model

from socialgames.settings import GAME_SETTINGS
from .models import Game, GamePlayer, Round, Answer, Step
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

import game.services as services


class GameStartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        uri = kwargs['uri']
        user = request.user
        game = Game.objects.get(uri=uri)
        player = game.players.filter(user=user, game=game)

        if game.step != "PRE" or not player.exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            services.start_game(game)

        services.send(uri, 'start_game', game.to_json())

        return Response({
            'status': 'SUCCESS',
            'message': '%s started game' % user.username
        })


class GameView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        game = Game.objects.create(owner=user)
        GamePlayer.objects.create(user=user, game=game)

        return Response({
            'status': 'SUCCESS', 'uri': game.uri,
            'message': 'New game created'
        })

    def patch(self, request, *args, **kwargs):
        uri = kwargs['uri']
        user = request.user
        game = Game.objects.get(uri=uri)
        player = game.players.filter(user=user, game=game)

        if game.step != "PRE" and not player.exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        game.players.get_or_create(user=user, game=game)
        services.send(uri, 'update_players_list', game.to_json())
        return Response({
            'status': 'SUCCESS',
            'message': '%s joined game' % user.username,
            'game': game.to_json()
        })

    def delete(self, request, *args, **kwargs):
        game = Game.objects.get(uri=kwargs['uri'])
        user = request.user

        if game.owner == user:
            winner = game.players.order_by("-score").first().to_json()
            final_players_list = game.players.order_by("-score").all().to_json()
            game.delete()
            return Response({'status': 'SUCCESS', 'winner': winner, 'players': final_players_list})

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AllRoundsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game = Game.objects.get(uri=kwargs['uri'])
        rounds = [game_round.to_json()
                  for game_round in game.rounds.all()]

        return Response({'uri': game.uri, 'rounds': rounds})


class FirstRoundView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game = Game.objects.get(uri=kwargs['uri'])
        first_round = game.rounds.filter(done=False).first()
        if first_round:
            game.step = Step.ANS.name
            game.save()
            services.send(kwargs['uri'], 'new_round',
                          {'id': first_round.id, 'word': first_round.text}, only_controllers=True)
            first_round.done = True
            first_round.save()
            return Response(first_round.to_json())

        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        game = Game.objects.get(uri=kwargs['uri'])
        services.get_points(game)

        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game_round = Round.objects.get(id=kwargs['round_id'])
        answers = [answer.to_json()
                   for answer in game_round.answers.all()]

        return Response({'id': game_round.id, 'answers': answers})

    def post(self, request, *args, **kwargs):
        text = request.data['text']
        user = request.user
        game_round = Round.objects.get(id=kwargs['round_id'])
        player = GamePlayer.objects.filter(user=user, game=game_round.game).first()
        Answer.objects.create(player=player, game_round=game_round, text=text)

        if services.check_if_last_answer(game_round):
            services.send(game_round.game.uri, 'all_answers', {}, only_screen=True)

        return Response({'status': 'SUCCESS'})
