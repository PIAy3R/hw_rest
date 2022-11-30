from utils import *
from parseLogs import *
import spacy
import re

def classify(TestCase:list):
    for cases in TestCase:
        if 'does not have a valid value' in re.findall(r'does not have a valid value', cases.response_body):
            print('param value invalid')
        elif 'is invalid' in re.findall(r'is invalid', cases.response_body):
            print('param invalid')
        elif '404' in re.findall(r'404', cases.response_body):
            continue
        if 'only' in re.findall(r'only', cases.response_body):
            cases.showSelf()
            print()


if __name__ == '__main__':
    parseTestCases()
    classify(TestCases)
