import os
from github import Github
from ave import load_game_from_file
from ave.test import check_game

if os.environ["CIRCLE_BRANCH"] != "master":
    git = Github(os.environ["GH_TOKEN"])
    repo = git.get_repo("AVEGame/AVE-usergames")
    pulls = repo.get_pulls(
        head=os.environ["CIRCLE_PROJECT_USERNAME"] + ":" + os.environ["CIRCLE_BRANCH"],
        state="open")

    if pulls.totalCount != 1:
        print("Count not identify PR.")
        raise KeyboardInterrupt

    pr = pulls[0]

    gamename = pr.title.split()[-1]
    gamefile = os.path.join(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), ".."), gamename)

    game = load_game_from_file(gamefile)
    game.load()

    issues = check_game(game)
    errors = [i for i in issues if i.error_value > 3]
    info = [i for i in issues if i.error_value <= 3]
    errors.sort(key=lambda e: -e.error_value)
    info.sort(key=lambda e: -e.error_value)

    results = ""
    if len(errors) > 0:
        results += str(len(errors)) + " error"
        if len(errors) > 1:
            results += "s"
        results += " in " + gamename + "\n"
        for e in errors:
            results += "* " + str(e) + "\n"
        results += "\n"

        results += str(len(info)) + " note"
        if len(info) > 1:
            results += "s"
        results += " on " + gamename + "\n"
        for e in info:
            results += "* " + str(e) + "\n"

    if results == "":
        results = "No errors or issues were found in " + gamename + "."

    pr.create_issue_comment(body=results)
