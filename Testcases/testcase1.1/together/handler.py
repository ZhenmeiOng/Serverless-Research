# together.py
'''def handle(req):
    #print ("hello")
    print("hello2")

    return req'''

import time
import os
import random
from multiprocessing import Process, Pipe

defaultKey = "loopTime.txt"
defaultLoopTime = 10000000
defaultParallelIndex = 100

def handle(event, context=None):
    startTime = GetTime()
    if 'key' in event:
        key = event['key']
    else:
        key = defaultKey

    loopTime = extractLoopTime(key)  # key is the file path?

    retTime = GetTime()
    result1 = {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "loopTime": loopTime,
        "key": key
    }
    result_final = alu_handler(result1,"")
    #print (result_final)
    return result_final

def extractLoopTime(file_path):
    try:
        with open(file_path, 'r') as f:
            loopTime = int(f.readline().strip())
            print("loopTime: " + str(loopTime))
            return loopTime
    except Exception as e:
        print(f"Error reading loop time from file: {e}")
        return defaultLoopTime

def alu_handler(event, context=None):
    startTime = GetTime()
    if 'execTime' in event:
        execTime_prev = event['execTime']
    else:
        execTime_prev = 0
    if 'loopTime' in event:
        loopTime = event['loopTime']
    else:
        loopTime = defaultLoopTime
    parallelIndex = defaultParallelIndex
    temp = alu(loopTime, parallelIndex)
    retTime = GetTime()
    return {
        "loopTime": loopTime,
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": temp,
        'execTime_prev': execTime_prev
    }

def doAlu(times, childConn, clientId):
    a = random.randint(10, 100)
    b = random.randint(10, 100)
    temp = 0
    for i in range(times):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b
    #print(times)
    childConn.send(temp)
    childConn.close()
    return temp

def alu(times, parallelIndex):
    per_times = int(times / parallelIndex)
    threads = []
    childConns = []
    parentConns = []
    for i in range(parallelIndex):
        parentConn, childConn = Pipe()
        parentConns.append(parentConn)
        childConns.append(childConn)
        t = Process(target=doAlu, args=(per_times, childConn, i))
        threads.append(t)
    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()
    
    results = []
    for i in range(parallelIndex):
        results.append(parentConns[i].recv())
    return str(results)

def GetTime():
    return int(round(time.time() * 1000))

# for running locally in vm
if __name__ == "__main__":
    # Simulate a function call like OpenFaaS would make
    result = handler("", None)
    #print("Function output:")
    #print(result)