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
        response_dict = responselog.get('testInteractions', {})[0]
        test_result = responselog.get('testResults', {})

        testcase = Testcase(operation, response_dict, test_result)
        testcase.optimization()


        print(testcase.operation)
        print(testcase.url)
        print(testcase.response_code)
        print(testcase.response_body)
        print(testcase.judge)
        print(testcase.tag)
        print()

parseLogs()