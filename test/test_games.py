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

    issues = check_game(game)
    errors = [i for i in issues if i.error_value > 3]
    info = [i for i in issues if i.error_value <= 3]
    errors.sort(key=lambda e: -e.error_value)
    info.sort(key=lambda e: -e.error_value)

    if len(errors) > 0:
        with open(results_txt, "a") as f:
            f.write(str(len(errors)) + " error(s) in " + filename + "\n")
            for e in errors:
                f.write("  " + str(e) + "\n")
            f.write("\n")
    if len(info) > 0:
        with open(results_txt, "a") as f:
            f.write(str(len(info)) + " info(s) in " + filename + "\n")
            for e in info:
                f.write("  " + str(e) + "\n")
            f.write("\n")

    # Assert that the worst error is a Warning or lower
    assert len(errors) == 0
