import os
import json
from typing import Optional
from model import *
from storage import Storage


SCHEMA_VERSION = 1
class JsonStorage(Storage):
    def __init__(self, path):
        self.path = path
        self.data = {
            'schema_version': SCHEMA_VERSION,
            'users': {},
            'groups': {},
            'players': {},
            'unconfirmed_games': {},
            'games': {},
        }
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, 'r') as f:
            self.data = json.load(f)
        assert self.data['schema_version'] == SCHEMA_VERSION

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.data['users'].get(user_id)
    
    def get_group(self, group_id: str) -> Optional[Group]:
        return self.data['groups'].get(group_id)
    
    def save_user(self, user: User) -> None:
        self.data['users'][user.id] = user
        self._save()
    
    def save_group(self, group: Group) -> None:
        self.data['groups'][group.id] = group
        self._save()
    
    def get_player(self, user_id: str, group_id: str) -> Optional[Player]:
        user = self.get_user(user_id)
        group = self.get_group(group_id)
        rating = self.data['players'].get((user_id, group_id))
        if user is None or group is None or rating is None:
            return None
        return Player(user=user, group=group, rating=rating)
    
    def save_player(self, player: Player) -> None:
        assert self.get_user(player.user_id) is not None
        assert self.get_group(player.group_id) is not None
        self.data['players'][(player.user_id, player.group_id)] = player.rating
        self._save()

    def next_confirmation_code(self) -> str:
        for _ in range(10):
            code = os.urandom(8).hex()
            if code not in self.data['unconfirmed_games']:
                return code
        raise Exception("Can't generate confirmation code")
    
    def next_game_id(self) -> str:
        return str(len(self.data['games']))
    
    def get_unconfirm_game_by_code(self, confirmation_code: str) -> Optional[UncomfirmedGame]:
        return self.data['unconfirmed_games'].get(confirmation_code)
    
    def save_unconfirm_game(self, game: UncomfirmedGame) -> None:
        self.data['unconfirmed_games'][game.confirmation_code] = game
        self._save()

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.data['games'].get(game_id)

    def save_game(self, game: Game) -> None:
        self.data['games'][game.id] = game
        self._save()
