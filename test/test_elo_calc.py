import pytest
from elo_calculator import EloCalculator, EloInput, EloRatingChange


def test_valid_input():
    input_a = EloInput(rating=1500, score=1)
    input_b = EloInput(rating=1400, score=0)
    changes = EloCalculator.calc((input_a, input_b))
    assert changes[0].rating_change > 0
    assert changes[1].rating_change < 0


def test_draw_scenario():
    input_a = EloInput(rating=1500, score=1)
    input_b = EloInput(rating=1500, score=1)
    changes = EloCalculator.calc((input_a, input_b))
    assert changes[0].rating_change == 0
    assert changes[1].rating_change == 0


def test_negative_rating():
    with pytest.raises(Exception, match="Rating must be positive"):
        EloInput(rating=-1500, score=1)


def test_negative_score():
    with pytest.raises(Exception, match="Score must be positive"):
        EloInput(rating=1500, score=-1)


def test_invalid_number_of_players():
    input_a = EloInput(rating=1500, score=1)
    with pytest.raises(Exception, match="Only 2 players are allowed"):
        EloCalculator.calc((input_a,))
    with pytest.raises(Exception, match="Only 2 players are allowed"):
        EloCalculator.calc((input_a, input_a, input_a))


def test_minimum_rating():
    input_a = EloInput(rating=0, score=0)
    input_b = EloInput(rating=0, score=1)
    changes = EloCalculator.calc((input_a, input_b))
    assert changes[0].rating_change == 0
    assert changes[1].rating_change > 0


def test_invalid_rating_change():
    with pytest.raises(Exception, match="Rating change must be correct"):
        EloRatingChange(old_rating=1500, new_rating=1600, rating_change=200)


def test_rating_becomes_negative():
    input_a = EloInput(rating=11, score=0)
    input_b = EloInput(rating=10, score=1)
    changes = EloCalculator.calc((input_a, input_b))
    assert changes[0].new_rating == 0
    assert changes[1].new_rating > 0


def test_high_rating_difference():
    input_a = EloInput(rating=3000, score=0)
    input_b = EloInput(rating=1000, score=1)
    changes = EloCalculator.calc((input_a, input_b))
    assert changes[0].rating_change < 0
    assert changes[1].rating_change > 0


def test_abs_score_dont_matter():
    input_a = EloInput(rating=3000, score=1)
    input_b = EloInput(rating=1000, score=1001)
    changes_high = EloCalculator.calc((input_a, input_b))

    input_a = EloInput(rating=3000, score=1)
    input_b = EloInput(rating=1000, score=2)
    changes_low = EloCalculator.calc((input_a, input_b))

    assert changes_high[0].rating_change == changes_low[0].rating_change
    assert changes_high[1].rating_change == changes_low[1].rating_change
