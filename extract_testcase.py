import json
import os
from pathlib import Path
from hw_rest.Dto.restct import Config
import string

rootpath = Config.dataPath
baseurl = 'http://localhost:30000/api/v4'

class TestCase:
    def __init__(self):
        self.testcases = dict()
        self.operation = dict()
        self.infos = dict()
        self.assignment = dict()
        self.headers = dict()
        self.params = dict()
        self.responese = dict()



    def extractTestCase(self,logdir):
        Logs = os.listdir(logdir)
        count = 0
        for log in Logs:
            log = Path(logdir + '/' + log)
            with log.open("r") as fp:
                responselog = json.load(fp)
            split = str(responselog.get('name')).split('-')
            operationstr = baseurl + split[1] + '***' + split[0].lower() + '***' + str(count)

            self.assignment['url'] = responselog.get('testInteractions')[0].get('requestURL')

            self.headers['Content-Type'] = 'application/json'
            self.headers['PRIVATE-TOKEN'] = 'YOUR PRIVATE TOKEN'
            self.assignment['headers'] = self.headers

            if len(responselog.get('testInteractions')[0].get('requestURL').split('?')) > 1:
                print(responselog.get('testInteractions')[0].get('requestURL').split('?')[1].split('&'))

            self.infos['assignment'] = self.assignment



            self.infos['status_code'] = responselog.get('testInteractions')[0].get('responseStatusCode').get('code')

            if 'mutated' not in responselog.get('testInteractions')[0].get('tags'):
                self.responese['message'] = responselog.get('testResults').get('StatusCodeOracle').get('message')
            else:
                self.responese['message'] = responselog.get('testResults').get('ErrorStatusCodeOracle').get('message')

            self.infos['response'] = self.responese

            print(self.infos)



def getPaths(rootPath):
    logdirs = list()
    APILogs = os.listdir(rootpath)
    for apis in APILogs:
        logpathNominal = Config.dataPath + apis +'/Report/NominalFuzzer'
        logpathError = Config.dataPath + apis + '/Report/ErrorFuzzer'
        logdirs.append(logpathNominal)
        logdirs.append(logpathError)
    return logdirs

if __name__ == "__main__":
    logdirs = getPaths(rootPath=rootpath)

    for logdir in logdirs:
        testcase = TestCase()
        testcase.extractTestCase(logdir)

