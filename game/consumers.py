from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from game.models import GameSession
import game.services as services
from socialgames.settings import GAME_SETTINGS


class GameSessionConsumer(JsonWebsocketConsumer):

    def connect(self):
        # if self.scope["user"].is_anonymous:
        #     self.close()

        # if not self.__auth_game():
        #     self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.__get_uri(),
            self.channel_name
        )
        self.accept()

    def receive_json(self, content, **kwargs):
        uri = self.__get_uri()

        command = content.get("command", None)
        content['user'] = self.scope['user']
        content['game'] = GameSession.objects.get(uri=uri)
        method = getattr(self, command, self.wrong_command)
        method(content)

    def message(self, content):
        self.send_response({
            "user": self.scope["user"].username,
            "message": content['message']
        })

    def wrong_command(self, content):
        self.send_response({
            "error": "Command not supported"
        })

    def start_game(self, content):
        services.start_game(content['game'])

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.__get_uri(),
            self.channel_name,
        )
        self.send_json({
            "command": "disconnect",
            "response": "disconnected"
        })

    def send_response(self, response, broadcast=True):
        if broadcast:
            async_to_sync(self.channel_layer.group_send)(
                self.__get_uri(),
                {
                    "type": "broadcast",
                    "response": response
                })
        else:
            self.send_json(response)

    def broadcast(self, content):
        self.send_json(content["response"])

    def __auth_game(self):
        return GameSession.objects.filter(uri=self.scope["url_route"]["kwargs"]["uri"]).exists()

    def __get_uri(self):
        if self.scope["url_route"]["kwargs"]["device_type"] == "games":
            return self.scope["url_route"]["kwargs"]["uri"]
        else:
            return self.scope["url_route"]["kwargs"]["uri"] + GAME_SETTINGS['controller_postfix']
