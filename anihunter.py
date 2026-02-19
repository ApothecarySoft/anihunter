import argparse
import os
import webbrowser
from apitools import fetchDataForTag
from cachefiles import latestValidTagFileOrNew, loadDataFromFile, removeAllTagFile

parser = argparse.ArgumentParser()
parser.add_argument(
    "tags",
    help="anilist tag(s) you're interested in",
    nargs="+"
)
parser.add_argument(
    "-b",
    "--browser",
    help="open all new things in the default browser",
    action="store_true",
)
parser.add_argument(
    "-c",
    "--clean",
    help="choose to clear previous run data (this cannot be undone). all media will appear as new",
    action="store_true"
)
args = parser.parse_args()

allNewStuff = {}
tags: list[str] = []

if os.path.exists(args.tags[0]):
    with open(args.tags[0], "r") as tagFile:
        tags = tagFile.readlines()
else:
    tags = args.tags

for rawTag in tags:
    cleanTag = rawTag.lower().strip()
    if args.clean:
        removeAllTagFile(cleanTag)

    filename = latestValidTagFileOrNew(tag=cleanTag, clean=False)
    prevStuff = {}
    if os.path.exists(filename):
        prevStuff = loadDataFromFile(filename)

    latestValidTagFileOrNew(tag=cleanTag)

    currentStuff = fetchDataForTag(tag=cleanTag)

    newKeys = set(currentStuff.keys()) - set(prevStuff.keys())

    newStuff = {k: currentStuff[k] for k in newKeys}

    allNewStuff |= newStuff

for entry in allNewStuff.values():
    if args.browser:
        url = f"https://anilist.co/{entry['type'].lower()}/{entry['id']}/"
        webbrowser.open_new_tab(url)

    if entry["title"]["english"]:
        print(entry["title"]["english"])
    else:
        print(entry["title"]["userPreferred"])
    print(f"{entry['type']}\n")
