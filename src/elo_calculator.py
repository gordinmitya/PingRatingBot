from typing import Tuple
from pydantic.dataclasses import dataclass

# https://worldoftanks.com/en/content/strongholds_guide/elo_rating/
# OR
# https://gordinmitya.notion.site/ELO-rating-2cb39259330d4ebcbffc53a7f4fa104d


@dataclass(frozen=True)
class EloInput:
    rating: int
    score: int

    def __post_init__(self):
        assert self.rating >= 0, "Rating must be positive"
        assert self.score >= 0, "Score must be positive"


@dataclass(frozen=True)
class EloRatingChange:
    old_rating: int
    new_rating: int
    rating_change: int

    def __post_init__(self):
        assert self.old_rating >= 0, "Old rating must be positive"
        assert self.new_rating >= 0, "New rating must be positive"
        assert self.old_rating + self.rating_change == self.new_rating, "Rating change must be correct"


class EloCalculator:
    INITIAL_RATING: int = 1000

    @staticmethod
    def calc(given: Tuple[EloInput]) -> Tuple[EloRatingChange]:
        assert len(given) == 2, "Only 2 players are allowed"
        player_a, player_b = given
        diff_a = EloCalculator.individual_diff(player_a.rating, player_b.rating, player_a.score - player_b.score)
        diff_b = EloCalculator.individual_diff(player_b.rating, player_a.rating, player_b.score - player_a.score)
        return (
            EloRatingChange(player_a.rating, player_a.rating + diff_a, diff_a),
            EloRatingChange(player_b.rating, player_b.rating + diff_b, diff_b),
        )

    @staticmethod
    def individual_diff(ratingA: int, ratingB: int, scoreDiff: int) -> int:
        # Calculate the expected score based on the ratings
        e = 1.0 / (1 + 10 ** ((ratingB - ratingA) / 400.0))
        
        # Determine the actual score based on the score difference
        if scoreDiff > 0:
            s = 1.0
        elif scoreDiff == 0:
            s = 0.5
        elif scoreDiff < 0:
            s = 0.0
        else:
            assert False

        # Choose the K-factor based on the player's rating
        if ratingA > 3000:
            k = 5.0
        elif ratingA >= 2401:
            k = 10.0
        elif ratingA >= 601:
            k = 15.0
        elif ratingA >= 0:
            k = 25.0
        else:
            assert False, "Rating must be positive"

        # Calculate the new rating difference
        p = round(k * (s - e))
        
        # Ensure the rating does not become negative
        if ratingA + p < 0:
            return -ratingA

        return p
