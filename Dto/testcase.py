from testoracle_kg.Dto.parameter import buildParam
from testoracle_kg.Dto.parameter import AbstractParam
from testoracle_kg.Dto.keywords import ParamKey, DocKey
from testoracle_kg.Exception.exceptions import UnsupportedError
import json
import re
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Set
from testoracle_kg.Dto.parameter import AbstractParam, EnumParam
from enum import Enum

class Testcase:
    def __init__(self, operationin, response_dictin: dict, test_resultin: dict):
        self.operation = operationin
        self.response_dict = response_dictin
        self.test_result = test_resultin
        self.url = str()
        self.response_code = str()
        self.response_body = str()
        self.judge = str()
        self.tag = list()

    def optimization(self):
        self.cutOperation()
        self.parseResponse()
        self.parseResult()
    def cutOperation(self):
        loc = self.operation.rindex('-')
        self.operation = self.operation[:loc]

    def parseResponse(self):
        self.url = self.response_dict.get('requestURL')
        self.response_code = self.response_dict.get('responseStatusCode').get('code')
        self.response_body = self.response_dict.get('responseBody')
        self.tag = self.response_dict.get('tags')

    def parseResult(self):
        self.judge = self.test_result.get('ErrorStatusCodeOracle').get('result')

