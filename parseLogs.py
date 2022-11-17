import json
import os
from pathlib import Path

from hw_rest.Dto.restct import Config
from hw_rest.Dto.testcase import Testcase


Logs = os.listdir(Config.dataPath)
def parseLogs():
    for log in Logs:
        log = Path(Config.dataPath + '/' +log)
        with log.open("r") as fp:
            responselog = json.load(fp)
        operation = responselog.get('name')
        response_dict = responselog.get('testInteractions', {})
        test_result = responselog.get('testResults', {})

        testcase = Testcase(operation, response_dict, response_dict)
        testcase.optimization()
        print(testcase.operation)

parseLogs()