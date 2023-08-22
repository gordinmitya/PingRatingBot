from abc import ABC, abstractmethod
from typing import Optional, Tuple

from storage import Storage
from elo_calculator import EloCalculator, EloInput, EloRatingChange
from model import *


class View(ABC):
    @abstractmethod
    def show_group_greeting(self, group: Group) -> None:
        pass

    @abstractmethod
    def show_player_greeting(self, player: Player) -> None:
        pass


class Controller:
    def __init__(self, storage: Storage, view: View):
        self.storage = storage
        self.calc = EloCalculator()

    def _register_if_necessary(self, group: Group, user: User) -> None:
        if self.storage.get_group(group.id) is None:
            self.storage.save_group(group)
            self.view.show_group_greeting(group)
        if self.storage.get_user(user.id) is None:
            self.storage.save_user(user)
        if self.storage.get_player(user.id, group.id) is None:
            player = Player(user.id, group.id, EloCalculator.INITIAL_RATING)
            self.storage.save_player(player)
            self.view.show_player_greeting(player)

    def new_game(self, group: Group, users: Tuple[User, User], score: Tuple[int, int]) -> None:
        assert len(user_ids) == 2
        assert len(score) == 2
        group = self.storage.get_group(group_id)
        assert group is not None
        player1, player2 = (self.storage.get_player(group_id, user_id) for user_id in user_ids)
        

        players = (self.storage.get_player(group_id, user_id) for user_id in user_ids)
        
