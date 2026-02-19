from datetime import date
from glob import glob
import json
import os
import re


def _getTodayDateStamp():
    return str(date.today()).replace("-", "")


def _generateDataFileNameForUser(tag: str):
    return f"cache{os.sep}{_sanitizeTag(tag=tag)}-{_getTodayDateStamp()}-list.json"


def saveUserDataFile(tag: str, entries: list):
    with open(
        _generateDataFileNameForUser(tag=tag), "w"
    ) as file:
        json.dump(entries, file)


def _sanitizeTag(tag: str):
    return re.sub(r"[^a-zA-Z0-9_-]", "", tag)


def removeAllTagFile(tag: str):
    fileNames = glob(f"cache{os.sep}{_sanitizeTag(tag=tag)}-*-list.json")
    for fileName in fileNames:
        os.remove(fileName)


def latestValidTagFileOrNew(tag: str, clean=True):
    fileNames = glob(f"cache{os.sep}{_sanitizeTag(tag=tag)}-*-list.json")
    latestValidFileName = None
    latestValidDateStamp = None
    for fileName in fileNames:
        dateStamp = _extractDateStampFromFileName(fileName=fileName)
        if not latestValidDateStamp or dateStamp > latestValidDateStamp:
            if clean and latestValidFileName:
                os.remove(latestValidFileName)
            latestValidFileName = fileName
            latestValidDateStamp = dateStamp
        elif clean:
            os.remove(fileName)
    return latestValidFileName or _generateDataFileNameForUser(tag=tag)


def _extractDateStampFromFileName(fileName):
    return int(fileName.split("-")[-2])


def loadDataFromFile(userFile):
    if not os.path.exists(userFile):
        return None

    with open(userFile, "r") as file:
        userList = json.load(file)

    return userList
