from utils import *
from parseLogs import *
import spacy
import re

if __name__ == '__main__':
    parseTestCases()
    for cases in TestCases:
        if re.match('is invalid', cases.response_body) != None:
            print(cases.response_body)