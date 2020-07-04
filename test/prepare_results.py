import os

results_txt = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "results.txt")

with open(results_txt) as f:
    results = f.read()

if results == "":
    with open(results_txt, "w") as f:
        "No errors or issues were found in any game."
