from utils import *
from parseLogs import *


if __name__ == '__main__':
    parseTestCases()
    parseInterLogs()
    for cases in TestCases:
        # if int(cases.response_code) >= 200 and int(cases.response_code) < 400 and 'mutated' not in cases.tags:

        cases.showSelf()
        print()
    # for logs in apiLogs:
    #     if int(logs.statuscode) != 404:
    #         logs.printSelf()