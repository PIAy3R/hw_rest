import json
import os
from pathlib import Path
from hw_rest.Dto.restct import Config
from hw_rest.Dto.testcase import Testcase
from hw_rest.Dto.rtgCaseLog import TestLog,ErrorLog

class Paths:
    rootpath = Config.dataPath
    interLogPath = Config.logpath
    errorLogPath = Config.errorpath

TestCases = []
apiLogs = []
ErrorLogs = []

def parseTestCases():

    logdirs = getPaths(Paths.rootpath)

    for logdir in logdirs:
        Logs = os.listdir(logdir)
        for log in Logs:
            log = Path(logdir + '/' +log)
            with log.open("r") as fp:
                responselog = json.load(fp)
            operation = responselog.get('name')
            response_dict = responselog.get('testInteractions', {})[0]
            test_result = responselog.get('testResults', {})

            TestCases.append(Testcase.buildCase(operation, response_dict, test_result))

def getPaths(rootPath):
    logdirs = list()
    APILogs = os.listdir(Paths.rootpath)
    for apis in APILogs:
        logpathNominal = Config.dataPath + apis +'/Report/NominalFuzzer'
        logpathError = Config.dataPath + apis + '/Report/ErrorFuzzer'
        logdirs.append(logpathNominal)
        logdirs.append(logpathError)
    return logdirs


def parseInterLogs():
    filePath = Path(Paths.interLogPath)
    with filePath.open("r") as fp:
        for lines in fp:
            log = json.loads(lines)
            apiLogs.append(TestLog.buildtestlog(log))


def parsEerrorLog():
    filePath = Path(Paths.errorLogPath)
    with filePath.open("r") as fp:
        for lines in fp:
            log = json.loads(lines)
            ErrorLogs.append(ErrorLog.builderrorlog(log))


