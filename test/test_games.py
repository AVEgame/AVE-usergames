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


@pytest.mark.parametrize('filename', games)
def test_games_for_errors(filename):
    game = load_game_from_file(filename)
    game.load()

    issues = check_game(game)
    errors = [i for i in issues if i.error_value > 3]
    info = [i for i in issues if i.error_value <= 3]
    errors.sort(key=lambda e: -e.error_value)
    info.sort(key=lambda e: -e.error_value)

    if len(errors) > 0:
        print("\n  " + str(len(errors)) + " errors(s) in " + filename)
        for e in errors:
            print(e)
    if len(info) > 0:
        print("\n  " + str(len(info)) + " info(s) in " + filename)
        for e in info:
            print(e)

    # Assert that the worst error is a Warning or lower
    assert len(errors) == 0
