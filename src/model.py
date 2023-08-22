from pydantic.dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Group:
    id: str
    name: str


@dataclass(frozen=True)
class User:
    id: str
    name: str
    handle: str | None


@dataclass(frozen=True)
class Player:
    user: User
    group: Group
    rating: int


@dataclass(frozen=True)
class Game:
    id: str
    timestamp: float
    player1: Player
    score1: int
    player2: Player
    score2: int


class ConfirmationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class UncomfirmedGame:
    game: Game
    status = ConfirmationStatus.PENDING
    responder: User
    confirmation_code: str
