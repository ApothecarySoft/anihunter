import argparse
import os
import webbrowser
from apitools import fetchDataForTag
from cachefiles import latestValidTagFileOrNew, loadDataFromFile, removeAllTagFile

parser = argparse.ArgumentParser()
parser.add_argument(
    "tag",
    help="an anilist tag you're interested in",
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

if args.clean:
    removeAllTagFile(args.tag)

filename = latestValidTagFileOrNew(tag=args.tag, clean=False)
prevStuff = {}
if os.path.exists(filename):
    prevStuff = loadDataFromFile(filename)

currentStuff = fetchDataForTag(tag=args.tag)

newKeys = set(currentStuff.keys()) - set(prevStuff.keys())

newStuff = {k: currentStuff[k] for k in newKeys}

for entry in newStuff.values():
    if args.browser:
        url = f"https://anilist.co/{entry['type'].lower()}/{entry['id']}/"
        webbrowser.open_new_tab(url)

    if entry["title"]["english"]:
        print(entry["title"]["english"])
    else:
        print(entry["title"]["userPreferred"])
    print(f"{entry['type']}\n")
