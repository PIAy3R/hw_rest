import json
import os
from pathlib import Path
from hw_rest.Dto.restct import Config
from hw_rest.Dto.testcase import Testcase
from hw_rest.Dto.rtgCaseLog import TestLog,ErrorLog

rootpath = Config.dataPath
interLogPath = Config.logpath
errorLogPath = Config.errorpath

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
    with filePath.open("r") as fp:
        for lines in fp:
            log = json.loads(lines)
            baseCls = TestLog.buildtestlog(log)
            print(baseCls)
            print(baseCls.statuscode)
            for dict in baseCls.paramslist:
                print(dict)
            print()

def parsEerrorLog():
    filePath = Path(errorLogPath)
    with filePath.open("r") as fp:
        for lines in fp:
            log = json.loads(lines)
            errorcls = ErrorLog.builderrorlog(log)
            print(errorcls.exceptionmessage)
            print(errorcls.exceptionbacktrace)
            print()



parseInterLogs()
# parsEerrorLog()

