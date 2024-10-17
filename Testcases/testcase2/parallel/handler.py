import random
import time
import threading
import json 
import requests

# replace AWS arn with do-alu OpenFaas function URL
AluFunctionArn = 'http://192.168.64.27:8080/function/do-alu'
def handle(event):
    startTime = GetTime()
    if 'n' in event:
        times = event['n']
        parallelIndex = event['parallelIndex']
        temp = alu(times,parallelIndex)
        tot_exec = 0
        tempdict = eval(temp)
        for execTime in tempdict:
            print(execTime)
            tot_exec += int(execTime)
        avg_exec = tot_exec / parallelIndex
        return{
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
    #botoClient = boto3.client('lambda')
    payload = bytes("{\"n\": %d}" %(times / parallelIndex), encoding="utf8")
    resultTexts = []
    threads = []

    for i in range(parallelIndex):
        t = threading.Thread(target=singleAlu, args=(payload, resultTexts, i))
        threads.append(t)
        resultTexts.append('')

    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()

    return str(resultTexts)

def singleAlu(payload, resultTexts, botoClient, clientId):
    clientStartTime = GetTime()
    '''
    response = botoClient.invoke(
        FunctionName = AluFunctionArn,
        Payload = payload,
    )'''
     # Perform an HTTP POST request to the OpenFaaS function
    response = requests.post(AluFunctionUrl, data=payload)

    clientEndTime = GetTime()
    clientExecTime = clientEndTime - clientStartTime
    singleAluTimeinfo = "client %d startTime: %s, retTime: %s, execTime %s" %(clientId, clientStartTime, clientEndTime, clientExecTime)

    #result = json.loads(response['Payload'].read())
    result = response.json() # parse JSON response
    resultTexts[clientId] = str(result['execTime'])
    print("client %d finished" %clientId)