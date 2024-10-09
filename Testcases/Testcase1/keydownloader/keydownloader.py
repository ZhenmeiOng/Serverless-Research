## handler.py for keyDownloader

import time
import os

defaultKey = "loopTime.txt"

def handler(event, context):
    startTime = GetTime()
    if 'key' in event:
        key = event['key']
    else:
        key = defaultKey

    loopTime = extractLoopTime(key)

    retTime = GetTime()
    result = {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "loopTime": loopTime,
        "key": key
    }
    print (result)
    return result

def extractLoopTime(file_path):
    try:
        with open(file_path, 'r') as f:
            loopTime = int(f.readline().strip())
            print("loopTime: " + str(loopTime))
            return loopTime
    except Exception as e:
        print(f"Error reading loop time from file: {e}")


def GetTime():
    return int(round(time.time() * 1000))