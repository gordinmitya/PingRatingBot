from abc import ABC, abstractmethod
from typing import Optional
from model import *


class Storage(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_group(self, group_id: int) -> Optional[Group]:
        pass

    @abstractmethod
    def get_player(self, user_id: int, group_id: str) -> Optional[Player]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass

    @abstractmethod
    def save_group(self, group: Group) -> None:
        pass

    @abstractmethod
    def save_player(self, player: Player) -> None:
        pass

    @abstractmethod
    def next_confirmation_code(self) -> str:
        pass

    @abstractmethod
    def next_game_id(self) -> str:
        pass

    @abstractmethod
    def get_unconfirm_game_by_code(self, confirmation_code: str) -> Optional[UncomfirmedGame]:
        pass

    @abstractmethod
    def save_unconfirm_game(self, game: UncomfirmedGame) -> None:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Optional[Game]:
        pass

    @abstractmethod
    def save_game(self, game: Game) -> None:
        pass
