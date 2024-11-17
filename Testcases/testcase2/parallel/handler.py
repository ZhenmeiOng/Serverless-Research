import random
import time
import threading
import json 
import requests

url = 'http://192.168.64.27:8080/function/do-alu'
def handle(req):
    startTime = GetTime()
    event = json.loads(req) # convert json to python dictionary
    if 'n' in event:
        times = event['n']
        parallelIndex = event['parallelIndex']
        temp = alu(times,parallelIndex)
        tot_exec = 0
        tempdict = eval(temp) # change string to list
        for execTime in tempdict:
            tot_exec += int(execTime)
        avg_exec = tot_exec / parallelIndex
        return {
            'result': temp,
            'avg_exec':avg_exec,
            'times': times,
            'execTime': GetTime() - startTime
        }
    else:
        return{
            'error': "No n in event"
        }
    


def GetTime():
    return int(round(time.time() * 1000))

def alu(times, parallelIndex):
    # serialize the byte string into a JSON string
    payload = {"n": times // parallelIndex}

    resultTexts = []
    threads = []

    for i in range(parallelIndex):
        t = threading.Thread(target=singleAlu, 
                             args=(payload, resultTexts, i))
        threads.append(t)
        resultTexts.append('')

    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()

    return str(resultTexts)

def singleAlu(payload, resultTexts, clientId):
    # clientStartTime = GetTime()

     # call do-alu and get returned values
    response = requests.post(url, json=payload)

    # clientEndTime = GetTime()
    # clientExecTime = clientEndTime - clientStartTime
    # singleAluTimeinfo = "client %d startTime: %s, retTime: %s, execTime %s" %(clientId, clientStartTime, clientEndTime, clientExecTime)

    result = response.json() # parse JSON response
    resultTexts[clientId] = str(result['execTime'])
    print("client %d finished" %clientId)
    print(result['times'])
    print(result['execTime'])

