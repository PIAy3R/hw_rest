import json
import os
from pathlib import Path
from hw_rest.Dto.restct import Config
from hw_rest.Dto.testcase import Testcase


rootpath = Config.dataPath

interLogPath = Config.logpath

def parseLogs():

    logdirs = getPaths(rootpath)

    for logdir in logdirs:
        Logs = os.listdir(logdir)
        for log in Logs:
            log = Path(logdir + '/' +log)
            with log.open("r") as fp:
                responselog = json.load(fp)
            operation = responselog.get('name')
            response_dict = responselog.get('testInteractions', {})[0]
            test_result = responselog.get('testResults', {})

            testcase = Testcase.buildCase(operation, response_dict, test_result)

            if testcase.judge == 'FAIL' and testcase.response_code == 500:
                print(testcase.operation)
                print(testcase.url)
                print(testcase.response_code)
                print(testcase.response_body)
                print(testcase.judge)
                print(testcase.tags)
                print()

def getPaths(rootPath):
    logdirs = list()
    APILogs = os.listdir(rootpath)
    for apis in APILogs:
        logpathNominal = Config.dataPath + apis +'/Report/NominalFuzzer'
        logpathError = Config.dataPath + apis + '/Report/ErrorFuzzer'
        logdirs.append(logpathNominal)
        logdirs.append(logpathError)
    return logdirs



def parseInterLogs():
    filePath = Path(interLogPath)
    for line in open(filePath, "r", encoding='UTF-8'):
        print(line)

parseInterLogs()


