import pytest
import os
from ave import config
from ave import load_game_from_file
from ave.test import check_game

config.debug = True
games_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..")

games = [os.path.join(games_path, filename)
         for filename in os.listdir(games_path) if filename[-4:] == ".ave"]

results_txt = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "results.txt")
with open(results_txt, "w") as f:
    pass


@pytest.mark.parametrize('filename', games)
def test_games_for_errors(filename):
    game = load_game_from_file(filename)
    game.load()

    # Assert that the worst error is an AVEWarning or lower
    errors = [i for i in check_game(game) if i.error_value > 3]
    errors.sort(key=lambda e: -e.error_value)

    for e in errors:
        print(e)

    assert len(errors) == 0
