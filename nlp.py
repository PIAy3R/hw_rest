from utils import *
from parseLogs import *
import spacy


if __name__ == '__main__':
    parseTestCases()
    for cases in TestCases:
        if int(cases.response_code) >= 200 and int(cases.response_code) < 400:
            cases.showSelf()
            print()
    # for logs in apiLogs:
    #     if int(logs.statuscode) != 404:
    #         logs.printSelf()