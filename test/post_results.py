from github import Github
import os

results_txt = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "results.txt")

with open(results_txt) as f:
    results = f.read()

if results == "":
    results = "No errors or issues were found in any game."

git = Github(os.environ["GH_TOKEN"])
repo = git.get_repo("AVEGame/AVE-usergames")
pulls = repo.get_pulls(
    head=os.environ["CIRCLE_PROJECT_USERNAME"] + ":" + os.environ["CIRCLE_BRANCH"],
    state="open")

if pr.totalCount != 1:
    print("Count not identify PR.")
    raise KeyboardInterrupt

pr = pulls[0]

pr.create_comment(body=results)
