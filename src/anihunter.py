import argparse
import os
import platform
import subprocess
import webbrowser
from apitools import countdownTimer_s, fetchDataForTag
from cachefiles import latestValidTagFileOrNew, loadDataFromFile, removeAllTagFile

parser = argparse.ArgumentParser()
parser.add_argument(
    "tags",
    help="anilist tag(s) you're interested in (or the path of a text file containing a list of tags on separate lines)",
    nargs="*",
)
parser.add_argument(
    "-l",
    "--localized",
    help="do NOT open pages in browser",
    action="store_true",
)
parser.add_argument(
    "-c",
    "--clean",
    help="choose to clear previous run data (this cannot be undone). all media will appear as new",
    action="store_true",
)
args = parser.parse_args()

allNewStuff = {}
tags: list[str] = []

while True:

    tagFile = None

    if not args.tags:
        tagFile = "tags.txt"
    elif len(args.tags) == 1 and os.path.exists(args.tags[0]):
        tagFile = args.tags[0]

    if tagFile:
        if not os.path.exists(tagFile):
            with open(tagFile, "w") as f:
                pass
        with open(tagFile, "r") as tf:
            tags = tf.readlines()
    else:
        tags = args.tags

    if len(tags) > 0:
        break

    if tagFile:
        input("Your tag file is empty!\nPress ENTER to open the file and add some tags (on separate lines)")
        if platform.system() == 'Darwin':    # macOS
            subprocess.call(('open', tagFile))
        elif platform.system() == 'Windows':  # Windows
            # Use shell=True for 'start' command to work correctly
            os.startfile(tagFile) # Or subprocess.call(('start', filepath), shell=True)
        else:                                # Linux variants
            try:
                # xdg-open is a standard on many Linux systems
                subprocess.call(('xdg-open', tagFile))
            except FileNotFoundError:
                subprocess.call(('nano', tagFile))
        input("Once you've saved your tag file, press ENTER to retry")

for rawTag in tags:
    cleanTag = rawTag.lower().strip()
    if args.clean:
        removeAllTagFile(cleanTag)

    filename = latestValidTagFileOrNew(tag=cleanTag, clean=False)
    prevStuff = {}
    if os.path.exists(filename):
        prevStuff = loadDataFromFile(filename)

    currentStuff = fetchDataForTag(tag=cleanTag)

    latestValidTagFileOrNew(tag=cleanTag)

    newKeys = set(currentStuff.keys()) - set(prevStuff.keys())

    newStuff = {k: currentStuff[k] for k in newKeys}

    allNewStuff |= newStuff

browserTabCounter = 1

if len(allNewStuff) == 0:
    print("Nothing new matching those tags. Add new tags or run with -c to clear cache")

for entry in allNewStuff.values():
    if not args.localized:
        url = f"https://anilist.co/{entry['type'].lower()}/{entry['id']}/"
        webbrowser.open_new_tab(url)
        if browserTabCounter % 10 == 0:
            input(f"Press ENTER to continue ({browserTabCounter}/{len(allNewStuff)})")
        browserTabCounter += 1


    if entry["title"]["english"]:
        print(entry["title"]["english"])
    else:
        print(entry["title"]["userPreferred"])
    print(f"{entry['type']}\n")
